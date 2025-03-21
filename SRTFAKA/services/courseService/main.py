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
from generated import course_pb2, courseProgress_pb2
from generated import course_pb2_grpc, courseProgress_pb2_grpc
from common.utils import generateRandomId
from .db import CourseDB
from .db import CourseProgressDB

courseDB = CourseDB()
courseProgressDB = CourseProgressDB()

class CourseProgress(courseProgress_pb2_grpc.CourseProgressServicer):
    async def JoinCourse(
        self,
        request: courseProgress_pb2.CourseProgressData,
        context: grpc.aio.ServicerContext,
    ) -> courseProgress_pb2.CourseProgressData:
        try: 
            print(f"GRPC Server: {request}")

            courseProgressDB = CourseProgressDB()
            created_course_progress_id = courseProgressDB.joinCourse(request.cleared, request.student_id, request.course_id)
            
            if not created_course_progress_id:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Join course failed or error occurred.")
                return courseProgress_pb2.CourseProgressData()
            
            return courseProgress_pb2.CourseProgressData(cleared=request.cleared, student_id=request.student_id, course_id=request.course_id)

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error during joining course creation: {e}")
            return courseProgress_pb2.CourseProgressData()

    async def UpdateCourseProgress(
        self,
        request: courseProgress_pb2.CourseProgressData, 
        context: grpc.aio.ServicerContext,
    ) -> courseProgress_pb2.CourseProgressData:
        try:
            print(f"GRPC Server: {request}")

            # Instantiate the database handler (replace with actual DB interaction)
            courseProgressDB = CourseProgressDB()

            updated_course_progress = courseProgressDB.updateCourseProgress(
               request.cleared, request.student_id, request.course_id
            )

            if not updated_course_progress:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Update course progress failed or no matching record found.")
                return courseProgress_pb2.CourseProgressData()

            # Return updated CourseProgressData
            return courseProgress_pb2.CourseProgressData(
                student_id=request.student_id,
                course_id=request.course_id,
                cleared=request.cleared 
            )

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error during course progress update: {e}")
            return courseProgress_pb2.CourseProgressId()




class Course(course_pb2_grpc.CourseServicer):
    async def GetAllCourse(
        self,
        request: course_pb2.CourseData,
        context: grpc.aio.ServicerContext,
    ) -> course_pb2.CourseList:
        rows = courseDB.getAllCourse()
        if not rows:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No courses found.")
            return course_pb2.CourseList()

        courses = [
            course_pb2.CourseData(
                id=row["id"],  # Accessing dictionary keys
                name=row["name"],
                details=row["details"],
                industry_id=row["industry_id"],
                industry_name=row["industry_name"],
                cert_id=row["cert_id"],
            ) for row in rows
        ]
        # print(courses)
        return course_pb2.CourseList(courses=courses)

    async def GetCourseById(
        self,
        request: course_pb2.CourseId,
        context: grpc.aio.ServicerContext,
    ) -> course_pb2.CourseData:
        course = courseDB.getCourseById(request.id)

        if not course:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Course with ID {request.id} not found.")
            return course_pb2.CourseData()
        
        return course_pb2.CourseData(
            id=course['id'],
            name=course['name'],
            details=course['details'],
            industry_id=course['industry_id'],
            cert_id=course['cert_id'],
            industry_name=course['industry_name'],
        )
    
    async def CreateCourse(
        self,
        request: course_pb2.CourseData,
        context: grpc.aio.ServicerContext,
    ) -> course_pb2.CourseData:
        try:
            print(f"GRPC Server: {request}")

            # Call the createCourse method to insert the course into the database
            courseDB = CourseDB()  # Ensure this is initialized properly in your class
            created_course_id = courseDB.createCourse(request.name, request.details, request.industry_id, request.cert_id)

            if not created_course_id:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Course creation failed or error occurred.")
                return course_pb2.CourseData()

            return course_pb2.CourseData(name=request.name, details=request.details, industry_id=request.industry_id, cert_id=request.cert_id)

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error during course creation: {e}")
            return course_pb2.CourseData()

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
    courseProgress_pb2_grpc.add_CourseProgressServicer_to_server(CourseProgress(), server)

    listen_addr = "[::]:50052"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
