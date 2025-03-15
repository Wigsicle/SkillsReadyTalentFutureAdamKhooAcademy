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
from ..generated import course_pb2
from ..generated import course_pb2_grpc
from ..common.utils import generateRandomId
from .db import CourseDB

courseDB = CourseDB()

class Course(course_pb2_grpc.CourseServicer):
    async def GetAllCourse(
        self,
        request: course_pb2.CourseData,
        context: grpc.aio.ServicerContext,
    ) -> course_pb2.CourseList:
        rows = courseDB.getAllCourse()
        if rows is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No courses found.")
            return course_pb2.CourseList()
        courses = [course_pb2.CourseData(courseId=row["courseId"], name=row["name"],
                                           instructor=row["instructor"]) for row in rows]
        return course_pb2.CourseList(courses=courses)


    async def CreateCourse(
                self,
                request: course_pb2.CourseData,
                context: grpc.aio.ServicerContext,
            ) -> course_pb2.CourseData:
                newCourseId = generateRandomId()
                print(f"GRPC Server: {request}")
                course = courseDB.createCourse((newCourseId, request.name, request.instructor))
                if course is None:
                    context.set_code(grpc.StatusCode.INTERNAL)
                    context.set_details("Course creation failed or error occured.")
                    return course_pb2.CourseData()
                return course_pb2.CourseData(courseId=newCourseId, name=request.name, instructor=request.instructor)

    async def UpdateCourse(self, request: course_pb2.CourseData, context: grpc.aio.ServicerContext) -> course_pb2.CourseData:
        updated = courseDB.updateCourse(
            {"courseId": request.courseId, "name": request.name, "instructor": request.instructor}
        )
        if not updated:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Course update failed or error occured.")
            return course_pb2.CourseData()
        return course_pb2.CourseData(courseId=request.courseId)
    
    async def DeleteCourse(self, request: course_pb2.CourseId, context: grpc.aio.ServicerContext) -> course_pb2.CourseId:
        deleted = courseDB.deleteCourse(request.courseId)
        if not deleted:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Course not found for deletion or error occured.")
        return course_pb2.CourseId()


async def serve() -> None:
    server = grpc.aio.server()
    course_pb2_grpc.add_CourseServicer_to_server(Course(), server)
    listen_addr = "[::]:50052"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
