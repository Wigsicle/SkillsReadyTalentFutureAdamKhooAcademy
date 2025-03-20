from fastapi import APIRouter, Depends, HTTPException, Query
from ..gRPCHandler import getAssessment, getAssessmentAttempts, addAssessmentAttempt
from google.protobuf.json_format import MessageToDict
from ..models import AssessmentResponse, Assessment, UserCertificate, AssessmentAttemptData
from ..auth import getCurrentUser
from ...generated import assessment_pb2
from pydantic import BaseModel
from typing import Optional
from .certificate import issue_certificate_api


assessment = APIRouter()

@assessment.get("/assessment")
async def get_assessment(currentUser: AssessmentResponse = Depends(getCurrentUser)):
    # Get the protobuf message
    response = await getAssessment()
    # Convert the protobuf message to a dictionary
    assessments = MessageToDict(response)
    return {"message": "Assessments retrieved", "data": assessments}

@assessment.get("/assessment/attempts")
async def get_assessment_attempts(currentUser: AssessmentResponse = Depends(getCurrentUser)):
    # Get the protobuf message
    response = await getAssessmentAttempts()
    # Convert the protobuf message to a dictionary
    attempts = MessageToDict(response)
    return {"message": "Assessment attempts retrieved", "data": attempts}

@assessment.post("/assessment/attempts")
async def add_assessment(attempt: AssessmentAttemptData, currentUser: AssessmentResponse = Depends(getCurrentUser)):
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
    certResonse = await issue_certificate_api(UserCertificate(userId=attempt.studentId, certId=attempt.certId))  
    if response is None and certResonse is None:
        raise HTTPException(status_code=500, detail="Error occurred while adding assessment attempt")
    
    # Convert the Protobuf response to a dictionary
    return {"message": "Assessment attempt added", "data": MessageToDict(response)}