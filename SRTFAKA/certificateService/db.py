import sqlite3
from datetime import datetime
import os
from typing import Optional, Any
from sqlalchemy.orm import sessionmaker, mapped_column, relationship, Mapped, DeclarativeBase, Session
from sqlalchemy import Integer, String, DateTime, ForeignKey, Time, JSON, create_engine
from sqlalchemy.ext.hybrid import hybrid_property
from apiGateway.base import Base

# Database Connection
DATABASE_URL = "postgresql+psycopg2://postgres:password@127.0.0.1:5433/academy_db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Certificate(Base):
    """
    _Holds the details of the generic certificate, not the specific one awarded to the user._
    Args:
        Base (_sqlalchemy.declarativebase_): _Link to the Base model class for declaring ORM models_
    Parameters:
        id (_int_): Unique ID of the Certificate Base
    """
    __tablename__ = 'certificate'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    validity_period: Mapped[datetime.time] = mapped_column(Time)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    additional_info: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True) # maps to a dictionary
    
    #FK
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey('course.id')) # 1:1 
    
class UserCertificate(Base):
    __tablename__ = 'user_cert'
    id: Mapped[int] = mapped_column(primary_key=True)
    issued_on: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expires_on: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    additional_info: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True)
    
    #FK
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)    # Use this to access user obj
    cert_id: Mapped[int] = mapped_column(Integer, ForeignKey('certificate.id'), nullable=False)

    cert_info: Mapped[Certificate] = relationship(foreign_keys='certificate.id')

# =====================================
#  **Helper Functions for Queries**
# =====================================

def create_certificate(db: Session, name: str, course_id: int, blockchain_tx_id: str = None, certificate_hash: str = None):
    """Create and store a new certificate in the database."""
    new_cert = Certificate(
        name=name,
        course_id=course_id,
        blockchain_tx_id=blockchain_tx_id,
        certificate_hash=certificate_hash
    )
    db.add(new_cert)
    db.commit()
    db.refresh(new_cert)
    return new_cert

def get_all_certificates(db: Session):
    """Fetch all certificates from the database."""
    return db.query(Certificate).all()

def get_certificate_by_id(db: Session, certificate_id: int):
    """Fetch a specific certificate by its ID."""
    return db.query(Certificate).filter(Certificate.id == certificate_id).first()

def update_certificate(db: Session, certificate_id: int, name: str = None, course_id: int = None):
    """Update an existing certificate in the database."""
    certificate = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if not certificate:
        return None

    if name:
        certificate.name = name
    if course_id:
        certificate.course_id = course_id

    db.commit()
    return certificate

def delete_certificate(db: Session, certificate_id: int):
    """Delete a certificate from the database."""
    certificate = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if certificate:
        db.delete(certificate)
        db.commit()
        return True
    return False

def get_user_certificates(db: Session, user_id: int):
    """Fetch all certificates belonging to a specific user."""
    return db.query(UserCertificate).filter(UserCertificate.user_id == user_id).all()
