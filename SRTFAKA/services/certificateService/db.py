import sqlite3
from datetime import datetime
import os
from typing import Optional, Any, TYPE_CHECKING
from sqlalchemy.orm import sessionmaker, mapped_column, relationship, Mapped, DeclarativeBase
from sqlalchemy import Integer, String, DateTime, ForeignKey, Time, JSON, Date
from sqlalchemy.ext.hybrid import hybrid_property
from apiGateway.base import Base

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
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)    # Use this to access user obj
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
        
        except sqlite3.Error as e:
            print(f"Database error during getCertificate: {e}")
            return False

    def deleteCertificate(self, certificateId):
        """Delete an certificate by certificateId."""
        sql = '''DELETE FROM certificates WHERE certificateId = ?'''
        try:
            self.cursor.execute(sql, (certificateId,))
            self.conn.commit()
            return self.cursor.rowcount  # Number of rows affected
        except sqlite3.Error as e:
            print(f"Database error during deleteCertificate: {e}")
            self.conn.rollback()
            return False

    def close(self):
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()
