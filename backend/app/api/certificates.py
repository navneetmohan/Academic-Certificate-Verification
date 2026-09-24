import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.models import Certificate, Institution
from app.schemas.schemas import (
    CertificateCreateRequest,
    CertificateResponse,
    CertificateListItem
)
from app.services.auth_service import get_current_institution
from app.services.certificate_service import (
    issue_new_certificate,
    revoke_existing_certificate
)
from app.blockchain.client import blockchain_service

router = APIRouter(prefix="/certificates", tags=["Certificates"])

@router.post("", response_model=CertificateResponse, status_code=status.HTTP_201_CREATED)
def issue_certificate(
    data: CertificateCreateRequest,
    institution: Institution = Depends(get_current_institution),
    db: Session = Depends(get_db)
):
    cert = issue_new_certificate(data, institution, db)
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    return CertificateResponse(
        id=cert.id,
        certificate_id=cert.certificate_id,
        student_name=cert.student_name,
        student_id=cert.student_id,
        degree=cert.degree,
        department=cert.department,
        institution_name=cert.institution.name,
        graduation_year=cert.graduation_year,
        certificate_type=cert.certificate_type,
        issue_date=cert.issue_date,
        certificate_hash=cert.certificate_hash,
        blockchain_tx_hash=cert.blockchain_tx_hash,
        revoked=cert.revoked,
        created_at=cert.created_at,
        verification_url=f"{frontend_url}/verify/{cert.certificate_id}"
    )

@router.get("", response_model=List[CertificateListItem])
def list_certificates(
    institution: Institution = Depends(get_current_institution),
    db: Session = Depends(get_db)
):
    certs = db.query(Certificate).filter(
        Certificate.institution_id == institution.id
    ).order_by(Certificate.created_at.desc()).all()
    return certs

@router.get("/{certificate_id}", response_model=CertificateResponse)
def get_certificate_details(
    certificate_id: str,
    db: Session = Depends(get_db)
):
    cert = db.query(Certificate).filter(Certificate.certificate_id == certificate_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    return CertificateResponse(
        id=cert.id,
        certificate_id=cert.certificate_id,
        student_name=cert.student_name,
        student_id=cert.student_id,
        degree=cert.degree,
        department=cert.department,
        institution_name=cert.institution.name,
        graduation_year=cert.graduation_year,
        certificate_type=cert.certificate_type,
        issue_date=cert.issue_date,
        certificate_hash=cert.certificate_hash,
        blockchain_tx_hash=cert.blockchain_tx_hash,
        revoked=cert.revoked,
        created_at=cert.created_at,
        verification_url=f"{frontend_url}/verify/{cert.certificate_id}"
    )

@router.get("/{certificate_id}/download")
def download_certificate(
    certificate_id: str,
    db: Session = Depends(get_db)
):
    cert = db.query(Certificate).filter(Certificate.certificate_id == certificate_id).first()
    if not cert or not os.path.exists(cert.file_path):
        raise HTTPException(status_code=404, detail="Certificate file not found")

    return FileResponse(
        path=cert.file_path,
        media_type="application/pdf",
        filename=f"{cert.certificate_id}.pdf"
    )

@router.post("/{certificate_id}/revoke", response_model=CertificateResponse)
def revoke_certificate(
    certificate_id: str,
    institution: Institution = Depends(get_current_institution),
    db: Session = Depends(get_db)
):
    cert = revoke_existing_certificate(certificate_id, institution, db)
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    return CertificateResponse(
        id=cert.id,
        certificate_id=cert.certificate_id,
        student_name=cert.student_name,
        student_id=cert.student_id,
        degree=cert.degree,
        department=cert.department,
        institution_name=cert.institution.name,
        graduation_year=cert.graduation_year,
        certificate_type=cert.certificate_type,
        issue_date=cert.issue_date,
        certificate_hash=cert.certificate_hash,
        blockchain_tx_hash=cert.blockchain_tx_hash,
        revoked=cert.revoked,
        created_at=cert.created_at,
        verification_url=f"{frontend_url}/verify/{cert.certificate_id}"
    )

@router.get("/{certificate_id}/status")
def get_onchain_status(certificate_id: str):
    return blockchain_service.get_certificate_status(certificate_id)
