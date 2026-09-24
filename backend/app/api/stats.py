from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.models import Certificate
from app.schemas.schemas import DashboardStatsResponse
from app.blockchain.client import blockchain_service

router = APIRouter(prefix="/stats", tags=["Statistics"])

@router.get("", response_model=DashboardStatsResponse)
def get_dashboard_stats(db: Session = Depends(get_db)):
    total = db.query(Certificate).count()
    revoked = db.query(Certificate).filter(Certificate.revoked == True).count()
    valid = total - revoked

    is_connected = blockchain_service.is_connected()
    latest_block = blockchain_service.get_latest_block_number()
    contract_addr = blockchain_service.contract_address or "Not Deployed"

    return DashboardStatsResponse(
        total_certificates=total,
        valid_certificates=valid,
        revoked_certificates=revoked,
        blockchain_connected=is_connected,
        latest_block=latest_block,
        contract_address=contract_addr,
        institution_wallet=blockchain_service.issuer_address
    )
