from fastapi import APIRouter, HTTPException
from app.schemas.schemas import TransactionDetailResponse
from app.blockchain.client import blockchain_service

router = APIRouter(prefix="/blockchain", tags=["Blockchain"])

@router.get("/transaction/{tx_hash}", response_model=TransactionDetailResponse)
def get_transaction(tx_hash: str):
    details = blockchain_service.get_transaction_details(tx_hash)
    if "error" in details:
        raise HTTPException(status_code=404, detail=details["error"])
    return details
