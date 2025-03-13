from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    userId: str
    
class Account(BaseModel):
    username: str 
    
class AccountCreation(Account):
    password: str
    username: str
    firstname: str
    lastname: str
    country_id: int
    address: str
    email: str
    user_type_id: int
    
class AccountUpdate(Account):
    password: str
    
class AccountResponse(Account):
    userId: str
    password: str
    firstname: str
    lastname: str
    country_id: int
    address: str
    email: str
    user_type_id: int

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
    description: Optional[str] = None
    monthlySalary: Optional[int] = None
    startDate: str
    endDate: str
    availableSpotCount: int
    companyId: int
    companyName: Optional[str] = None
    employmentTypeId: int
    employmentValue: Optional[str] = None
    industryId: Optional[int] = None
    industryName: Optional[str] = None

class JobResponse(Job):
    jobId: int

class JobApplication(BaseModel):
    applicantId: int
    jobId: int
    resumeLink: str
    additionalInfo: Optional[str] = None
    industryId: int

class JobApplicationResponse(JobApplication):
    applicationId: int

class Certificate(BaseModel):
    name: str
    courseId: str
    
class CertificateResponse(Certificate):
    certificateId: str