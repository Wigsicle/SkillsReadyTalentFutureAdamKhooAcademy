from fastapi import APIRouter, Depends, HTTPException, Query
from ..gRPCHandler import getAssessment, createAssessment, updateAssessment, deleteAssessment
from google.protobuf.json_format import MessageToDict
from ..models import AssessmentResponse, Assessment
from ..auth import getCurrentUser
from ..db import load_questions

assessment = APIRouter()

@assessment.get("/assessment")
async def get_assessment():
    assessments = await getAssessment()  # Assuming this returns a list of Assessment objects
    # Format the assessments to match the expected structure
    formatted_assessments = [
        {
            "id": assessment.id,
            "name": assessment.name,
            "total_marks": assessment.total_marks,
            "course_id": assessment.course_id
        }
        for assessment in assessments
    ]
    return {"message": "Assessments retrieved", "data": formatted_assessments}
    
@assessment.post("/assessment/create") 
async def create_assessment(assessment: Assessment): 
    newAssessment = await createAssessment(assessment) 
    if newAssessment is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Assessment created", "data": MessageToDict(newAssessment)}

@assessment.put("/assessment/update")
async def update_assessment(assessmentId: str, assessment: Assessment, currentUser: AssessmentResponse = Depends(getCurrentUser)):
    response = await updateAssessment(assessmentId, assessment)
    if response is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Assessment updated", "data": MessageToDict(response)}

@assessment.delete("/assessment")
async def delete_assessment(assessmentId: str, currentUser: AssessmentResponse = Depends(getCurrentUser)):
    deletedAssessment = await deleteAssessment(assessmentId)
    if deletedAssessment is None:
        raise HTTPException(status_code=500, detail="Error occured")
    return {"message": "Assessment deleted successfully"}

@assessment.get("/questions")
async def get_questions():
    questions = load_questions()  # Call the function to load questions
    return {"data": questions}