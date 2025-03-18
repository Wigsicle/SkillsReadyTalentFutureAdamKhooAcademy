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
from ...generated import assessment_pb2
from ...generated import assessment_pb2_grpc
from ...common.utils import generateRandomId
from .db import AssessmentDB, Assessment, AssessmentAttempt
from sqlalchemy.orm import Session
from datetime import datetime

assessmentDB = AssessmentDB()

class Assessment(assessment_pb2_grpc.AssessmentServicer):
    async def GetAllAssessment(
        self,
        request: assessment_pb2.AssessmentData,
        context: grpc.aio.ServicerContext,
    ) -> assessment_pb2.AssessmentList:
        assessments = assessmentDB.getAllAssessment()
        if assessments is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No assessments found.")
            return assessment_pb2.AssessmentList()

        # Log the retrieved assessments
        for assessment in assessments:
            print(f"Retrieved Assessment: ID={assessment.id}, Name={assessment.name}, CourseID={assessment.course_id}, TotalMarks={assessment.total_marks}")

        return assessment_pb2.AssessmentList(assessments=[assessment_pb2.AssessmentData(
            assessmentId=int(assessment.id) if assessment.id is not None else 0,
            name=assessment.name if assessment.name is not None else "",
            courseId=int(assessment.course_id) if assessment.course_id is not None else 0,
            total_marks=float(assessment.total_marks) if assessment.total_marks is not None else 0.0
        ) for assessment in assessments])

    async def GetAllAssessmentAttempts(
        self,
        request: assessment_pb2.AssessmentData,
        context: grpc.aio.ServicerContext,
    ) -> assessment_pb2.AssessmentAttemptList:
        attempts = assessmentDB.getAllAssessmentAttempts()
        if attempts is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No assessment attempts found.")
            return assessment_pb2.AssessmentAttemptList()

        # Log the retrieved attempts
        for attempt in attempts:
            print(f"Retrieved Assessment Attempt: ID={attempt.id}, Earned Marks={attempt.earned_marks}, Attempted On={attempt.attempted_on}, Remarks={attempt.remarks}")

        return assessment_pb2.AssessmentAttemptList(attempts=[assessment_pb2.AssessmentAttemptData(
            attemptId=int(attempt.id) if attempt.id is not None else 0,
            earnedMarks=float(attempt.earned_marks) if attempt.earned_marks is not None else 0.0,
            attemptedOn=str(attempt.attempted_on) if attempt.attempted_on is not None else "",
            remarks=attempt.remarks if attempt.remarks is not None else ""
        ) for attempt in attempts])

    async def AddAssessmentAttempt(
        self,
        request: assessment_pb2.AssessmentAttemptData,
        context: grpc.aio.ServicerContext,
    ) -> assessment_pb2.AssessmentAttemptData:
        """Add a new assessment attempt."""
        try:
            new_attempt = AssessmentAttempt(
                earned_marks=request.earnedMarks,
                attempted_on=datetime.now(),  # Set to current date
                remarks=request.remarks,
                student_id=request.studentId,  # Set student_id from request
                assessment_id=request.assessmentId  # Set assessment_id from request
            )
            
            assessmentDB.session.add(new_attempt)
            assessmentDB.session.commit()
            
            return assessment_pb2.AssessmentAttemptData(
                attemptId=new_attempt.id,
                earnedMarks=new_attempt.earned_marks,
                attemptedOn=new_attempt.attempted_on.isoformat(),
                remarks=new_attempt.remarks
            )
        except Exception as e:
            assessmentDB.session.rollback()  # Rollback the session on error
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to add assessment attempt: {str(e)}")
            return assessment_pb2.AssessmentAttemptData()


async def serve() -> None:
    server = grpc.aio.server()
    assessment_pb2_grpc.add_AssessmentServicer_to_server(Assessment(), server)
    listen_addr = "[::]:50053"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())