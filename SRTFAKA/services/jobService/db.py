import sqlite3
from datetime import datetime
import os
from typing import Optional, List
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, mapped_column, relationship, Mapped, DeclarativeBase, Session, Mapped
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from ...apiGateway.base import Base, Industry, Country
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
    monthly_salary: Mapped[Optional[int]] = mapped_column(Integer, nullable=False) 
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default= datetime.now())
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    available_spot_count: Mapped[int] = mapped_column(Integer, nullable=False)
    monthly_salary: Mapped[int] = mapped_column(Integer, nullable=False)
    
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

        industry_id = self.get_company_industry_id(job_data["company_id"])
    
        if industry_id is None:
            print(f"ERROR: No industry found for company_id {job_data['company_id']}")
            return None
    
        sql = text("""
        INSERT INTO job_listing (
                   name, 
                   description, 
                   monthly_salary, 
                   start_date, 
                   end_date, 
                   available_spot_count, 
                   company_id, 
                   employment_type_id) 
        VALUES (
                   :name, 
                   :description, 
                   :monthly_salary, 
                   :start_date, 
                   :end_date, 
                   :available_spot_count, 
                   :company_id, 
                   :employment_type_id
                )
                RETURNING id;
                   """)
        values = {
            "name": job_data["name"],
            "description": job_data["description"],
            "monthly_salary": job_data["monthly_salary"],
            "start_date": job_data["start_date"],
            "end_date": job_data["end_date"],
            "available_spot_count": job_data["available_spot_count"],
            "company_id": job_data["company_id"],
            "employment_type_id": job_data["employment_type_id"],
    }

        try:
            result = self.session.execute(sql, values)
            self.session.commit()
            job_id = result.scalar()  # Retrieve the generated job ID

            if job_id:
                # Retrieve company and industry names
                company_name = self.get_company_name(job_data["company_id"])
                industry_name = self.get_industry_name(industry_id)
                employment_value = self.get_employment_value(job_data["employment_type_id"])

                return {
                    "job_id": job_id,
                    "name": job_data["name"],
                    "description": job_data["description"],
                    "monthly_salary": job_data["monthly_salary"],
                    "start_date": job_data["start_date"],
                    "end_date": job_data["end_date"],
                    "available_spot_count": job_data["available_spot_count"],
                    "company_id": job_data["company_id"],
                    "company_name": company_name,
                    "employment_type_id": job_data["employment_type_id"],
                    "employment_value": employment_value,
                    "industry_id": industry_id,
                    "industry_name": industry_name
                }
            return None

        except SQLAlchemyError as e:
            print(f"ERROR in create_job: {e}")
            self.session.rollback()
            return None


    def update_job(self, job_id: int, update_data: dict) -> Optional[dict]:
        """Update an existing job listing using raw SQL in PostgreSQL."""

        # Allowed fields that employers can update
        allowed_fields = {"name", "description", "start_date", "end_date", "available_spot_count", "employment_type_id"}
        update_data = {key: value for key, value in update_data.items() if key in allowed_fields}

        if not update_data:
            print(f"ERROR in update_job: No valid update fields provided.")
            return None

        # Check if job exists
        check_sql = text("SELECT id FROM job_listing WHERE id = :job_id")
        result = self.session.execute(check_sql, {"job_id": job_id}).fetchone()
        
        if not result:
            print(f"ERROR in update_job: Job ID {job_id} not found.")
            return None

        # Generate dynamic SET clause for SQL update
        updates = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
        sql = text(f"""
            UPDATE job_listing 
            SET {updates}
            WHERE id = :job_id
            RETURNING id, name, description, start_date, end_date, available_spot_count, company_id, employment_type_id, monthly_salary;
        """)

        update_data["job_id"] = job_id  # Add job_id to the parameter dictionary

        try:
            result = self.session.execute(sql, update_data)
            self.session.commit()
            updated_job = result.fetchone()

            if updated_job:
                # Retrieve company and industry names
                company_name = self.get_company_name(updated_job.company_id)
                industry_id = self.get_company_industry_id(updated_job.company_id)
                industry_name = self.get_industry_name(industry_id)
                employment_value = self.get_employment_value(updated_job.employment_type_id)

                updated_job_data = {
                    "job_id": updated_job.id,
                    "name": updated_job.name,
                    "description": updated_job.description,
                    "start_date": updated_job.start_date.strftime("%Y-%m-%d"),
                    "end_date": updated_job.end_date.strftime("%Y-%m-%d"),
                    "available_spot_count": updated_job.available_spot_count,
                    "company_id": updated_job.company_id,
                    "company_name": company_name,
                    "employment_type_id": updated_job.employment_type_id, 
                    "employment_value": employment_value,  
                    "industry_id": industry_id,
                    "industry_name": industry_name,
                    "monthly_salary": updated_job.monthly_salary
                }

                print(f"DEBUG: Job Updated Successfully - {updated_job_data}")
                return updated_job_data

            print(f"ERROR: Update failed for job_id={job_id}")
            return None

        except SQLAlchemyError as e:
            print(f"ERROR in update_job: {e}")
            self.session.rollback()
            return None


        
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
                    employment_type.id AS employment_type_id,
                    employment_type.value AS employment_value,
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
        sql = text("""
            SELECT 
                job_listing.id AS job_id,
                job_listing.name AS job_name,
                job_listing.description,
                job_listing.monthly_salary,
                job_listing.start_date,
                job_listing.end_date,
                job_listing.available_spot_count, 
                company.id AS company_id,    
                company.name AS company_name, 
                employment_type.id AS employment_type_id,
                employment_type.value AS employment_value,
                company.industry_id AS industry_id,      
                industry.name AS industry_name
            FROM job_listing
            JOIN company ON job_listing.company_id = company.id
            JOIN employment_type ON job_listing.employment_type_id = employment_type.id
            JOIN industry ON company.industry_id = industry.id
            WHERE job_listing.id = :job_id
        """)

        try:
            print(f"DEBUG: Fetching job details for job_id={job_id}")
            
            result = self.session.execute(sql, {"job_id": job_id})
            job = result.fetchone()

            if job:
                job_details = {
                    "job_id": job.job_id,
                    "job_name": job.job_name,
                    "description": job.description,
                    "monthly_salary": job.monthly_salary,
                    "start_date": job.start_date.strftime("%Y-%m-%d"),
                    "end_date": job.end_date.strftime("%Y-%m-%d"),
                    "available_spot_count": job.available_spot_count,
                    "company_id": job.company_id,
                    "company_name": job.company_name,
                    "employment_type_id": job.employment_type_id,
                    "employment_value": job.employment_value,
                    "industry_id": job.industry_id,
                    "industry_name": job.industry_name
                }

                print(f"DEBUG: Job Details Retrieved: {job_details}")
                return job_details

            print(f"ERROR: No job found for job_id={job_id}")
            return None

        except SQLAlchemyError as e:
            print(f"ERROR in get_job_details: {e}")
            return None



    def delete_job(self, job_id: int) -> bool:
        """Delete a job by jobId using raw SQL."""
        sql = text("DELETE FROM job_listing WHERE id = :job_id")

        try:
            result = self.session.execute(sql, {"job_id": job_id})
            self.session.commit()
            return result.rowcount > 0  # True if a row was deleted
        except SQLAlchemyError as e:
            print(f"ERROR in delete_job: {e}")
            self.session.rollback()
            return False

    
    def get_company_name(self, company_id: int) -> str:
        """Retrieve company name based on company ID."""
        sql = "SELECT name FROM company WHERE id = :company_id"
        result = self.session.execute(text(sql), {"company_id": company_id}).fetchone()
        return result[0] if result else "Unknown"
    
    def get_company_industry_id(self, company_id: int) -> Optional[int]:
        """Retrieve the industry ID of a company based on the company ID."""
        sql = text("SELECT industry_id FROM company WHERE id = :company_id")
        result = self.session.execute(sql, {"company_id": company_id}).fetchone()
        return result[0] if result else None


    def get_industry_name(self, industry_id: int) -> str:
        """Retrieve industry name based on industry ID."""
        sql = "SELECT name FROM industry WHERE id = :industry_id"
        result = self.session.execute(text(sql), {"industry_id": industry_id}).fetchone()
        return result[0] if result else "Unknown"
    
    def get_employment_value(self, employment_type_id: int) -> str:
        """Retrieve employment type value based on employment type ID."""
        sql = text("SELECT value FROM employment_type WHERE id = :employment_type_id")
        result = self.session.execute(sql, {"employment_type_id": employment_type_id}).fetchone()
        return result[0] if result else "Unknown"

    def apply_job(self, applicant_id: int, job_id: int, resume_link: str, additional_info: Optional[str] = None) -> Optional[int]:
        """Allows a user to apply for a job using raw SQL."""

        print(f"DEBUG: Entering apply_job() - Received applicant_id={applicant_id}, job_id={job_id}")

        if applicant_id == 0:
            print(f"ERROR: Invalid applicant_id received: {applicant_id}")
            return None

        # Retrieve company_id from job listing
        sql_get_company = text("SELECT company_id FROM job_listing WHERE id = :job_id")
        result = self.session.execute(sql_get_company, {"job_id": job_id}).fetchone()

        if not result:
            print(f"ERROR in apply_job: Job ID {job_id} not found.")
            return None

        company_id = result[0]

        # Retrieve industry_id from company_id
        industry_id = self.get_company_industry_id(company_id)

        if industry_id is None:
            print(f"ERROR in apply_job: No industry found for company_id {company_id}")
            return None
        
        print(f"DEBUG: Applying job with applicant_id={applicant_id}")

        # Insert the job application
        sql_insert = text("""
            INSERT INTO application (applicant_id, listing_id, resume_link, additional_info, applied_on, status, industry_id) 
            VALUES (:applicant_id, :job_id, :resume_link, :additional_info, :applied_on, :status, :industry_id)
            RETURNING id;
        """)

        values = {
            "applicant_id": int(applicant_id),
            "job_id": job_id,
            "resume_link": resume_link,
            "additional_info": additional_info or "",
            "applied_on": datetime.now(),
            "status": "Submitted",  # Default status for new applications
            "industry_id": industry_id 
        }

        print(f"DEBUG: Final SQL Values = {values}")  # Print final values before insertion

        try:
            result = self.session.execute(sql_insert, values)
            self.session.commit()
            return result.scalar()  # Return the newly inserted application ID
        except SQLAlchemyError as e:
            print(f"ERROR in apply_job: {e}")
            self.session.rollback()
            return None

    def get_applications_by_user(self, applicant_id: int) -> List[dict]:
        """Retrieve job applications for a specific user with additional details."""
        sql = text("""
            SELECT 
                application.id AS application_id,
                CONCAT(COALESCE("user".first_name, ''), ' ', COALESCE("user".last_name, '')) AS applicant_name,  
                application.applicant_id,
                job_listing.id AS job_id,
                job_listing.name AS job_name,
                company.id AS company_id,
                company.name AS company_name,
                industry.id AS industry_id,
                industry.name AS industry_name,
                employment_type.value AS employment_value,
                application.applied_on,
                application.resume_link,
                application.additional_info,
                application.status
            FROM application
            JOIN job_listing ON application.listing_id = job_listing.id
            JOIN company ON job_listing.company_id = company.id
            JOIN industry ON company.industry_id = industry.id
            JOIN employment_type ON job_listing.employment_type_id = employment_type.id
            JOIN "user" ON application.applicant_id = "user".id  
            WHERE application.applicant_id = :applicant_id
            ORDER BY application.applied_on DESC;
        """)

        try:
            print(f"DEBUG: Fetching applications for applicant_id={applicant_id}")
            result = self.session.execute(sql, {"applicant_id": applicant_id})
            rows = result.fetchall()

            applications = [
                {
                    "application_id": row.application_id,
                    "applicant_id": row.applicant_id,
                    "applicant_name": row.applicant_name, 
                    "job_id": row.job_id,
                    "job_name": row.job_name,
                    "company_id": row.company_id,
                    "company_name": row.company_name,
                    "industry_id": row.industry_id,
                    "industry_name": row.industry_name,
                    "employment_value": row.employment_value,
                    "applied_on": row.applied_on.strftime("%Y-%m-%d %H:%M:%S"),
                    "resume_link": row.resume_link,
                    "additional_info": row.additional_info or "",
                    "status": row.status
                }
                for row in rows
            ]

            print(f"DEBUG: Applications Retrieved: {len(applications)} for applicant_id={applicant_id}")
            return applications

        except SQLAlchemyError as e:
            print(f"ERROR in get_applications_by_user: {e}")
            return []




    def get_application_details(self, application_id: int) -> Optional[dict]:
        """Retrieve full details of a specific job application using raw SQL."""
        sql = text("""
            SELECT 
                application.id AS application_id,
                application.applicant_id,
                CONCAT(COALESCE("user".first_name, ''), ' ', COALESCE("user".last_name, '')) AS applicant_name,  
                job_listing.id AS job_id,
                job_listing.name AS job_name,
                company.id AS company_id,
                company.name AS company_name,  
                industry.id AS industry_id,
                industry.name AS industry_name, 
                employment_type.value AS employment_value,  
                application.applied_on,
                application.resume_link,
                application.additional_info,
                application.status
            FROM application
            JOIN job_listing ON application.listing_id = job_listing.id
            JOIN company ON job_listing.company_id = company.id
            JOIN industry ON company.industry_id = industry.id
            JOIN employment_type ON job_listing.employment_type_id = employment_type.id
            JOIN "user" ON application.applicant_id = "user".id 
            WHERE application.id = :application_id
        """)

        try:
            print(f"DEBUG: Fetching application details for application_id={application_id}")
            
            result = self.session.execute(sql, {"application_id": application_id})
            application = result.fetchone()

            if application:
                application_details = {
                    "application_id": application.application_id,
                    "applicant_id": application.applicant_id,
                    "applicant_name": application.applicant_name, 
                    "job_id": application.job_id,
                    "job_name": application.job_name,
                    "company_id": application.company_id,
                    "company_name": application.company_name,  
                    "industry_id": application.industry_id,
                    "industry_name": application.industry_name, 
                    "employment_value": application.employment_value, 
                    "applied_on": application.applied_on.strftime("%Y-%m-%d %H:%M:%S"),
                    "resume_link": application.resume_link,
                    "additional_info": application.additional_info or "",
                    "status": application.status
                }

                print(f"DEBUG: Application Details Retrieved: {application_details}")
                return application_details

            print(f"ERROR: No application found for application_id={application_id}")
            return None

        except SQLAlchemyError as e:
            print(f"ERROR in get_application_details: {e}")
            return None


    def close(self):
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()
