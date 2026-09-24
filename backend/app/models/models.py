import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Institution(Base):
    __tablename__ = "institutions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    wallet_address = Column(String(42), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_authorized = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    certificates = relationship("Certificate", back_populates="institution")


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    certificate_id = Column(String(64), unique=True, index=True, nullable=False)
    student_name = Column(String(255), nullable=False)
    student_id = Column(String(100), nullable=False)
    degree = Column(String(255), nullable=False)
    department = Column(String(255), nullable=False)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    graduation_year = Column(Integer, nullable=False)
    certificate_type = Column(String(100), default="Degree Certificate")
    issue_date = Column(String(50), nullable=False)
    file_path = Column(String(512), nullable=False)
    certificate_hash = Column(String(66), nullable=False, index=True) # 0x + 64 hex characters
    blockchain_tx_hash = Column(String(66), nullable=False)
    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    institution = relationship("Institution", back_populates="certificates")
    transactions = relationship("BlockchainTransaction", back_populates="certificate")


class BlockchainTransaction(Base):
    __tablename__ = "blockchain_transactions"

    id = Column(Integer, primary_key=True, index=True)
    certificate_id = Column(String(64), ForeignKey("certificates.certificate_id"), nullable=False, index=True)
    transaction_hash = Column(String(66), unique=True, index=True, nullable=False)
    transaction_type = Column(String(50), nullable=False)  # 'ISSUE' or 'REVOKE'
    block_number = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    certificate = relationship("Certificate", back_populates="transactions")
