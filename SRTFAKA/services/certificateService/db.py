import sqlite3
from datetime import datetime
import os
from typing import Optional, Any
from sqlalchemy.orm import sessionmaker, mapped_column, relationship, Mapped, DeclarativeBase
from sqlalchemy import Integer, String, DateTime, ForeignKey, Time, JSON, Date
from sqlalchemy.ext.hybrid import hybrid_property
from apiGateway.base import Base

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
    years_valid: Mapped[int] = mapped_column(Integer, nullable=True)   # number of years the cert is valid for
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    additional_info: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True) # maps to a dictionary
    
    #FK
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey('course.id'), nullable=True) # 1:1
    
class UserCertificate(Base):
    __tablename__ = 'user_cert'
    id: Mapped[int] = mapped_column(primary_key=True)
    issued_on: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expires_on: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    additional_info: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True)
    
    #FK
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)    # Use this to access user obj
    cert_id: Mapped[int] = mapped_column(Integer, ForeignKey('certificate.id'), nullable=False)

    #cert_info: Mapped[Certificate] = relationship(foreign_keys='certificate.id')
     # Corrected Relationship
    #cert_info: Mapped[Certificate] = relationship("Certificate", foreign_keys=[cert_id])
    cert_info: Mapped["Certificate"] = relationship("Certificate", foreign_keys=[cert_id])



#Base.metadata.create_all(engine)


# =====================================
#  **Helper Functions for Queries**
# =====================================

def create_certificate(db: Session, name: str, course_id: int, validity_period: time, description: str, additional_info: dict):
    """Creates a new generic certificate in the database."""
    new_cert = Certificate(
        name=name,
        course_id=course_id,
        validity_period=validity_period,
        description=description,
        additional_info=additional_info
    )
    db.add(new_cert)
    db.commit()
    db.refresh(new_cert)
    # Debugging
    print(f"Created certificate: {new_cert}")
    print(f"Certificate ID: {new_cert.id}")  # Check if `id` is populated
    print(f"Certificate attributes: {new_cert.__dict__}")  # Print all attributes
    return new_cert

def issue_certificate(db: Session, user_id: int, cert_id: int, issued_on: datetime, expires_on: datetime, additional_info: dict):
    """Issues a new certificate to a user based on an existing certificate."""
    cert = db.query(Certificate).filter(Certificate.id == cert_id).first()
    if not cert:
        return None  # Certificate does not exist

    new_user_cert = UserCertificate(
        user_id=user_id,
        cert_id=cert_id,
        issued_on=issued_on,
        expires_on=expires_on,
        additional_info=additional_info
    )
    db.add(new_user_cert)
    db.commit()
    db.refresh(new_user_cert)
    return new_user_cert

def get_user_certificates(db: Session, user_id: int):
    """Fetches all certificates owned by a specific user."""
    return db.query(UserCertificate).filter(UserCertificate.user_id == user_id).all()



