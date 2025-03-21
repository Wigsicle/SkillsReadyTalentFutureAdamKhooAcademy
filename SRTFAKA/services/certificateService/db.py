import sqlite3
from datetime import datetime
import os
from typing import Optional, Any, TYPE_CHECKING
from sqlalchemy.orm import sessionmaker, mapped_column, relationship, Mapped, DeclarativeBase, Session
from sqlalchemy import Integer, String, DateTime, ForeignKey, Time, JSON, Date, JSON, create_engine
from sqlalchemy.ext.hybrid import hybrid_property
from apiGateway.base import Base
from dateutil.relativedelta import relativedelta

# Database Connection
DATABASE_URL = "postgresql+psycopg2://postgres:password@127.0.0.1:5433/academy_db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Return the session for use
    finally:
        db.close()  # Ensure session is closed


if TYPE_CHECKING:
    from services.courseService.db import Course
    from services.accountService.db import User

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

    course: Mapped["Course"] = relationship("Course", back_populates='certificate')
    issued_certs: Mapped["UserCertificate"] = relationship("UserCertificate", back_populates='cert_info')
    
class UserCertificate(Base):
    __tablename__ = 'user_cert'
    id: Mapped[int] = mapped_column(primary_key=True)
    issued_on: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expires_on: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    additional_info: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True)
    
    #FK
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=True)    # Use this to access user obj
    cert_id: Mapped[int] = mapped_column(Integer, ForeignKey('certificate.id'), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates='certs_attained')
    cert_info: Mapped["Certificate"] = relationship("Certificate", back_populates='issued_certs')
    
    
currentPath = os.path.dirname(os.path.abspath(__file__))
class CertificateDB:
    def __init__(self):
        # SQLite database file
        db_path = currentPath + '/certificates.db'
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Access rows as dictionaries
        self.cursor = self.conn.cursor()

        # SQL to create certificates table
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS certificates (
            certificateId TEXT PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            courseId TEXT NOT NULL
        )
        '''
        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            print("Table 'certificates' created successfully.")
        except sqlite3.Error as e:
            print(f"Database error during table creation: {e}")
            self.conn.rollback()
    
    def createCertificate(self, certificateObj):
        """Insert a new certificate into the database."""
        sql = '''INSERT INTO certificates (certificateId, name, courseId) 
                 VALUES (?, ?, ?)'''
        try:
            self.cursor.execute(sql, certificateObj)
            self.conn.commit()
            return certificateObj[0]  # Return created certificate ID
        except sqlite3.Error as e:
            print(f"Database error during createCertificate: {e}")
            self.conn.rollback()
            return False

    def updateCertificate(self, certificateObj):
        """Update the amount of an existing certificate by certificateId."""
        sql = '''UPDATE certificates
                 SET name = ?, courseId=?
                 WHERE certificateId = ?'''
        try:
            self.cursor.execute(sql, (certificateObj['name'], certificateObj['courseId'], certificateObj['certificateId']))
            self.conn.commit()
            return self.cursor.rowcount  # Number of rows affected
        except sqlite3.Error as e:
            print(f"Database error during updateCertificate: {e}")
            self.conn.rollback()
            return False

    def getAllCertificate(self):
        try:
            sql = '''SELECT * FROM certificates'''
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            if not rows:
                return None

            # Convert rows to a list of dictionaries with ISO 8601 timestamp strings
            certificates = []
            for row in rows:
                row_dict = dict(row)
                certificates.append(row_dict)
            # sorted_rows = sorted(rows, key=lambda row: datetime.strptime(row['transactionDate'], "%d/%m/%Y"))
            return certificates
        except sqlite3.Error as e:
            print(f"Database error during getCertificate: {e}")
            return False
        
    def getCertificate(self, name=None, courseId=None):
        try:
            # Start SQL query and parameters list
            sql = "SELECT * FROM certificates WHERE 1=1"
            params = []

            # Dynamic conditions based on provided filters
            if name:
                sql += " AND name = ?"
                params.append(name)
            
            if courseId:
                sql += " AND courseId = ?"
                params.append(courseId)
        
            
            # Execute the query
            self.cursor.execute(sql, tuple(params))
            rows = self.cursor.fetchall()

            # If no rows found, return None
            if not rows:
                return None

            # Convert rows to a list of dictionaries
            certificates = []
            for row in rows:
                row_dict = dict(row)
                certificates.append(row_dict)

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


