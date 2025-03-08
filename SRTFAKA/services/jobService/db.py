import sqlite3
from datetime import datetime
import os
from typing import Optional, List
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, mapped_column, relationship, Mapped, DeclarativeBase, Session, Mapped
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from apiGateway.base import Base, Industry, Country

indFKey = 'industry.id' #PK of Industry Table
engine = create_engine("postgresql+psycopg2://postgres:password@127.0.0.1:5433/academy_db")

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
    pay: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # FK dependency
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey('company.id'), nullable=False)
    employment_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('employment_type.id'), nullable=False) # FT/PT/Intern

    # Object Relations with Company and Applications
    company: Mapped[Company] = relationship('Company', back_populates='listed_jobs')
    employment: Mapped[EmploymentType] = relationship('Relationship', foreign_keys='employment_type.id')
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
        """Initialize the database session."""
        self.engine = engine
        self.session = SessionLocal()
    
    def create_job(self, job_data: dict) -> Optional[int]:
        """Insert a new job into the database."""
        try:
            new_job = JobListing(
                name=job_data["name"],
                description=job_data["description"],
                monthly_salary=job_data["monthly_salary"],
                start_date=job_data["start_date"],
                end_date=job_data["end_date"],
                available_spot_count=job_data["available_spot_count"],
                company_id=job_data["company_id"],
                employment_type_id=job_data["employment_type_id"],
            )
            self.session.add(new_job)
            self.session.commit()
            return new_job.listing_id
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Database error during create_job: {e}")
            return None

    def update_job(self, job_id: int, update_data: dict) -> bool:
        """Update an existing job listing."""
        try:
            job = self.session.get(JobListing, job_id)
            if not job:
                return False
            
            for key, value in update_data.items():
                setattr(job, key, value)
            
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Database error during update_job: {e}")
            return False
        
    def get_job(
        self,
        country: Optional[str] = None,
        company_name: Optional[str] = None,
        industry_name: Optional[str] = None,
        employment_type: Optional[str] = None,
        min_salary: Optional[int] = None,
        max_salary: Optional[int] = None
    ) -> List[JobListing]:
        """Retrieve jobs filtered by country, company, industry, employment type, and salary range."""
        try:
            query = self.session.query(JobListing).join(Company).join(EmploymentType).join(Industry).join(Country)

            if country:
                query = query.filter(Country.name == country)
            if company_name:
                query = query.filter(Company.name == company_name)
            if industry_name:
                query = query.filter(Industry.name == industry_name)
            if employment_type:
                query = query.filter(EmploymentType.value == employment_type)
            if min_salary:
                query = query.filter(JobListing.monthly_salary >= min_salary)
            if max_salary:
                query = query.filter(JobListing.monthly_salary <= max_salary)

            # Only return jobs that are still available (status == True)
            query = query.filter(JobListing.status == True)

            return query.order_by(JobListing.start_date.desc()).all()
        
        except SQLAlchemyError as e:
            print(f"Database error during get_jobs: {e}")
            return []

    def get_total_jobs_count(self) -> int:
        """Returns the total number of job listings."""
        try:
            return self.session.query(JobListing).count()
        except SQLAlchemyError as e:
            print(f"Database error during get_total_jobs_count: {e}")
            return 0

    def get_job_details(self, job_id: int) -> Optional[JobListing]:
        """
        Retrieve full job details when a user clicks on a job.

        :param job_id: The ID of the job.
        :return: The job details or None if not found.
        """
        try:
            job = (
                self.session.query(JobListing)
                .join(Company)
                .join(Industry)
                .join(Country)
                .join(EmploymentType)
                .filter(JobListing.listing_id == job_id)
                .first()
            )

            return job

        except SQLAlchemyError as e:
            print(f"Database error during get_job_details: {e}")
            return None


    def delete_job(self, job_id: int) -> bool:
        """Delete a job by jobId."""
        try:
            job = self.session.get(JobListing, job_id)
            if not job:
                return False
            
            self.session.delete(job)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Database error during delete_job: {e}")
            return False
        
    def apply_job(
        self,
        applicant_id: int,
        job_id: int,
        resume_link: str,
        additional_info: Optional[str] = None
    ) -> Optional[int]:
        """
        Allows a user to apply for a specific job.
        Prevents duplicate applications.
        """
        try:
            # Check if the job exists and is still available
            job = self.session.get(JobListing, job_id)
            if not job:
                print(f"Error: Job ID {job_id} does not exist.")
                return None
            if not job.status:
                print(f"Error: Job ID {job_id} is no longer available.")
                return None

            # Prevent duplicate applications
            existing_application = (
                self.session.query(Application)
                .filter(Application.applicant_id == applicant_id, Application.listing_id == job_id)
                .first()
            )
            if existing_application:
                print("Error: User has already applied for this job.")
                return None

            # Create a new application
            new_application = Application(
                applicant_id=applicant_id,
                listing_id=job_id,
                resume_link=resume_link,
                additional_info=additional_info,
                applied_on=datetime.now()
            )

            # Add to session and commit
            self.session.add(new_application)
            self.session.commit()
            
            return new_application.id  # Return the application ID

        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Database error during apply_for_job: {e}")
            return None

            
    def get_applications(self, applicant_id: int) -> List[Application]:
        """
        Retrieve all job applications submitted by a user.
        
        :param applicant_id: The ID of the user.
        :return: A list of job applications.
        """
        try:
            applications = (
                self.session.query(Application)
                .join(JobListing)
                .join(Company)
                .filter(Application.applicant_id == applicant_id)
                .all()
            )

            return applications

        except SQLAlchemyError as e:
            print(f"Database error during get_applications_by_user: {e}")
            return []
        
    def get_application_details(self, application_id: int) -> Optional[Application]:
        """
        Retrieve full details of a specific job application.
        
        :param application_id: The ID of the application.
        :return: The application details or None if not found.
        """
        try:
            application = (
                self.session.query(Application)
                .join(JobListing)
                .join(Company)
                .join(Industry)
                .filter(Application.id == application_id)
                .first()
            )

            return application

        except SQLAlchemyError as e:
            print(f"Database error during get_application_details: {e}")
            return None

    """ If user is allowed to withdraw their application, uncomment this function """
    # def withdraw_application(self, application_id: int, applicant_id: int) -> bool:
    #     """
    #     Allows a user to withdraw (delete) a job application.
        
    #     :param application_id: The ID of the application to be withdrawn.
    #     :param applicant_id: The ID of the user (to prevent unauthorized deletion).
    #     :return: True if successful, False otherwise.
    #     """
    #     try:
    #         application = self.session.query(Application).filter(
    #             Application.id == application_id, Application.applicant_id == applicant_id
    #         ).first()

    #         if not application:
    #             print("Application not found or user is unauthorized.")
    #             return False

    #         self.session.delete(application)
    #         self.session.commit()
    #         return True

    #     except SQLAlchemyError as e:
    #         self.session.rollback()
    #         print(f"Database error during withdraw_application: {e}")
    #         return False

    def close(self):
        """Close the database session."""
        self.session.close()
