from fastapi import APIRouter, Depends, HTTPException, Query
from ..gRPCHandler import getJob, createJob, updateJob, deleteJob
from google.protobuf.json_format import MessageToDict
from ..models import JobResponse, Job
from ..auth import getCurrentUser

job = APIRouter()

@job.get("/job")
async def get_job():
    jobs = MessageToDict(await getJob())
    return {"message": "Jobs retrieved", "data": jobs}
    
@job.post("/job/create") 
async def create_job(job: Job): 
    newJob = await createJob(job) 
    if newJob is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Job created", "data": MessageToDict(newJob)}

@job.put("/job/update")
async def update_job(jobId: str, job: Job, currentUser: JobResponse = Depends(getCurrentUser)):
    response = await updateJob(jobId, job)
    if response is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Job updated", "data": MessageToDict(response)}

@job.delete("/job")
async def delete_job(jobId: str, currentUser: JobResponse = Depends(getCurrentUser)):
    deletedJob = await deleteJob(jobId)
    if deletedJob is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Job deleted successfully"}