import sqlite3
from datetime import datetime
import os
from typing import Optional, Any, List
from sqlalchemy.orm import mapped_column, relationship, Mapped, DeclarativeBase
from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey, JSON, text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker
from ...apiGateway.base import Base

# PostgreSQL database connection
db_url = os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:password@127.0.0.1:5433/academy_db')
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

class Assessment(Base):
    __tablename__ = 'assessment'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(255), nullable=False)
    total_marks: Mapped[float] = mapped_column(nullable=False, default=0.0)
    question_paper: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True)
    
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'), nullable=False) # Many assessments - 1 course, M:1
    
    # list of attempts that markers can mark

class AssessmentAttempt(Base):
    __tablename__ = 'assessment_attempt'
    id: Mapped[int] = mapped_column(primary_key=True)
    earned_marks: Mapped[Optional[float]] = mapped_column()    # marks given to an attempt of the assessment
    attempted_on: Mapped[datetime] = mapped_column(default=datetime.now())
    remarks: Mapped[Optional[str]] = mapped_column(String(255))
    
    @hybrid_property
    def score_str(self) -> str:
        result = ""
        if self.earned_marks is not None:
            result = f"{self.earned_marks}/{self.assessment.total_marks}"
            
        return result
    
    #FK
    student_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)  # Many Attempts - 1 Student, M:1
    assessment_id: Mapped[int] = mapped_column(ForeignKey('assessment.id'), nullable=False) # Many Attempts to 1 Assessment, M:1
    
    assessment: Mapped[Assessment] = relationship
    

class AssessmentDB:
    def __init__(self):
        self.session = Session()  # Create a new session

        # Create assessments table if it doesn't exist
        self.session.execute(text('''
        CREATE TABLE IF NOT EXISTS assessment (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            total_marks FLOAT NOT NULL DEFAULT 0.0,
            question_paper JSON,
            course_id INTEGER NOT NULL REFERENCES course(id)
        )
        '''))
        self.session.commit()
        print("Table 'assessment' created successfully.")

    def createAssessment(self, assessmentObj):
        """Insert a new assessment into the database."""
        new_assessment = Assessment(name=assessmentObj['name'], total_marks=assessmentObj['total_marks'], course_id=assessmentObj['course_id'])
        self.session.add(new_assessment)
        self.session.commit()
        return new_assessment.id  # Return created assessment ID

    def updateAssessment(self, assessmentObj):
        """Update an existing assessment by assessmentId."""
        assessment = self.session.query(Assessment).filter_by(id=assessmentObj['id']).first()
        if assessment:
            assessment.name = assessmentObj['name']
            assessment.total_marks = assessmentObj['total_marks']
            assessment.course_id = assessmentObj['course_id']
            self.session.commit()
            return 1  # Number of rows affected
        return 0

    def getAllAssessment(self) -> List[Assessment]:
        assessments = self.session.query(Assessment).all()
        return [dict(id=a.id, name=a.name, total_marks=a.total_marks, course_id=a.course_id) for a in assessments]


    def getAssessment(self, name=None, courseid=None):
        query = self.session.query(Assessment)
        if name:
            query = query.filter(Assessment.name == name)
        if courseid:
            query = query.filter(Assessment.course_id == courseid)
        assessments = query.all()
        return [dict(id=a.id, name=a.name, total_marks=a.total_marks, course_id=a.course_id) for a in assessments]

    def deleteAssessment(self, assessmentId):
        """Delete an assessment by assessmentId."""
        assessment = self.session.query(Assessment).filter_by(id=assessmentId).first()
        if assessment:
            self.session.delete(assessment)
            self.session.commit()
            return 1  # Number of rows affected
        return 0

    def close(self):
        """Close the database connection."""
        self.session.close()
