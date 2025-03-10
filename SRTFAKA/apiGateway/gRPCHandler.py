from generated import account_pb2_grpc, account_pb2, course_pb2, course_pb2_grpc, assessment_pb2, assessment_pb2_grpc, job_pb2, job_pb2_grpc, certificate_pb2, certificate_pb2_grpc
from .models import AccountCreation, AccountUpdate, Course, Assessment, Job, Certificate, CourseProgress
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


async def getAccountByUsername(accountUsername: str) -> account_pb2.AccountResponse:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            response = await stub.GetAccountByUsername(account_pb2.AccountRequestByUsername(username=accountUsername))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=404, detail=f"Error: {e.details()}")
        
async def createAccount(account: AccountCreation) -> account_pb2.AccountResponse:
    async with grpc.aio.insecure_channel(ACCOUNT_SERVICE_ADDRESS) as channel:
        stub = account_pb2_grpc.AccountStub(channel)
        try:
            response = await stub.CreateAccount(account_pb2.CreateAccountRequest(
                name=account.name, 
                username=account.username,
                password=account.password
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
                name=account.name,
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
        
async def joinCourse(course_progress: CourseProgress) -> course_pb2.CourseProgressData:
    async with grpc.aio.insecure_channel(COURSE_SERVICE_ADDRESS) as channel:
        stub = course_pb2_grpc.CourseProgressStub(channel)
        try:

            response = await stub.JoinCourse(course_pb2.CourseProgressData(
                cleared=course_progress.cleared, 
                student_id=course_progress.student_id, 
                course_id=course_progress.course_id
            ))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

async def createCourse(course: Course) -> course_pb2.CourseData:
    async with grpc.aio.insecure_channel(COURSE_SERVICE_ADDRESS) as channel:
        stub = course_pb2_grpc.CourseStub(channel)
        try:
            # Creating a CourseData object with additional fields like details, industry_id, and cert_id
            response = await stub.CreateCourse(course_pb2.CourseData(
                name=course.name,
                details=course.details,  # Including the details field
                industry_id=course.industry_id,  # Including the industry_id
                cert_id=course.cert_id  # Including the cert_id
            ))
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
        
async def getJob() -> job_pb2.JobList:
    async with grpc.aio.insecure_channel(JOB_SERVICE_ADDRESS) as channel:
        stub = job_pb2_grpc.JobStub(channel)
        try:
            response = await stub.GetAllJob(job_pb2.JobData())
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=404, detail=f"Error: {e.details()}")

async def createJob(job: Job) -> job_pb2.JobData:
    async with grpc.aio.insecure_channel(JOB_SERVICE_ADDRESS) as channel:
        stub = job_pb2_grpc.JobStub(channel)
        try:
            response = await stub.CreateJob(job_pb2.JobData(name=job.name, company=job.company))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

async def updateJob(jobId: str, job: Job) -> job_pb2.JobData:
    async with grpc.aio.insecure_channel(JOB_SERVICE_ADDRESS) as channel:
        stub = job_pb2_grpc.JobStub(channel)
        try:
            response = await stub.UpdateJob(job_pb2.JobData(jobId=jobId, name=job.name, company=job.company))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")

async def deleteJob(jobId: str) -> job_pb2.JobId:
    async with grpc.aio.insecure_channel(JOB_SERVICE_ADDRESS) as channel:
        stub = job_pb2_grpc.JobStub(channel)
        try:
            response = await stub.DeleteJob(job_pb2.JobId(jobId=jobId))
            return response
        except grpc.aio.AioRpcError as e:
            raise HTTPException(status_code=500, detail=f"Error: {e.details()}")
        
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