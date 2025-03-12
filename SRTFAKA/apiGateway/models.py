from pydantic import BaseModel


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
    company: str
    
class JobResponse(Job):
    jobId: str
    
class Certificate(BaseModel):
    name: str
    courseId: str
    
class CertificateResponse(Certificate):
    certificateId: str