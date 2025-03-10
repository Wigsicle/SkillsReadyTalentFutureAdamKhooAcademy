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
from SRTFAKA.generated import job_pb2
from SRTFAKA.generated import job_pb2_grpc
from .db import JobDB
from datetime import datetime


jobDB = JobDB()

class Job(job_pb2_grpc.JobServicer):
    """gRPC Servicer for Job Service"""

    async def GetAllJobs(self, request: job_pb2.Empty, context: grpc.aio.ServicerContext) -> job_pb2.JobList:
        """Retrieve all job listings"""
        rows = jobDB.get_job()
        if not rows:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return job_pb2.JobList()

        print(f"DEBUG: Retrieved rows: {rows}")

        jobs = []
        for row in rows:
            try:
                jobs.append(job_pb2.JobData(
                    jobId=int(row[0]),  
                    name=row[1],
                    description=row[2] or "",
                    monthlySalary=int(row[3]),
                    startDate=row[4].strftime("%Y-%m-%d"),
                    endDate=row[5].strftime("%Y-%m-%d"),
                    availableSpotCount=int(row[6]),
                    companyId=int(row[7]),
                    companyName=row[8],
                    employmentTypeId=int(row[9]),
                    industryId=int(row[10]),
                    industryName=row[11]  
                ))
            except IndexError:
                print(f"❌ ERROR: Row structure mismatch! {row}")  # ✅ Debugging Step
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Data format error in job retrieval.")
                return job_pb2.JobList()

        # jobs = [
        #     job_pb2.JobData(
        #         jobId=row[0],  
        #         name=row[1],
        #         description=row[2] or "",
        #         companyId=row[3],
        #         employmentTypeId=row[4],  
        #         startDate=row[5].strftime("%Y-%m-%d"),
        #         endDate=row[6].strftime("%Y-%m-%d"),
        #         availableSpotCount=row[7],
        #         industryId=row[8],
        #     ) 
        #     for row in rows
        # ]
        return job_pb2.JobList(jobs=jobs)

    async def GetJobDetails(self, request: job_pb2.JobId, context: grpc.aio.ServicerContext) -> job_pb2.JobData:
        """Retrieve full job details"""
        job = jobDB.get_job_details(request.jobId)
        if not job:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Job not found.")
            return job_pb2.JobData()
        
        return job_pb2.JobData(
            jobId=job[0],
            name=job[1],
            description=job[2] or "",
            monthlySalary=job[3],
            startDate=job[4].strftime("%Y-%m-%d"),
            endDate=job[5].strftime("%Y-%m-%d"),
            availableSpotCount=job[6],
            companyId=job[7],
            employmentTypeId=job[8],
            industryId=job[9],
        )


    async def CreateJob(self, request: job_pb2.JobData, context: grpc.aio.ServicerContext) -> job_pb2.JobData:
        """Create a new job listing"""
        job_data = {
             "name": request.name,
            "description": request.description,
            "monthly_salary": request.monthlySalary,
            "start_date": datetime.strptime(request.startDate, "%Y-%m-%d"),
            "end_date": datetime.strptime(request.endDate, "%Y-%m-%d"),
            "available_spot_count": request.availableSpotCount,
            "company_id": request.companyId,
            "employment_type_id": request.employmentTypeId,
            "industry_id": request.industryId,
        }
        
        job_id = jobDB.create_job(job_data)
        if not job_id:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to create job.")
            return job_pb2.JobData()
        
        return job_pb2.JobData(jobId=job_id, name=request.name, companyId=request.companyId)

    async def UpdateJob(self, request: job_pb2.JobData, context: grpc.aio.ServicerContext) -> job_pb2.JobData:
        """Update an existing job listing"""
        update_data = {
            "name": request.name,
            "description": request.description,
            "monthly_salary": request.monthlySalary,
            "start_date": datetime.strptime(request.startDate, "%Y-%m-%d"),
            "end_date": datetime.strptime(request.endDate, "%Y-%m-%d"),
            "available_spot_count": request.availableSpotCount,
            "company_id": request.companyId,
            "employment_type_id": request.employmentTypeId,
            "industry_id": request.industryId,
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
            applicant_id=request.applicationId,
            job_id=request.jobId,
            resume_link=request.resumeLink,
            additional_info=request.additionalInfo
        )
        
        if not application_id:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Application failed.")
            return job_pb2.ApplicationId()
        
        return job_pb2.ApplicationId(applicationId=application_id)

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
                    applicationId=app[0],
                    jobId=app[1],
                    jobName=app[2],
                    companyId=app[3],
                    appliedOn=app[4].strftime("%Y-%m-%d"),
                    resumeLink=app[5],
                    additionalInfo=app[6] or "",
                    industryId=app[7]
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
            applicationId=application[0],
            jobId=application[1],
            jobName=application[2],
            companyId=application[3],
            appliedOn=application[4].strftime("%Y-%m-%d"),
            resumeLink=application[5],
            additionalInfo=application[6] or "",
            industryId=application[7]
        )

async def serve() -> None:
    """Start the gRPC server."""
    server = grpc.aio.server()
    job_pb2_grpc.add_JobServicer_to_server(Job(), server)
    listen_addr = "[::]:50054"
    server.add_insecure_port(listen_addr)
    logging.info("Starting Job Service on %s", listen_addr)
    
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())