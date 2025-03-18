import sqlite3
from datetime import datetime
import os
from typing import Optional, Any, List, TYPE_CHECKING
from sqlalchemy.orm import mapped_column, relationship, Mapped, DeclarativeBase
from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.ext.hybrid import hybrid_property
from apiGateway.base import Base

if TYPE_CHECKING:
    from services.courseService.db import Course

class Assessment(Base):
    __tablename__ = 'assessment'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(255), nullable=False)
    total_marks: Mapped[float] = mapped_column(nullable=False, default=0.0)
    question_paper: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True)
    
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'), nullable=False) # Many assessments - 1 course, M:1
    
    course: Mapped["Course"] = relationship("Course", back_populates='assessments')
    attempts: Mapped[List["AssessmentAttempt"]] = relationship("AssessmentAttempt", back_populates='assessment')
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
    
    assessment: Mapped[Assessment] = relationship("Assessment", back_populates='attempts')
    

currentPath = os.path.dirname(os.path.abspath(__file__))
class AssessmentDB:
    def __init__(self):
        # SQLite database file
        db_path = currentPath + '/assessments.db'
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Access rows as dictionaries
        self.cursor = self.conn.cursor()

        # SQL to create assessments table
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS assessments (
            assessmentId TEXT PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            courseId TEXT NOT NULL
        )
        '''
        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            print("Table 'assessments' created successfully.")
        except sqlite3.Error as e:
            print(f"Database error during table creation: {e}")
            self.conn.rollback()
    
    def createAssessment(self, assessmentObj):
        """Insert a new assessment into the database."""
        sql = '''INSERT INTO assessments (assessmentId, name, courseId) 
                 VALUES (?, ?, ?)'''
        try:
            self.cursor.execute(sql, assessmentObj)
            self.conn.commit()
            return assessmentObj[0]  # Return created assessment ID
        except sqlite3.Error as e:
            print(f"Database error during createAssessment: {e}")
            self.conn.rollback()
            return False

    def updateAssessment(self, assessmentObj):
        """Update the amount of an existing assessment by assessmentId."""
        sql = '''UPDATE assessments
                 SET name = ?, courseId=?
                 WHERE assessmentId = ?'''
        try:
            self.cursor.execute(sql, (assessmentObj['name'], assessmentObj['courseId'], assessmentObj['assessmentId']))
            self.conn.commit()
            return self.cursor.rowcount  # Number of rows affected
        except sqlite3.Error as e:
            print(f"Database error during updateAssessment: {e}")
            self.conn.rollback()
            return False

    def getAllAssessment(self):
        try:
            sql = '''SELECT * FROM assessments'''
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            if not rows:
                return None

            # Convert rows to a list of dictionaries with ISO 8601 timestamp strings
            assessments = []
            for row in rows:
                row_dict = dict(row)
                assessments.append(row_dict)
            # sorted_rows = sorted(rows, key=lambda row: datetime.strptime(row['transactionDate'], "%d/%m/%Y"))
            return assessments
        except sqlite3.Error as e:
            print(f"Database error during getAssessment: {e}")
            return False
        
    def getAssessment(self, name=None, courseid=None):
        try:
            # Start SQL query and parameters list
            sql = "SELECT * FROM assessments WHERE 1=1"
            params = []

            # Dynamic conditions based on provided filters
            if name:
                sql += " AND name = ?"
                params.append(name)
            
            if courseid:
                sql += " AND courseId = ?"
                params.append(courseid)
        
            
            # Execute the query
            self.cursor.execute(sql, tuple(params))
            rows = self.cursor.fetchall()

            # If no rows found, return None
            if not rows:
                return None

            # Convert rows to a list of dictionaries
            assessments = []
            for row in rows:
                row_dict = dict(row)
                assessments.append(row_dict)

            return assessments
        
        except sqlite3.Error as e:
            print(f"Database error during getAssessment: {e}")
            return False

    def deleteAssessment(self, assessmentId):
        """Delete an assessment by assessmentId."""
        sql = '''DELETE FROM assessments WHERE assessmentId = ?'''
        try:
            self.cursor.execute(sql, (assessmentId,))
            self.conn.commit()
            return self.cursor.rowcount  # Number of rows affected
        except sqlite3.Error as e:
            print(f"Database error during deleteAssessment: {e}")
            self.conn.rollback()
            return False

    def close(self):
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()
