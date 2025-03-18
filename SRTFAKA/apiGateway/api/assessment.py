from fastapi import APIRouter, Depends, HTTPException, Query
from ..gRPCHandler import getAssessment, getAssessmentAttempts, addAssessmentAttempt
from google.protobuf.json_format import MessageToDict
from ..models import AssessmentResponse, Assessment
from ..auth import getCurrentUser
from ...generated import assessment_pb2
from pydantic import BaseModel
from typing import Optional

# Define the Pydantic model for AssessmentAttemptData here
class AssessmentAttemptData(BaseModel):
    attemptId: int
    earnedMarks: float
    attemptedOn: str
    remarks: Optional[str] = None
    studentId: int  # Ensure this field is included
    assessmentId: int  # Ensure this field is included

assessment = APIRouter()

@assessment.get("/assessment")
async def get_assessment():
    # Get the protobuf message
    response = await getAssessment()
    # Convert the protobuf message to a dictionary
    assessments = MessageToDict(response)
    return {"message": "Assessments retrieved", "data": assessments}

@assessment.get("/assessment/attempts")
async def get_assessment_attempts():
    # Get the protobuf message
    response = await getAssessmentAttempts()
    # Convert the protobuf message to a dictionary
    attempts = MessageToDict(response)
    return {"message": "Assessment attempts retrieved", "data": attempts}

@assessment.post("/assessment/attempts")
async def add_assessment(attempt: AssessmentAttemptData):
    """Add a new assessment attempt."""
    # Convert the Pydantic model to Protobuf message
    attempt_proto = assessment_pb2.AssessmentAttemptData(
        earnedMarks=attempt.earnedMarks,
        attemptedOn=attempt.attemptedOn,
        remarks=attempt.remarks,
        studentId=attempt.studentId,  # Include studentId
        assessmentId=attempt.assessmentId  # Include assessmentId
    )
    
    # Call the gRPC service to add the assessment attempt
    response = await addAssessmentAttempt(attempt_proto)
    
    if response is None:
        raise HTTPException(status_code=500, detail="Error occurred while adding assessment attempt")
    
    # Convert the Protobuf response to a dictionary
    return {"message": "Assessment attempt added", "data": MessageToDict(response)}