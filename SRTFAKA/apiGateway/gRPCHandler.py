from SRTFAKA.generated import account_pb2_grpc, account_pb2, course_pb2, course_pb2_grpc, assessment_pb2, assessment_pb2_grpc, job_pb2, job_pb2_grpc, certificate_pb2, certificate_pb2_grpc
from .models import AccountCreation, AccountUpdate, Course, Assessment, Job, Certificate
from fastapi import HTTPException
from dotenv import load_dotenv
from typing import Optional
import grpc
import os

load_dotenv()

ACCOUNT_SERVICE_ADDRESS = os.getenv('ACCOUNT_SERVICE_ADDRESS') 
COURSE_SERVICE_ADDRESS = os.getenv('COURSE_SERVICE_ADDRESS') 
ASSESSMENT_SERVICE_ADDRESS = os.getenv('ASSESSMENT_SERVICE_ADDRESS') 
JOB_SERVICE_ADDRESS = os.getenv('JOB_SERVICE_ADDRESS') 
CERTIFICATE_SERVICE_ADDRESS = os.getenv('CERTIFICATE_SERVICE_ADDRESS') 

async def getAccountById(accountId: str) -> account_pb2.AccountResponse:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            response = await stub.GetAccountById(account_pb2.AccountRequestById(userId=accountId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=404, detail=f"Error: {e.details()}")


async def getAccountByEmail(accountEmail: str) -> account_pb2.AccountResponse:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            response = await stub.GetAccountByEmail(account_pb2.AccountRequestByEmail(email=accountEmail))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=404, detail=f"Error: {e.details()}")
        
async def createAccount(account: AccountCreation) -> account_pb2.AccountResponse:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            response = await stub.CreateAccount(account_pb2.CreateAccountRequest(
                password=account.password,
                firstname=account.firstname,
                lastname=account.lastname,
                country_id=account.country_id,
                address=account.address,
                email=account.email,
                user_type_id=account.user_type_id
            ))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

async def updateAccount(accountId: str, account: AccountUpdate) -> account_pb2.AccountResponse:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            response = await stub.UpdateAccount(account_pb2.UpdateAccountRequest(
                userId=accountId,
                firstname=account.first_name,
                lastname=account.last_name,
                country_id=account.country_id,
                address=account.address,
                password=account.password
            ))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

                      
async def deleteAccount(accountId: str) -> None:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            response = await stub.DeleteAccount(account_pb2.AccountRequestById(userId=accountId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")


async def getCourse() -> course_pb2.CourseList:
    async with grpc.aio.insecure_channel(COURSE_SERVICE_ADDRESS) as channel:
        stub = course_pb2_grpc.CourseStub(channel)
        try:
            response = await stub.GetAllCourse(course_pb2.CourseData())
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=404, detail=f"Error: {e.details()}")

async def createCourse(course: Course) -> course_pb2.CourseData:
    async with grpc.aio.insecure_channel(COURSE_SERVICE_ADDRESS) as channel:
        stub = course_pb2_grpc.CourseStub(channel)
        try:
            response = await stub.CreateCourse(course_pb2.CourseData(name=course.name, instructor=course.instructor))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

async def updateCourse(courseId: str, course: Course) -> course_pb2.CourseData:
    async with grpc.aio.insecure_channel(COURSE_SERVICE_ADDRESS) as channel:
        stub = course_pb2_grpc.CourseStub(channel)
        try:
            response = await stub.UpdateCourse(course_pb2.CourseData(courseId=courseId, name=course.name, instructor=course.instructor))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

async def deleteCourse(courseId: str) -> course_pb2.CourseId:
    async with grpc.aio.insecure_channel(COURSE_SERVICE_ADDRESS) as channel:
        stub = course_pb2_grpc.CourseStub(channel)
        try:
            response = await stub.DeleteCourse(course_pb2.CourseId(courseId=courseId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

async def getAssessment() -> assessment_pb2.AssessmentList:
    async with grpc.aio.insecure_channel(ASSESSMENT_SERVICE_ADDRESS) as channel:
        stub = assessment_pb2_grpc.AssessmentStub(channel)
        try:
            response = await stub.GetAllAssessment(assessment_pb2.AssessmentData())
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=404, detail=f"Error: {e.details()}")

async def createAssessment(assessment: Assessment) -> assessment_pb2.AssessmentData:
    async with grpc.aio.insecure_channel(ASSESSMENT_SERVICE_ADDRESS) as channel:
        stub = assessment_pb2_grpc.AssessmentStub(channel)
        try:
            response = await stub.CreateAssessment(assessment_pb2.AssessmentData(name=assessment.name, courseId=assessment.courseId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

async def updateAssessment(assessmentId: str, assessment: Assessment) -> assessment_pb2.AssessmentData:
    async with grpc.aio.insecure_channel(ASSESSMENT_SERVICE_ADDRESS) as channel:
        stub = assessment_pb2_grpc.AssessmentStub(channel)
        try:
            response = await stub.UpdateAssessment(assessment_pb2.AssessmentData(assessmentId=assessmentId, name=assessment.name, courseId=assessment.courseId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

async def deleteAssessment(assessmentId: str) -> assessment_pb2.AssessmentId:
    async with grpc.aio.insecure_channel(ASSESSMENT_SERVICE_ADDRESS) as channel:
        stub = assessment_pb2_grpc.AssessmentStub(channel)
        try:
            response = await stub.DeleteAssessment(assessment_pb2.AssessmentId(assessmentId=assessmentId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")
        
async def getJobs() -> job_pb2.JobList:
    """Retrieve all job listings."""
    async with grpc.aio.insecure_channel(JOB_SERVICE_ADDRESS) as channel:
        stub = job_pb2_grpc.JobStub(channel)
        try:
            return await stub.GetAllJobs(job_pb2.Empty())
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=404, detail=f"Error: {e.details()}")

async def getJobDetails(jobId: int) -> job_pb2.JobData:
    """Retrieve job details by job ID."""
    async with grpc.aio.insecure_channel(JOB_SERVICE_ADDRESS) as channel:
        stub = job_pb2_grpc.JobStub(channel)
        try:
            print(f"DEBUG: Fetching job details for job_id={jobId}")
            
            response = await stub.GetJobDetails(job_pb2.JobId(jobId=jobId))

            if response.jobId == 0:
                print(f"ERROR: Job not found for job_id={jobId}")
                raise HTTPException(status_code=404, detail="Job not found.")

            print(f"DEBUG: Job details received: {response}")
            return response

        except grpc.aio.AioRpcError as e:
            print(f"ERROR: gRPC request failed for job_id={jobId} - {e.details()}")
            raise HTTPException(status_code=500, detail=f"gRPC Error: {e.details()}")

        
async def createJob(job: job_pb2.JobData) -> job_pb2.JobData:
    """Create a new job listing and return the Protobuf JobData object."""
    async with grpc.aio.insecure_channel(JOB_SERVICE_ADDRESS) as channel:
        stub = job_pb2_grpc.JobStub(channel)
        try:
            response = await stub.CreateJob(job_pb2.JobData(
                name=job.name,
                description=job.description,
                monthlySalary=job.monthlySalary,
                startDate=job.startDate,
                endDate=job.endDate,
                availableSpotCount=job.availableSpotCount,
                companyId=job.companyId,
                employmentTypeId=job.employmentTypeId
            ))

            return response

        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"gRPC Error: {e.details()}")


async def updateJob(jobId: str, job: Job) -> job_pb2.JobData:
    """Update an existing job listing."""
    async with grpc.aio.insecure_channel(JOB_SERVICE_ADDRESS) as channel:
        stub = job_pb2_grpc.JobStub(channel)
        try:
            return await stub.UpdateJob(job_pb2.JobData(
                jobId=jobId,
                name=job.name,
                description=job.description,
                monthlySalary=job.monthlySalary,
                startDate=job.startDate,
                endDate=job.endDate,
                availableSpotCount=job.availableSpotCount,
                companyId=job.companyId,
                employmentTypeId=job.employmentTypeId,    
                industryId=job.industryId,
            ))
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")



async def deleteJob(jobId: int) -> dict:
    """Delete a job listing."""
    async with grpc.aio.insecure_channel(JOB_SERVICE_ADDRESS) as channel:
        stub = job_pb2_grpc.JobStub(channel)
        try:
            response = await stub.DeleteJob(job_pb2.JobId(jobId=jobId))

            if response.jobId == 0:
                raise HTTPException(status_code=404, detail="Job not found or deletion failed.")

            return {"message": "Job deleted successfully", "jobId": response.jobId}

        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

async def applyForJob(applicant_id: int, job_id: int, resume_link: str, additional_info: Optional[str] = None) -> job_pb2.ApplicationId:
    """Allows a user to apply for a job."""
    async with grpc.aio.insecure_channel(JOB_SERVICE_ADDRESS) as channel:
        stub = job_pb2_grpc.JobStub(channel)
        try:
            print(f"DEBUG: Sending applicant_id={applicant_id} to ApplyJob gRPC call")
            
            return await stub.ApplyJob(job_pb2.ApplicationData(
                applicantId=applicant_id,
                jobId=job_id,
                resumeLink=resume_link,
                additionalInfo=additional_info or ""
            ))
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")


async def getApplicationsByUser(userId: int) -> job_pb2.ApplicationList:
    """Retrieve job applications for a specific user."""
    async with grpc.aio.insecure_channel(JOB_SERVICE_ADDRESS) as channel:
        stub = job_pb2_grpc.JobStub(channel)
        try:
            print(f"DEBUG: Fetching applications for user_id={userId}")
            
            response = await stub.GetApplications(job_pb2.UserId(userId=userId))

            if not response.applications:
                print(f"ERROR: No applications found for user_id={userId}")
                raise HTTPException(status_code=404, detail="No job applications found.")

            return response

        except grpc.aio.AioRpcError as e:
            print(f"ERROR: gRPC request failed for user_id={userId} - {e.details()}")
            raise HTTPException(status_code=500, detail=f"gRPC Error: {e.details()}")


async def getApplicationDetails(applicationId: int) -> job_pb2.ApplicationData:
    """Retrieve job application details by application ID."""
    async with grpc.aio.insecure_channel(JOB_SERVICE_ADDRESS) as channel:
        stub = job_pb2_grpc.JobStub(channel)
        try:
            print(f"DEBUG: Fetching application details for application_id={applicationId}")
            
            response = await stub.GetApplicationDetails(job_pb2.ApplicationId(applicationId=applicationId))

            if response.applicationId == 0:
                print(f"ERROR: Application not found for application_id={applicationId}")
                raise HTTPException(status_code=404, detail="Application not found.")

            print(f"DEBUG: Application details received: {response}")
            return response

        except grpc.aio.AioRpcError as e:
            print(f"ERROR: gRPC request failed for application_id={applicationId} - {e.details()}")
            raise HTTPException(status_code=500, detail=f"gRPC Error: {e.details()}")

        
async def getCertificate() -> certificate_pb2.CertificateList:
    async with grpc.aio.insecure_channel(CERTIFICATE_SERVICE_ADDRESS) as channel:
        stub = certificate_pb2_grpc.CertificateStub(channel)
        try:
            response = await stub.GetAllCertificate(certificate_pb2.CertificateData())
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=404, detail=f"Error: {e.details()}")

async def createCertificate(certificate: Certificate) -> certificate_pb2.CertificateData:
    async with grpc.aio.insecure_channel(CERTIFICATE_SERVICE_ADDRESS) as channel:
        stub = certificate_pb2_grpc.CertificateStub(channel)
        try:
            response = await stub.CreateCertificate(certificate_pb2.CertificateData(name=certificate.name, courseId=certificate.courseId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

async def updateCertificate(certificateId: str, certificate: Certificate) -> certificate_pb2.CertificateData:
    async with grpc.aio.insecure_channel(CERTIFICATE_SERVICE_ADDRESS) as channel:
        stub = certificate_pb2_grpc.CertificateStub(channel)
        try:
            response = await stub.UpdateCertificate(certificate_pb2.CertificateData(certificateId=certificateId, name=certificate.name, courseId=certificate.courseId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

async def deleteCertificate(certificateId: str) -> certificate_pb2.CertificateId:
    async with grpc.aio.insecure_channel(CERTIFICATE_SERVICE_ADDRESS) as channel:
        stub = certificate_pb2_grpc.CertificateStub(channel)
        try:
            response = await stub.DeleteCertificate(certificate_pb2.CertificateId(certificateId=certificateId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")