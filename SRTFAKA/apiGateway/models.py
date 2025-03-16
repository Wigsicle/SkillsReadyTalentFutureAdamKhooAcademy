from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
    # Convert courseId to int if you store it as an int in your DB/proto
    courseId: Optional[int] = None  
    yearsValid: Optional[int] = None
    description: Optional[str] = None
    additionalInfo: Optional[str] = None  # JSON string

class CertificateResponse(Certificate):
    certificateId: int

class UserCertificate(BaseModel):
    userId: int
    certId: int
    #issuedOn: Optional[datetime] = None
    #expiresOn: Optional[datetime] = None
    # additionalInfo as a JSON string or dictionary, depending on how you want to handle it
    additionalInfo: Optional[str] = None

class UserCertificateResponse(UserCertificate):
    id: int