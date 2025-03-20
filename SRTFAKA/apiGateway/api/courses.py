from fastapi import APIRouter, Depends, HTTPException, Query
from ..gRPCHandler import getCourse, createCourse, updateCourse, deleteCourse, joinCourse, getCourseById, updateCourseProgress
from google.protobuf.json_format import MessageToDict
from ..models import CourseResponse, Course, CourseProgress, CourseProgressId
from ..auth import getCurrentUser

course = APIRouter()

courseProgress = APIRouter()

@course.get("/course")
async def get_course():
    courses = MessageToDict(await getCourse())
    return {"message": "Courses retrieved", "data": courses}

@course.get("/course/{course_id}")
async def get_course_by_id(course_id: int):
    course_data = MessageToDict(await getCourseById(course_id))
    return {"message": "Course retrieved", "data": course_data}

    
@course.post("/course/create") 
async def create_course(course: Course): 
    newCourse = await createCourse(course) 
    if newCourse is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Course created", "data": MessageToDict(newCourse)}

@course.put("/course/update")
async def update_course(courseId: str, course: Course, currentUser: CourseResponse = Depends(getCurrentUser)):
    response = await updateCourse(courseId, course)
    if response is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Course updated", "data": MessageToDict(response)}

@course.delete("/course")
async def delete_course(courseId: str, currentUser: CourseResponse = Depends(getCurrentUser)):
    deletedCourse = await deleteCourse(courseId)
    if deletedCourse is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Course deleted successfully"}

@courseProgress.post("/courseProgress/join")
async def join_course(course_progress: CourseProgress):
    # Ensure the courseProgress object is correctly passed and contains necessary data
        # You can directly use the course_progress object here
        response = await joinCourse(course_progress)

        if response is None:
            raise HTTPException(status_code=500, details="Join Course failed")
        return {"message": "Joined Course", "data": MessageToDict(response)}

@courseProgress.put("/courseProgress/update")
async def update_course_progress(course_progress: CourseProgress):
    response = await updateCourseProgress(course_progress)

    # Check for a successful response
    if response is None:
        raise HTTPException(status_code=500, detail="Update Course Progress failed")

    # Return success message and the updated data
    return {"message": "Course Progress Updated", "data": MessageToDict(response)}




    



