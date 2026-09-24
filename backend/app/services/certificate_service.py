import os
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.models import Certificate, Institution, BlockchainTransaction
from app.schemas.schemas import CertificateCreateRequest, CertificateResponse
from app.utils.pdf_generator import generate_certificate_pdf
from app.utils.hashing import compute_sha256
from app.blockchain.client import blockchain_service

CERTIFICATES_DIR = os.getenv("CERTIFICATE_STORAGE_PATH", os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../certificates")))

os.makedirs(CERTIFICATES_DIR, exist_ok=True)

def generate_unique_certificate_id(db: Session) -> str:
    """Generates sequential academic certificate ID format: CERT-YYYY-XXXX"""
    year = datetime.utcnow().year
    count = db.query(Certificate).count() + 1
    candidate_id = f"CERT-{year}-{count:04d}"
    
    while db.query(Certificate).filter(Certificate.certificate_id == candidate_id).first():
        count += 1
        candidate_id = f"CERT-{year}-{count:04d}"
        
    return candidate_id

def issue_new_certificate(
    data: CertificateCreateRequest,
    institution: Institution,
    db: Session
) -> Certificate:
    certificate_id = generate_unique_certificate_id(db)
    issue_date = data.issue_date or datetime.utcnow().strftime("%Y-%m-%d")
    institution_name = data.institution_name or institution.name

    # 1. Generate PDF Certificate
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    verification_base_url = f"{frontend_url}/verify"
    
    pdf_bytes = generate_certificate_pdf(
        certificate_id=certificate_id,
        student_name=data.student_name,
        student_id=data.student_id,
        degree=data.degree,
        department=data.department,
        institution_name=institution_name,
        graduation_year=data.graduation_year,
        issue_date=issue_date,
        certificate_type=data.certificate_type,
        verification_base_url=verification_base_url
    )

    # 2. Compute SHA-256 Hash of the PDF
    cert_hash = compute_sha256(pdf_bytes)

    # 3. Store PDF to local filesystem
    file_name = f"{certificate_id}.pdf"
    file_path = os.path.join(CERTIFICATES_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(pdf_bytes)

    # 4. Record Certificate Hash on Blockchain
    try:
        tx_result = blockchain_service.issue_certificate(
            certificate_id=certificate_id,
            certificate_hash=cert_hash
        )
        tx_hash = tx_result["tx_hash"]
        block_number = tx_result["block_number"]
    except Exception as e:
        # Clean up file if blockchain transaction fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Blockchain transaction failed: {str(e)}"
        )

    # 5. Persist Off-Chain Record in Database
    cert = Certificate(
        certificate_id=certificate_id,
        student_name=data.student_name,
        student_id=data.student_id,
        degree=data.degree,
        department=data.department,
        institution_id=institution.id,
        graduation_year=data.graduation_year,
        certificate_type=data.certificate_type,
        issue_date=issue_date,
        file_path=file_path,
        certificate_hash=cert_hash,
        blockchain_tx_hash=tx_hash,
        revoked=False
    )
    db.add(cert)
    db.flush()

    # Record blockchain transaction
    tx_record = BlockchainTransaction(
        certificate_id=certificate_id,
        transaction_hash=tx_hash,
        transaction_type="ISSUE",
        block_number=block_number
    )
    db.add(tx_record)
    db.commit()
    db.refresh(cert)

    return cert

def revoke_existing_certificate(
    certificate_id: str,
    institution: Institution,
    db: Session
) -> Certificate:
    cert = db.query(Certificate).filter(Certificate.certificate_id == certificate_id).first()
    if not cert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Certificate {certificate_id} not found."
        )

    if cert.institution_id != institution.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the issuing institution can revoke this certificate."
        )

    if cert.revoked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Certificate {certificate_id} is already revoked."
        )

    # Execute revocation on blockchain
    try:
        tx_result = blockchain_service.revoke_certificate(certificate_id)
        tx_hash = tx_result["tx_hash"]
        block_number = tx_result["block_number"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Blockchain revocation failed: {str(e)}"
        )

    # Update off-chain state
    cert.revoked = True
    tx_record = BlockchainTransaction(
        certificate_id=certificate_id,
        transaction_hash=tx_hash,
        transaction_type="REVOKE",
        block_number=block_number
    )
    db.add(tx_record)
    db.commit()
    db.refresh(cert)

    return cert
