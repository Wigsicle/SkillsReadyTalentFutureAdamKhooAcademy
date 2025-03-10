from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    userId: str
    
class Account(BaseModel):
    name: str 
    
class AccountCreation(Account):
    password: str
    username: str
    
class AccountUpdate(Account):
    password: str
    
class AccountResponse(Account):
    userId: str
    password: str
    accountStatus: str

class Course(BaseModel):
    name: str
    instructor: str
    
class CourseResponse(Course):
    courseId: str
    
class Assessment(BaseModel):
    name: str
    courseId: str
    
class AssessmentResponse(Assessment):
    assessmentId: str
    
class Job(BaseModel):
    name: str
    company_id: int
    description: Optional[str] = None
    monthly_salary: Optional[int] = None
    start_date: str
    end_date: str
    employment_type_id: int
    available_spot_count: int
    industry_id: int
    pay: int

class JobResponse(Job):
    jobId: int

class JobApplication(BaseModel):
    applicant_id: int
    job_id: int
    resume_link: str
    additional_info: Optional[str] = None
    industry_id: int

class JobApplicationResponse(JobApplication):
    applicationId: int

class Certificate(BaseModel):
    name: str
    courseId: str
    
class CertificateResponse(Certificate):
    certificateId: str