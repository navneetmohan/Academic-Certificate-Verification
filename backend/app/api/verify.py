from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.schemas import VerifyResponse
from app.services.verification_service import verify_certificate_record
from app.models.models import Certificate

router = APIRouter(prefix="/verify", tags=["Verification"])

@router.get("/{certificate_id}", response_model=VerifyResponse)
def verify_by_id(
    certificate_id: str,
    db: Session = Depends(get_db)
):
    """
    Public verification endpoint to verify certificate authenticity on the blockchain by ID.
    """
    return verify_certificate_record(
        certificate_id=certificate_id,
        pdf_bytes=None,
        db=db
    )

@router.post("", response_model=VerifyResponse)
async def verify_uploaded_file(
    file: UploadFile = File(...),
    certificate_id: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Public verification endpoint accepting an uploaded PDF certificate.
    Computes cryptographic SHA-256 fingerprint and compares it to the immutable blockchain ledger.
    """
    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    return verify_certificate_record(
        certificate_id=certificate_id,
        pdf_bytes=pdf_bytes,
        db=db
    )

@router.post("/tamper-test/{certificate_id}", response_model=VerifyResponse)
def test_tampered_document(
    certificate_id: str,
    db: Session = Depends(get_db)
):
    """
    Demonstration helper endpoint: simulates a tampered certificate by altering bytes
    of an issued certificate to prove cryptographic tampering detection.
    """
    cert = db.query(Certificate).filter(Certificate.certificate_id == certificate_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")

    with open(cert.file_path, "rb") as f:
        original_bytes = bytearray(f.read())

    # Alter several bytes to simulate forgery/tampering
    if len(original_bytes) > 200:
        for idx in range(100, 110):
            original_bytes[idx] = (original_bytes[idx] + 1) % 256

    tampered_bytes = bytes(original_bytes)

    return verify_certificate_record(
        certificate_id=certificate_id,
        pdf_bytes=tampered_bytes,
        db=db
    )
