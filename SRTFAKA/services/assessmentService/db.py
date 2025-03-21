from datetime import datetime
import os
from typing import Optional, Any, List, TYPE_CHECKING
from sqlalchemy.orm import mapped_column, relationship, Mapped, DeclarativeBase
from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.hybrid import hybrid_property

DATABASE_URL = "postgresql+psycopg2://postgres:password@127.0.0.1:5433/academy_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if TYPE_CHECKING:
    from services.courseService.db import Course
    from services.accountService.db import User

class Assessment(Base):
    __tablename__ = 'assessment'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    total_marks: Mapped[float] = mapped_column(nullable=False, default=0.0)
    question_paper: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True)
    
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'), nullable=False)  # Many assessments - 1 course, M:1
    
    # Use a string reference for the relationship
    attempts: Mapped[list["AssessmentAttempt"]] = relationship("AssessmentAttempt", back_populates="assessment")
    
    course: Mapped["Course"] = relationship("Course", back_populates='assessments')
    attempts: Mapped[List["AssessmentAttempt"]] = relationship("AssessmentAttempt", back_populates='assessment')
    # list of attempts that markers can mark
     


class AssessmentAttempt(Base):
    __tablename__ = 'assessment_attempt'
    id: Mapped[int] = mapped_column(primary_key=True)
    earned_marks: Mapped[float] = mapped_column(nullable=False)
    attempted_on: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    remarks: Mapped[str] = mapped_column(String(255), nullable=True)
    
    #student_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    student_id: Mapped[int] = mapped_column(Integer, nullable=False)  # Just an integer
    
    # Add assessment_id as a foreign key to maintain the relationship
    assessment_id: Mapped[int] = mapped_column(ForeignKey('assessment.id'), nullable=False)  # Foreign key to assessment

    @hybrid_property
    def score_str(self) -> str:
        result = ""
        if self.earned_marks is not None:
            result = f"{self.earned_marks}/{self.total_marks}"  # Adjusted to use total_marks directly
        return result
    
    #FK
    student_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)  # Many Attempts - 1 Student, M:1
    assessment_id: Mapped[int] = mapped_column(ForeignKey('assessment.id'), nullable=False) # Many Attempts to 1 Assessment, M:1
    
    student: Mapped["User"] = relationship("User", back_populates='assess_attempts')
    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates='attempts')
    

currentPath = os.path.dirname(os.path.abspath(__file__))
class AssessmentDB:
    def __init__(self):
        self.session = SessionLocal()

    def getAllAssessment(self):
       try:
           assessments = self.session.query(Assessment).all()
           for assessment in assessments:
               print(f"Retrieved Assessment: {assessment.id}, {assessment.name}, {assessment.course_id}, {assessment.total_marks}")
           return assessments
       except Exception as e:
           print(f"Database error during getAllAssessment: {e}")
           return None
       finally:
           self.session.close()

    def getAllAssessmentAttempts(self):
        try:
            attempts = self.session.query(AssessmentAttempt).all()
            for attempt in attempts:
                print(f"Retrieved Assessment Attempt: ID={attempt.id}, Earned Marks={attempt.earned_marks}, Attempted On={attempt.attempted_on}, Remarks={attempt.remarks}")
            return attempts
        except Exception as e:
            print(f"Database error during getAllAssessmentAttempts: {e}")
            return None
        finally:
            self.session.close()