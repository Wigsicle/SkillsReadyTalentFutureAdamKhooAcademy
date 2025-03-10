# Copyright 2020 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import logging
import grpc
from SRTFAKA.generated import job_pb2_grpc
from SRTFAKA.generated import job_pb2
from .db import JobDB

jobDB = JobDB()

class Job(job_pb2_grpc.JobServicer):
    """gRPC Servicer for Job Service"""

    async def GetAllJobs(self, request: job_pb2.Empty, context: grpc.aio.ServicerContext) -> job_pb2.JobList:
        """Retrieve all job listings"""
        rows = jobDB.get_job()
        if not rows:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return job_pb2.JobList()

        jobs = [
            job_pb2.JobData(
                jobId=str(row["id"]),  
                name=row["name"],
                company=row["company"],
                employmentType=row["value"],  
                pay=row["pay"]
            ) 
            for row in rows
        ]
        return job_pb2.JobList(jobs=jobs)

    async def GetJobDetails(self, request: job_pb2.JobId, context: grpc.aio.ServicerContext) -> job_pb2.JobData:
        """Retrieve full job details"""
        job = jobDB.get_job_details(request.jobId)
        if not job:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Job not found.")
            return job_pb2.JobData()
        
        return job_pb2.JobData(
            jobId=str(job["id"]),
            name=job["name"],
            company=job["company"],
            description=job["description"] or "",
            salary=job["pay"],
            startDate=job["start_date"],
            endDate=job["end_date"],
            employmentType=job["value"]
        )

    async def CreateJob(self, request: job_pb2.JobData, context: grpc.aio.ServicerContext) -> job_pb2.JobData:
        """Create a new job listing"""
        job_data = {
            "name": request.name,
            "description": request.description,
            "monthly_salary": request.salary,
            "start_date": datetime.strptime(request.startDate, "%Y-%m-%d"),
            "end_date": datetime.strptime(request.endDate, "%Y-%m-%d"),
            "available_spot_count": request.availableSpotCount,
            "company_id": request.companyId,
            "employment_type_id": request.employmentTypeId,
            "pay": request.salary
        }
        
        job_id = jobDB.create_job(job_data)
        if not job_id:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to create job.")
            return job_pb2.JobData()
        
        return job_pb2.JobData(jobId=str(job_id), name=request.name, company=str(request.companyId))

    async def UpdateJob(self, request: job_pb2.JobData, context: grpc.aio.ServicerContext) -> job_pb2.JobData:
        """Update an existing job listing"""
        update_data = {
            "name": request.name,
            "description": request.description,
            "monthly_salary": request.salary,
            "start_date": datetime.strptime(request.startDate, "%Y-%m-%d"),
            "end_date": datetime.strptime(request.endDate, "%Y-%m-%d"),
            "available_spot_count": request.availableSpotCount,
            "employment_type_id": request.employmentTypeId,
            "pay": request.salary
        }

        updated = jobDB.update_job(request.jobId, update_data)
        if not updated:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Job update failed.")
            return job_pb2.JobData()
        
        return job_pb2.JobData(jobId=request.jobId)

    async def DeleteJob(self, request: job_pb2.JobId, context: grpc.aio.ServicerContext) -> job_pb2.JobId:
        """Delete a job by its ID"""
        deleted = jobDB.delete_job(request.jobId)
        if not deleted:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Job not found or deletion failed.")
        
        return job_pb2.JobId(jobId=request.jobId)

    async def ApplyJob(self, request: job_pb2.ApplicationData, context: grpc.aio.ServicerContext) -> job_pb2.ApplicationId:
        """Allows a user to apply for a job"""
        application_id = jobDB.apply_job(
            applicant_id=request.applicantId,
            job_id=request.jobId,
            resume_link=request.resumeLink,
            additional_info=request.additionalInfo
        )
        
        if not application_id:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Application failed.")
            return job_pb2.ApplicationId()
        
        return job_pb2.ApplicationId(applicationId=str(application_id))

    async def GetApplications(self, request: job_pb2.UserId, context: grpc.aio.ServicerContext) -> job_pb2.ApplicationList:
        """Retrieve all job applications by a user"""
        applications = jobDB.get_applications(request.userId)
        if not applications:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No applications found.")
            return job_pb2.ApplicationList()
        
        return job_pb2.ApplicationList(
            applications=[
                job_pb2.ApplicationData(
                    applicationId=str(app["id"]),
                    jobId=str(app["job_id"]),
                    jobName=app["job_name"],
                    company=app["company"],
                    appliedOn=app["applied_on"],
                    resumeLink=app["resume_link"],
                    additionalInfo=app["additional_info"] or ""
                )
                for app in applications
            ]
        )

    async def GetApplicationDetails(self, request: job_pb2.ApplicationId, context: grpc.aio.ServicerContext) -> job_pb2.ApplicationData:
        """Retrieve full details of a specific job application"""
        application = jobDB.get_application_details(request.applicationId)
        if not application:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Application not found.")
            return job_pb2.ApplicationData()
        
        return job_pb2.ApplicationData(
            applicationId=str(application["id"]),
            jobId=str(application["job_id"]),
            jobName=application["job_name"],
            company=application["company"],
            appliedOn=application["applied_on"],
            resumeLink=application["resume_link"],
            additionalInfo=application["additional_info"] or ""
        )

async def serve() -> None:
    """Start the gRPC server."""
    server = grpc.aio.server()
    job_pb2_grpc.add_JobServiceServicer_to_server(Job(), server)
    
    listen_addr = "[::]:50054"
    server.add_insecure_port(listen_addr)
    logging.info("Starting Job Service on %s", listen_addr)
    
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())