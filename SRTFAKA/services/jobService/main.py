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
from ...generated import job_pb2
from ...generated import job_pb2_grpc
from ...common.utils import generateRandomId
from .db import JobDB

jobDB = JobDB()

class Job(job_pb2_grpc.JobServicer):
    async def GetAllJob(
        self,
        request: job_pb2.JobData,
        context: grpc.aio.ServicerContext,
    ) -> job_pb2.JobList:
        rows = jobDB.getAllJob()
        if rows is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No jobs found.")
            return job_pb2.JobList()
        jobs = [job_pb2.JobData(jobId=row["jobId"], name=row["name"],
                                           company=row["company"]) for row in rows]
        return job_pb2.JobList(jobs=jobs)


    async def CreateJob(
                self,
                request: job_pb2.JobData,
                context: grpc.aio.ServicerContext,
            ) -> job_pb2.JobData:
                newJobId = generateRandomId()
                print(f"GRPC Server: {request}")
                job = jobDB.createJob((newJobId, request.name, request.company))
                if job is None:
                    context.set_code(grpc.StatusCode.INTERNAL)
                    context.set_details("Job creation failed or error occured.")
                    return job_pb2.JobData()
                return job_pb2.JobData(jobId=newJobId, name=request.name, company=request.company)

    async def UpdateJob(self, request: job_pb2.JobData, context: grpc.aio.ServicerContext) -> job_pb2.JobData:
        updated = jobDB.updateJob(
            {"jobId": request.jobId, "name": request.name, "company": request.company}
        )
        if not updated:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Job update failed or error occured.")
            return job_pb2.JobData()
        return job_pb2.JobData(jobId=request.jobId)
    
    async def DeleteJob(self, request: job_pb2.JobId, context: grpc.aio.ServicerContext) -> job_pb2.JobId:
        deleted = jobDB.deleteJob(request.jobId)
        if not deleted:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Job not found for deletion or error occured.")
        return job_pb2.JobId()


async def serve() -> None:
    server = grpc.aio.server()
    job_pb2_grpc.add_JobServicer_to_server(Job(), server)
    listen_addr = "[::]:50054"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
