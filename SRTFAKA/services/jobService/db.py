import sqlite3
from datetime import datetime
import os
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, mapped_column, relationship, Mapped, DeclarativeBase
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from ...apiGateway.base import Base, Industry, Country
from ...accountService.db import User

engine = create_engine("postgresql+psycopg2://postgres:password@127.0.0.1:5433/academy_db")

class EmploymentType(Base):
    """Full-Time/Part-Time/Intern"""
    __tablename__ = "employment_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String(255), nullable=False)
    short_val: Mapped[str] = mapped_column(String(255), nullable=False)

class Company(Base):
    __tablename__ = "company"
    company_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)

    #FK
    industry_id: Mapped[int] = mapped_column(Integer, ForeignKey='industry.id')
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey='country_id')

    listed_jobs: Mapped[list['JobListing']] = relationship("JobListing", foreign_keys='job_listing.company_id', back_populates="company")
    industry: Mapped[Industry] = relationship(foreign_keys='industry.id')
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

    listing_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default= datetime.now())
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    available_spot_count: Mapped[int] = mapped_column(Integer, nullable=False)
    pay: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # FK dependency
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey('company.company_id'), nullable=False)
    employment_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('employment_type.id', nullable=False)) # FT/PT/Intern

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
    Stores details of user job application. Retrieve by applicant_id field (user_id)
    '''
    __tablename__ = "application"

    id: Mapped[int] = mapped_column(primary_key=True)
    applicant_id: Mapped[int] = mapped_column(Integer, nullable=False) # MUST ensure write consistency with User DB, let APIGate handle
    applied_on: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())  # if empty automatically assign right now
    edited_on: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    resume_link: Mapped[str] = mapped_column(String(255), nullable=False)
    additional_info: Mapped[str] = mapped_column(String(255), nullable=True)

    # FK dependency
    listing_id: Mapped[int] = mapped_column(Integer, ForeignKey('job_listing.listing_id'), nullable=False)

    listing: Mapped[JobListing] = relationship('JobListing', back_populates='applications')
    applicant: Mapped[User] = relationship('User', back_populates='applications')


currentPath = os.path.dirname(os.path.abspath(__file__))
class JobDB:
    def __init__(self):
        # SQLite database file
        db_path = currentPath + '/jobs.db'
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Access rows as dictionaries
        self.cursor = self.conn.cursor()

        # SQL to create jobs table
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS jobs (
            jobId TEXT PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            company TEXT NOT NULL
        )
        '''
        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            print("Table 'jobs' created successfully.")
        except sqlite3.Error as e:
            print(f"Database error during table creation: {e}")
            self.conn.rollback()
    
    def createJob(self, jobObj):
        """Insert a new job into the database."""
        sql = '''INSERT INTO jobs (jobId, name, company) 
                 VALUES (?, ?, ?)'''
        try:
            self.cursor.execute(sql, jobObj)
            self.conn.commit()
            return jobObj[0]  # Return created job ID
        except sqlite3.Error as e:
            print(f"Database error during createJob: {e}")
            self.conn.rollback()
            return False

    def updateJob(self, jobObj):
        """Update the amount of an existing job by jobId."""
        sql = '''UPDATE jobs
                 SET name = ?, company=?
                 WHERE jobId = ?'''
        try:
            self.cursor.execute(sql, (jobObj['name'], jobObj['company'], jobObj['jobId']))
            self.conn.commit()
            return self.cursor.rowcount  # Number of rows affected
        except sqlite3.Error as e:
            print(f"Database error during updateJob: {e}")
            self.conn.rollback()
            return False

    def getAllJob(self):
        try:
            sql = '''SELECT * FROM jobs'''
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            if not rows:
                return None

            # Convert rows to a list of dictionaries with ISO 8601 timestamp strings
            jobs = []
            for row in rows:
                row_dict = dict(row)
                jobs.append(row_dict)
            # sorted_rows = sorted(rows, key=lambda row: datetime.strptime(row['transactionDate'], "%d/%m/%Y"))
            return jobs
        except sqlite3.Error as e:
            print(f"Database error during getJob: {e}")
            return False
        
    def getJob(self, name=None, company=None):
        try:
            # Start SQL query and parameters list
            sql = "SELECT * FROM jobs WHERE 1=1"
            params = []

            # Dynamic conditions based on provided filters
            if name:
                sql += " AND name = ?"
                params.append(name)
            
            if company:
                sql += " AND company = ?"
                params.append(company)
        
            
            # Execute the query
            self.cursor.execute(sql, tuple(params))
            rows = self.cursor.fetchall()

            # If no rows found, return None
            if not rows:
                return None

            # Convert rows to a list of dictionaries
            jobs = []
            for row in rows:
                row_dict = dict(row)
                jobs.append(row_dict)

            return jobs
        
        except sqlite3.Error as e:
            print(f"Database error during getJob: {e}")
            return False

    def deleteJob(self, jobId):
        """Delete an job by jobId."""
        sql = '''DELETE FROM jobs WHERE jobId = ?'''
        try:
            self.cursor.execute(sql, (jobId,))
            self.conn.commit()
            return self.cursor.rowcount  # Number of rows affected
        except sqlite3.Error as e:
            print(f"Database error during deleteJob: {e}")
            self.conn.rollback()
            return False

    def close(self):
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()
