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
from .db import AssessmentDB, Assessment
from sqlalchemy.orm import Session

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

    async def CreateAssessment(
                self,
                request: assessment_pb2.AssessmentData,
                context: grpc.aio.ServicerContext,
            ) -> assessment_pb2.AssessmentData:
                with Session() as session:
                    new_assessment = Assessment(
                        name=request.name,
                        course_id=request.courseId,
                        question_paper=request.question_paper  # Assuming this is passed in the request
                    )
                    session.add(new_assessment)
                    session.commit()
                    return assessment_pb2.AssessmentData(assessmentId=new_assessment.id, name=new_assessment.name, courseId=new_assessment.course_id)

    async def UpdateAssessment(self, request: assessment_pb2.AssessmentData, context: grpc.aio.ServicerContext) -> assessment_pb2.AssessmentData:
        updated = assessmentDB.updateAssessment(
            {"assessmentId": request.assessmentId, "name": request.name, "courseId": request.courseId}
        )
        if not updated:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Assessment update failed or error occured.")
            return assessment_pb2.AssessmentData()
        return assessment_pb2.AssessmentData(assessmentId=request.assessmentId)
    
    async def DeleteAssessment(self, request: assessment_pb2.AssessmentId, context: grpc.aio.ServicerContext) -> assessment_pb2.AssessmentId:
        deleted = assessmentDB.deleteAssessment(request.assessmentId)
        if not deleted:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Assessment not found for deletion or error occured.")
        return assessment_pb2.AssessmentId()


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