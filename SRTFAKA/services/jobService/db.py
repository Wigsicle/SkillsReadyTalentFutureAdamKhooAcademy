import sqlite3
from datetime import datetime
import os
from typing import Optional, List
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, mapped_column, relationship, Mapped, DeclarativeBase, Session, Mapped
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from SRTFAKA.apiGateway.base import Base, Industry, Country
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

indFKey = 'industry.id' #PK of Industry Table
engine = create_engine("postgresql+psycopg2://postgres:password@127.0.0.1:5433/academy_db")
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class EmploymentType(Base):
    """Full-Time/Part-Time/Intern"""
    __tablename__ = "employment_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String(255), nullable=False)
    short_val: Mapped[str] = mapped_column(String(255), nullable=False)

class Company(Base):
    __tablename__ = "company"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)

    #FK
    industry_id: Mapped[int] = mapped_column(Integer, ForeignKey(indFKey))
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey('country.id'))

    listed_jobs: Mapped[list['JobListing']] = relationship("JobListing", foreign_keys='job_listing.company_id', back_populates="company")
    industry: Mapped[Industry] = relationship(foreign_keys=indFKey)
    country: Mapped[Country] = relationship("Country", foreign_keys='country.id')

class JobListing(Base):
    '''
    Stores the value of a single job listing.

    Attributes
    ----------
    name : str
        name of job listing

    '''
    __tablename__ = "job_listing"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    monthly_salary: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) 
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default= datetime.now())
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    available_spot_count: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # FK dependency
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey('company.id'), nullable=False)
    employment_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('employment_type.id'), nullable=False) # FT/PT/Intern

    # Object Relations with Company and Applications
    company: Mapped[Company] = relationship('Company', back_populates='listed_jobs')
    employment: Mapped[EmploymentType] = relationship('EmploymentType', foreign_keys='employment_type.id')
    applications: Mapped[list['Application']] = relationship('Application', back_populates='listing')

    @hybrid_property
    def available_status(self)->Mapped[bool]:
        """
        Status of job listing based on end_date value not exceeding current DT, 
        Available = True, Not Available = False
        """
        return (self.end_date < datetime.now())
    
    @hybrid_property
    def applicant_count(self)->Mapped[int]:
        return self.applications.count
    
    @hybrid_property
    def country_name(self)->Mapped[str]:
        return self.company.country.name
    
    @hybrid_property
    def industry_name(self)->Mapped[str]:
        return self.company.industry.name

class Application(Base):
    '''
    Stores details of user job application. 
    '''
    __tablename__ = "application"

    id: Mapped[int] = mapped_column(primary_key=True)
    applied_on: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())  # if empty automatically assign right now
    edited_on: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    resume_link: Mapped[str] = mapped_column(String(255), nullable=False)
    additional_info: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(255), nullable=False, default="Submitted") # Submitted/Under-Review/Accepted

    # FK dependency
    applicant_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    listing_id: Mapped[int] = mapped_column(Integer, ForeignKey('job_listing.id'), nullable=False)
    industry_id: Mapped[int] = mapped_column(Integer, ForeignKey(indFKey))

    #applicant: Mapped[User] = relationship(back_populates='applications')
    listing: Mapped[JobListing] = relationship('JobListing', back_populates='applications')
    industry: Mapped[Industry] = relationship('Industry', foreign_keys=indFKey)
    


#============ Job DB Class ===================
currentPath = os.path.dirname(os.path.abspath(__file__))
class JobDB:
    def __init__(self):
        """Initialize the database connection."""
        self.session = SessionLocal()
    
    def create_job(self, job_data: dict) -> Optional[int]:
        """Insert a new job into the database using raw SQL."""
        sql = """
        INSERT INTO job_listing (name, description, monthly_salary, start_date, end_date, available_spot_count, company_id, employment_type_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            job_data["name"],
            job_data["description"],
            job_data["monthly_salary"],
            job_data["start_date"],
            job_data["end_date"],
            job_data["available_spot_count"],
            job_data["company_id"],
            job_data["employment_type_id"],
        )

        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
            return self.cursor.lastrowid  # Return created job ID
        except sqlite3.Error as e:
            print(f"ERROR in create_job: {e}")
            self.conn.rollback()
            return None



    def update_job(self, job_id: int, update_data: dict) -> bool:
        """Update an existing job listing using raw SQL."""
        sql = "UPDATE job_listing SET "
        updates = []
        values = []

        for key, value in update_data.items():
            updates.append(f"{key} = ?")
            values.append(value)

        sql += ", ".join(updates)
        sql += " WHERE id = ?"
        values.append(job_id)

        try:
            self.cursor.execute(sql, tuple(values))
            self.conn.commit()
            return self.cursor.rowcount > 0  # True if at least one row was updated
        except sqlite3.Error as e:
            print(f"ERROR in update_job: {e}")
            self.conn.rollback()
            return False

        
    def get_job(self):
        """Retrieve all job listings using raw SQL."""
        try:
            sql = text("""
            SELECT 
                    job_listing.id,
                    job_listing.name,
                    job_listing.description,
                    job_listing.monthly_salary,
                    job_listing.start_date,
                    job_listing.end_date,
                    job_listing.available_spot_count, 
                    company.id AS company_id,    
                    company.name AS company_name, 
                    employment_type.id,
                    company.industry_id as industry_id,      
                    industry.name AS industry_name
            FROM job_listing
            JOIN company ON job_listing.company_id = company.id
            JOIN employment_type ON job_listing.employment_type_id = employment_type.id
            JOIN industry ON company.industry_id = industry.id
            """)
            
            print(f"DEBUG: Running SQL Query:\n{sql}")  # Debugging Step
            
            result = self.session.execute(sql)
            rows = result.fetchall()
            
            print(f"DEBUG: Jobs Retrieved: {len(rows)}")  # Debugging Step

            return rows
        except SQLAlchemyError as e:
            print(f"ERROR in get_job: {e}")
            return []


    def get_total_jobs_count(self) -> int:
        """Returns the total number of job listings using raw SQL."""
        try:
            sql = "SELECT COUNT(*) FROM job_listing"
            self.cursor.execute(sql)
            count = self.cursor.fetchone()[0]
            return count
        except sqlite3.Error as e:
            print(f"ERROR in get_total_jobs_count: {e}")
            return 0


    def get_job_details(self, job_id: int) -> Optional[dict]:
        """Retrieve full job details using raw SQL."""
        sql = """
        SELECT job_listing.id, job_listing.name, job_listing.description, company.name, employment_type.value,
        FROM job_listing
        JOIN company ON job_listing.company_id = company.id
        JOIN employment_type ON job_listing.employment_type_id = employment_type.id
        WHERE job_listing.id = ?
        """
        try:
            self.cursor.execute(sql, (job_id,))
            job = self.cursor.fetchone()
            if job:
                return dict(job)  # Convert to dictionary
            return None
        except sqlite3.Error as e:
            print(f"ERROR in get_job_details: {e}")
            return None


    def delete_job(self, job_id: int) -> bool:
        """Delete a job by jobId using raw SQL."""
        sql = "DELETE FROM job_listing WHERE id = ?"

        try:
            self.cursor.execute(sql, (job_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0  # True if a row was deleted
        except sqlite3.Error as e:
            print(f"ERROR in delete_job: {e}")
            self.conn.rollback()
            return False

        
    def apply_job(self, applicant_id: int, job_id: int, resume_link: str, additional_info: Optional[str] = None) -> Optional[int]:
        """Allows a user to apply for a job using raw SQL."""
        sql = """
        INSERT INTO application (applicant_id, listing_id, resume_link, additional_info, applied_on) 
        VALUES (?, ?, ?, ?, ?)
        """
        values = (applicant_id, job_id, resume_link, additional_info or "", datetime.now())

        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"ERROR in apply_job: {e}")
            self.conn.rollback()
            return None

        
    def get_application_details(self, application_id: int) -> Optional[dict]:
        """Retrieve full details of a specific job application using raw SQL."""
        sql = """
        SELECT application.id, user.id AS applicant_id, job_listing.id AS job_id, 
            application.resume_link, application.additional_info, application.applied_on
        FROM application
        JOIN user ON application.applicant_id = user.id
        JOIN job_listing ON application.listing_id = job_listing.id
        WHERE application.id = ?
        """
        try:
            self.cursor.execute(sql, (application_id,))
            application = self.cursor.fetchone()
            if application:
                return dict(application)  # Convert result into a dictionary
            return None
        except sqlite3.Error as e:
            print(f"ERROR in get_application_details: {e}")
            return None

    def close(self):
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()
