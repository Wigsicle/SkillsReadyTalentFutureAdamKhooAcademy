from datetime import datetime
from typing import Optional, Any
from sqlalchemy.orm import mapped_column, relationship, Mapped, DeclarativeBase
from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.hybrid import hybrid_property

DATABASE_URL = "postgresql+psycopg2://postgres:password@127.0.0.1:5433/academy_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Assessment(Base):
    __tablename__ = 'assessment'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    total_marks: Mapped[float] = mapped_column(nullable=False, default=0.0)
    question_paper: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True)
    
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'), nullable=False)  # Many assessments - 1 course, M:1
    
    # Use a string reference for the relationship
    attempts: Mapped[list["AssessmentAttempt"]] = relationship("AssessmentAttempt", back_populates="assessment")
    
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
    
    # Foreign Keys
    student_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)  # Many Attempts - 1 Student, M:1
    assessment_id: Mapped[int] = mapped_column(ForeignKey('assessment.id'), nullable=False) # Many Attempts to 1 Assessment, M:1
    
    assessment: Mapped[Assessment] = relationship("Assessment", back_populates="attempts")
    

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