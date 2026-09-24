from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.models import Certificate, Institution
from app.schemas.schemas import VerifyResponse
from app.utils.hashing import compute_sha256, verify_hash_match
from app.blockchain.client import blockchain_service

def verify_certificate_record(
    certificate_id: Optional[str],
    pdf_bytes: Optional[bytes],
    db: Session
) -> VerifyResponse:
    now_iso = datetime.utcnow().isoformat() + "Z"
    calculated_hash = None

    if pdf_bytes is not None:
        calculated_hash = compute_sha256(pdf_bytes)

    # If certificate_id was not provided, try to find it by calculated_hash
    if not certificate_id and calculated_hash:
        match = db.query(Certificate).filter(Certificate.certificate_hash == calculated_hash).first()
        if match:
            certificate_id = match.certificate_id

    if not certificate_id:
        return VerifyResponse(
            status="NOT_FOUND",
            is_authentic=False,
            certificate_id=None,
            hash_matches=False,
            is_revoked=False,
            verified_at=now_iso,
            calculated_hash=calculated_hash,
            message="Certificate ID was not provided and could not be determined from the document."
        )

    # 1. Authoritative check on Blockchain
    try:
        onchain_status = blockchain_service.get_certificate_status(certificate_id)
    except Exception as e:
        return VerifyResponse(
            status="ERROR",
            is_authentic=False,
            certificate_id=certificate_id,
            hash_matches=False,
            is_revoked=False,
            verified_at=now_iso,
            calculated_hash=calculated_hash,
            message=f"Blockchain query error: {str(e)}"
        )

    if not onchain_status["exists"]:
        return VerifyResponse(
            status="NOT_FOUND",
            is_authentic=False,
            certificate_id=certificate_id,
            hash_matches=False,
            is_revoked=False,
            verified_at=now_iso,
            calculated_hash=calculated_hash,
            message="No blockchain record exists for this certificate ID."
        )

    onchain_hash = onchain_status["certificate_hash"]
    is_revoked = onchain_status["revoked"]
    issuer_addr = onchain_status["issuer"]
    issued_at = onchain_status["issued_at"]
    issued_at_iso = datetime.utcfromtimestamp(issued_at).isoformat() + "Z" if issued_at > 0 else None

    # Fetch institution public name and degree from DB if available (avoiding private PII)
    inst_name = None
    degree = None
    issue_date = None
    tx_hash = None
    db_cert = db.query(Certificate).filter(Certificate.certificate_id == certificate_id).first()
    if db_cert:
        degree = db_cert.degree
        issue_date = db_cert.issue_date
        tx_hash = db_cert.blockchain_tx_hash
        if db_cert.institution:
            inst_name = db_cert.institution.name

    # 2. Case Check: Hash Verification if PDF was provided
    if calculated_hash is not None:
        hash_matches = verify_hash_match(calculated_hash, onchain_hash)
        if not hash_matches:
            return VerifyResponse(
                status="INVALID",
                is_authentic=False,
                certificate_id=certificate_id,
                hash_matches=False,
                is_revoked=is_revoked,
                issuer_address=issuer_addr,
                institution_name=inst_name,
                degree=degree,
                issue_date=issue_date,
                issued_at=issued_at,
                issued_at_iso=issued_at_iso,
                verified_at=now_iso,
                onchain_hash=onchain_hash,
                calculated_hash=calculated_hash,
                tx_hash=tx_hash,
                message="The uploaded certificate does not match the cryptographic fingerprint recorded on the blockchain."
            )

    # 3. Case Check: Revocation
    if is_revoked:
        return VerifyResponse(
            status="REVOKED",
            is_authentic=False,
            certificate_id=certificate_id,
            hash_matches=(calculated_hash is None or verify_hash_match(calculated_hash, onchain_hash)),
            is_revoked=True,
            issuer_address=issuer_addr,
            institution_name=inst_name,
            degree=degree,
            issue_date=issue_date,
            issued_at=issued_at,
            issued_at_iso=issued_at_iso,
            verified_at=now_iso,
            onchain_hash=onchain_hash,
            calculated_hash=calculated_hash,
            tx_hash=tx_hash,
            message="This certificate was previously issued but has been revoked by the issuing institution."
        )

    # 4. Case Check: Authentic / Valid
    return VerifyResponse(
        status="VALID",
        is_authentic=True,
        certificate_id=certificate_id,
        hash_matches=True,
        is_revoked=False,
        issuer_address=issuer_addr,
        institution_name=inst_name,
        degree=degree,
        issue_date=issue_date,
        issued_at=issued_at,
        issued_at_iso=issued_at_iso,
        verified_at=now_iso,
        onchain_hash=onchain_hash,
        calculated_hash=calculated_hash or onchain_hash,
        tx_hash=tx_hash,
        message="Authenticity verified. Certificate cryptographic fingerprint matches the immutable blockchain ledger."
    )
