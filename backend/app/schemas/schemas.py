from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict

# Auth schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class InstitutionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    wallet_address: str
    email: str
    is_authorized: bool

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    institution: InstitutionResponse

# Certificate schemas
class CertificateCreateRequest(BaseModel):
    student_name: str = Field(..., min_length=2, max_length=255)
    student_id: str = Field(..., min_length=2, max_length=100)
    degree: str = Field(..., min_length=2, max_length=255)
    department: str = Field(..., min_length=2, max_length=255)
    institution_name: Optional[str] = None
    graduation_year: int = Field(..., ge=1950, le=2100)
    certificate_type: str = Field(default="Bachelor of Science", max_length=100)
    issue_date: Optional[str] = None

class CertificateListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    certificate_id: str
    student_name: str
    degree: str
    department: str
    issue_date: str
    revoked: bool
    blockchain_tx_hash: str
    created_at: datetime

class CertificateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    certificate_id: str
    student_name: str
    student_id: str
    degree: str
    department: str
    institution_name: str
    graduation_year: int
    certificate_type: str
    issue_date: str
    certificate_hash: str
    blockchain_tx_hash: str
    revoked: bool
    created_at: datetime
    verification_url: str


# Verification schemas
class VerifyResponse(BaseModel):
    status: str  # "VALID", "INVALID", "REVOKED", "NOT_FOUND"
    is_authentic: bool
    certificate_id: Optional[str] = None
    hash_matches: bool
    is_revoked: bool
    issuer_address: Optional[str] = None
    institution_name: Optional[str] = None
    degree: Optional[str] = None
    issue_date: Optional[str] = None
    issued_at: Optional[int] = None
    issued_at_iso: Optional[str] = None
    verified_at: str
    onchain_hash: Optional[str] = None
    calculated_hash: Optional[str] = None
    message: str
    tx_hash: Optional[str] = None

# Blockchain Transaction schemas
class TransactionDetailResponse(BaseModel):
    tx_hash: str
    block_number: Optional[int] = None
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    gas_used: Optional[int] = None
    status: Optional[int] = None
    timestamp: Optional[int] = None
    confirmations: Optional[int] = None

# Stats schemas
class DashboardStatsResponse(BaseModel):
    total_certificates: int
    valid_certificates: int
    revoked_certificates: int
    blockchain_connected: bool
    latest_block: int
    contract_address: str
    institution_wallet: str
