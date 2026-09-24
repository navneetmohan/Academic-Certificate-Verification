import os
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base, Institution

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./certificates.db")

# SQLite requires check_same_thread=False for multithreading
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if default institution exists
        default_email = os.getenv("DEFAULT_INSTITUTION_EMAIL", "admin@university.edu")
        existing = db.query(Institution).filter(Institution.email == default_email).first()
        if not existing:
            default_wallet = os.getenv(
                "DEFAULT_INSTITUTION_WALLET",
                "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"  # Hardhat Account #1
            )
            default_password = os.getenv("DEFAULT_INSTITUTION_PASSWORD", "adminpassword123")
            hashed_pwd = bcrypt.hashpw(default_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            admin_inst = Institution(
                name="Metropolitan State University",
                wallet_address=default_wallet,
                email=default_email,
                hashed_password=hashed_pwd,
                is_authorized=True
            )
            db.add(admin_inst)
            db.commit()
            print(f"[DB] Initialized default institution: {admin_inst.name} ({admin_inst.email})")
    finally:
        db.close()
