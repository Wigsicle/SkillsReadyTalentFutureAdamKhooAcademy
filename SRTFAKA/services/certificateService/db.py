import sqlite3
from datetime import datetime
import os
from typing import Optional, Any
from sqlalchemy.orm import sessionmaker, mapped_column, relationship, Mapped, DeclarativeBase, Session
from sqlalchemy import Integer, String, DateTime, ForeignKey, Time, JSON, Date, JSON, create_engine
from sqlalchemy.ext.hybrid import hybrid_property
from apiGateway.base import Base
from dateutil.relativedelta import relativedelta

# Database Connection
DATABASE_URL = "postgresql+psycopg2://postgres:password@job_database:5432/academy_db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Return the session for use
    finally:
        db.close()  # Ensure session is closed

"""
    Minimal stub model for referencing the 'couse' and 'user' table. 
    This prevents circular imports with the accountService.
"""

class Course(Base):
    __tablename__ = "course"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


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
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=True)    # Use this to access user obj
    cert_id: Mapped[int] = mapped_column(Integer, ForeignKey('certificate.id'), nullable=False)

    #cert_info: Mapped[Certificate] = relationship(foreign_keys='certificate.id')
     # Corrected Relationship
    #cert_info: Mapped[Certificate] = relationship("Certificate", foreign_keys=[cert_id])
    cert_info: Mapped["Certificate"] = relationship("Certificate", foreign_keys=[cert_id])

#Base.metadata.create_all(engine)

# =====================================
#  **Helper Functions for Queries**
# =====================================

def create_certificate(
    db: Session, 
    name: str, 
    course_id: Optional[int],  # Can be None
    years_valid: Optional[int],  # Matches schema (nullable)
    description: Optional[str],  # Nullable
    additional_info: Optional[dict[str, Any]]  # Matches schema (nullable JSON)
):
    """Creates a new generic certificate in the database."""

    if course_id:  # Only check if course_id is provided
        #from db import Course  # Import inside function to avoid circular import
        from sqlalchemy.exc import NoResultFound

        try:
            db.query(Course).filter_by(id=course_id).one()
        except NoResultFound:
            raise ValueError(f"⚠️ Course ID {course_id} does not exist!")

    new_cert = Certificate(
        name=name,
        course_id=course_id,
        years_valid=years_valid,
        description=description,
        additional_info=additional_info
    )

    db.add(new_cert)
    db.commit()
    db.refresh(new_cert)

    # Debugging Logs
    print(f"✅ Created certificate: {new_cert}")
    print(f"🆔 Certificate ID: {new_cert.id}")  # Ensure ID is assigned
    print(f"📜 Certificate attributes: {vars(new_cert)}")  # Full attribute dump

    return new_cert



def issue_certificate(
    db: Session,
    user_id: int,
    cert_id: int,
    issued_on: datetime,
    expires_on: Optional[datetime] = None,
    additional_info: Optional[dict[str, Any]] = None
) -> UserCertificate:
    """
    Issues a new certificate to a user based on an existing certificate.
    
    Args:
        db (Session): The active database session.
        user_id (int): The ID of the user receiving the certificate.
        cert_id (int): The ID of the existing generic certificate.
        issued_on (datetime): The datetime when the certificate is issued.
        expires_on (Optional[datetime]): The datetime when the certificate expires (if applicable).
        additional_info (Optional[dict[str, Any]]): Additional details to store as JSON.
    
    Returns:
        UserCertificate: The newly issued user certificate.
    
    Raises:
        ValueError: If the certificate with the given cert_id does not exist.
    """
    # Verify that the certificate exists
    cert = db.query(Certificate).filter(Certificate.id == cert_id).first()
    if not cert:
        raise ValueError(f"Certificate with id {cert_id} does not exist!")
    # If the caller did not provide an expires_on, but the certificate has years_valid, compute it
    if expires_on is None and cert.years_valid:
        expires_on = issued_on + relativedelta(years=cert.years_valid)
    
    # Create a new UserCertificate record
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
    
    # Debug logs
    print(f"✅ Issued certificate {cert_id} to user {user_id}: {new_user_cert}")
    
    return new_user_cert

def get_user_certificates(db: Session, user_id: int) -> list[UserCertificate]:
    """
    Retrieves all certificates associated with the specified user.

    Args:
        db (Session): The active database session.
        user_id (int): The ID of the user whose certificates are to be retrieved.

    Returns:
        list[UserCertificate]: A list of UserCertificate objects for the given user.
    """
    # Optional: Verify the user actually exists. If you want to raise an error if not:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError(f"User with id {user_id} does not exist!")

    # Query the user_cert table for all certificates belonging to this user.
    user_certs = db.query(UserCertificate).filter(UserCertificate.user_id == user_id).all()
    
    # Debugging Logs
    print(f"✅ Retrieved {len(user_certs)} certificates for user {user_id}")

    return user_certs

def get_all_certificates(db: Session) -> list[Certificate]:
    """
    Retrieves all certificates from the database.

    Args:
        db (Session): The active database session.

    Returns:
        list[Certificate]: A list of all Certificate objects in the database.
    """
    # Query the Certificate table to get all certificates
    certificates = db.query(Certificate).all()
    
    # Debugging Logs
    print(f"✅ Retrieved {len(certificates)} certificates from the database.")

    return certificates

def update_certificate(
    db: Session,
    certificate_id: int,
    name: Optional[str] = None,
    course_id: Optional[int] = None,
    years_valid: Optional[int] = None,
    description: Optional[str] = None,
    additional_info: Optional[dict[str, Any]] = None
) -> Certificate:
    """
    Updates an existing generic certificate in the database.

    Args:
        db (Session): The active database session.
        certificate_id (int): The ID of the certificate to update.
        name (Optional[str]): New certificate name, if provided.
        course_id (Optional[int]): New course ID, if provided.
        years_valid (Optional[int]): New validity period, if provided.
        description (Optional[str]): New description, if provided.
        additional_info (Optional[dict[str, Any]]): New JSON metadata, if provided.

    Returns:
        Certificate: The updated Certificate object.

    Raises:
        ValueError: If the certificate does not exist, or if a new course_id is provided and the course doesn't exist.
    """
    # Query the certificate by id
    cert = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if not cert:
        raise ValueError(f"Certificate with id {certificate_id} does not exist!")
    
    # If a new course_id is provided, verify that the course exists (to match the behavior in create_certificate)
    if course_id is not None:
        #from db import Course  # Import inside function to avoid circular import
        from sqlalchemy.exc import NoResultFound
        try:
            db.query(Course).filter_by(id=course_id).one()
        except NoResultFound:
            raise ValueError(f"⚠️ Course ID {course_id} does not exist!")
        cert.course_id = course_id

    if name is not None:
        cert.name = name
    if years_valid is not None:
        cert.years_valid = years_valid
    if description is not None:
        cert.description = description
    if additional_info is not None:
        cert.additional_info = additional_info

    db.commit()
    db.refresh(cert)

    # Debug logs
    print(f"✅ Updated Certificate ID: {cert.id}")
    print(f"📜 New attributes: {vars(cert)}")
    
    return cert


def update_user_certificate(
    db: Session,
    user_cert_id: int,
    user_id: Optional[int] = None,
    cert_id: Optional[int] = None,
    issued_on: Optional[datetime] = None,
    expires_on: Optional[datetime] = None,
    additional_info: Optional[dict[str, Any]] = None
) -> UserCertificate:
    """
    Updates an existing issued certificate (user_cert record) in the database.

    Args:
        db (Session): The active database session.
        user_cert_id (int): The ID of the user certificate record to update.
        user_id (Optional[int]): New user ID, if provided.
        cert_id (Optional[int]): New certificate ID, if provided.
        issued_on (Optional[datetime]): New issue date, if provided.
        expires_on (Optional[datetime]): New expiration date, if provided.
        additional_info (Optional[dict[str, Any]]): New JSON metadata, if provided.

    Returns:
        UserCertificate: The updated UserCertificate object.

    Raises:
        ValueError: If the user certificate record does not exist, or if a new cert_id is provided and that certificate doesn't exist.
    """
    # Query the user certificate record by id
    user_cert = db.query(UserCertificate).filter(UserCertificate.id == user_cert_id).first()
    if not user_cert:
        raise ValueError(f"UserCertificate with id {user_cert_id} does not exist!")
    
    new_cert = None
    if cert_id is not None:
        # Verify the certificate exists
        cert = db.query(Certificate).filter(Certificate.id == cert_id).first()
        if not cert:
            raise ValueError(f"Certificate with id {cert_id} does not exist!")
        user_cert.cert_id = cert_id

    if user_id is not None:
        user_cert.user_id = user_id
    if issued_on is not None: 
        user_cert.issued_on = issued_on
    if expires_on is not None:
        user_cert.expires_on = expires_on
    else:
        # If expires_on is not provided and cert_id is updated (or new_cert exists)
        # and issued_on is available, compute the expiration based on new certificate's years_valid.
        if new_cert and user_cert.issued_on and new_cert.years_valid:
            user_cert.expires_on = user_cert.issued_on + relativedelta(years=new_cert.years_valid)

    if additional_info is not None:
        user_cert.additional_info = additional_info

    db.commit()
    db.refresh(user_cert)

    # Debug logs
    print(f"✅ Updated UserCertificate ID: {user_cert.id}")
    print(f"📜 New attributes: {vars(user_cert)}")
    
    return user_cert


