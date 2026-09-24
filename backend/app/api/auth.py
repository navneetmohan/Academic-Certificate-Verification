from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.models import Institution
from app.schemas.schemas import LoginRequest, TokenResponse, InstitutionResponse
from app.services.auth_service import verify_password, create_access_token, get_current_institution

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    institution = db.query(Institution).filter(Institution.email == login_data.email).first()
    if not institution or not verify_password(login_data.password, institution.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_access_token(data={"sub": institution.email, "id": institution.id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "institution": institution
    }

@router.get("/me", response_model=InstitutionResponse)
def get_current_user(current_institution: Institution = Depends(get_current_institution)):
    return current_institution
