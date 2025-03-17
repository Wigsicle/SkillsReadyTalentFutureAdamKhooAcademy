from fastapi import APIRouter, Depends, HTTPException, Query
from ..gRPCHandler import getJobs, getJobDetails, createJob, updateJob, deleteJob, applyForJob, getApplicationsByUser, getApplicationDetails
from google.protobuf.json_format import MessageToDict
from ..models import JobResponse, Job, JobApplication, JobApplicationResponse
from ..auth import getCurrentUser

job = APIRouter()

@job.get("/job")
async def get_job():
    jobs = MessageToDict(await getJobs())
    return {"message": "Jobs retrieved", "data": jobs}

@job.get("/job/{jobId}")
async def get_job_details(jobId: int):
    """Retrieve details of a specific job by jobId."""
    
    print(f"DEBUG: Fetching job details for job_id={jobId}")
    
    job_details = await getJobDetails(jobId)

    if not job_details or job_details.jobId == 0:
        raise HTTPException(status_code=404, detail="Job not found.")

    return {"message": "Job details retrieved", "data": MessageToDict(job_details)}
    
@job.post("/job/create") 
async def create_job(job: Job): 
    newJob = await createJob(job) 
    if newJob is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Job created", "data": MessageToDict(newJob)}

@job.put("/job/update/{jobId}")
async def update_job(jobId: int, job: Job):
    """Update an existing job listing"""

    print(f"DEBUG: Received request to update job_id={jobId} with data: {job.dict()}")

    response = await updateJob(jobId, job)

    if response is None or response.jobId == 0:
        print(f"ERROR: Job update failed for job_id={jobId}")
        raise HTTPException(status_code=500, detail="Job update failed.")

    print(f"DEBUG: Job updated successfully: {response}")
    
    return {"message": "Job updated successfully", "data": MessageToDict(response)}



@job.delete("/job")
async def delete_job(jobId: int):
    deletedJob = await deleteJob(jobId)
    if deletedJob is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Job deleted successfully"}


@job.post("/job/apply")
async def apply_job(application: JobApplication):
    """Allows a user to apply for a job."""
    
    print(f"DEBUG: Sending applicant_id={application.applicantId} to ApplyJob gRPC call")
    
    application_response = await applyForJob(
        applicant_id=application.applicantId,
        job_id=application.jobId,
        resume_link=application.resumeLink,
        additional_info=application.additionalInfo
    )

    if application_response is None:
        raise HTTPException(status_code=500, detail="Job application failed")

    return {"message": "Job application submitted", "data": MessageToDict(application_response)}


@job.get("/job/applications/{userId}")
async def get_applications_by_user(userId: int):
    """Retrieve job applications for a specific user."""
    
    print(f"DEBUG: Fetching job applications for user_id={userId}")
    
    applications = await getApplicationsByUser(userId)

    if not applications.applications:
        raise HTTPException(status_code=404, detail="No job applications found.")

    return {"message": "Applications retrieved", "data": MessageToDict(applications)}


@job.get("/job/application/{applicationId}")
async def get_application_details(applicationId: int):
    """Retrieve details of a specific job application by applicationId."""
    
    print(f"DEBUG: Fetching job application details for application_id={applicationId}")
    
    application_details = await getApplicationDetails(applicationId)

    if not application_details or application_details.applicationId == 0:
        raise HTTPException(status_code=404, detail="Application not found.")

    return {"message": "Application details retrieved", "data": MessageToDict(application_details)}
