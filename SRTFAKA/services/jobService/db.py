import sqlite3
from datetime import datetime
import os
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, mapped_column, relationship, Mapped, DeclarativeBase
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
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default= datetime.now())
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    available_spot_count: Mapped[int] = mapped_column(Integer, nullable=False)
    monthly_salary: Mapped[int] = mapped_column(Integer, nullable=False)
    
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
    