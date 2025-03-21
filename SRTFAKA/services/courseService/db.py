import sqlite3
from datetime import datetime
import os
from sqlalchemy.orm import mapped_column, relationship, Mapped, DeclarativeBase, Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from apiGateway.base import Base, Industry
from services.assessmentService.db import Assessment
from services.certificateService.db import Certificate
from common.utils import generateRandomId
from contextlib import contextmanager
from sqlalchemy.sql import text

indFKey = 'industry.id'
courseFKey = 'course.id'
userFKey = 'user.id'
engine = create_engine("postgresql+psycopg2://postgres:password@job_database:5432/academy_db")
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Course(Base):
    __tablename__ = 'course'
    __table_args__ = {'extend_existing': True}
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[str] = mapped_column(String(255))
    
    # FK
    industry_id: Mapped[int] = mapped_column(ForeignKey('industry.id'))
    cert_id: Mapped[int] = mapped_column(nullable=True)    # 1 to 1 RS 
    
    students_enrolled: Mapped[list['CourseProgress']] = relationship(back_populates='course_info')
    assessments: Mapped[list['Assessment']] = relationship()
    certificate: Mapped['Certificate'] = relationship()
    industry: Mapped['Industry'] = relationship()
    
class CourseProgress(Base):
    """Tracks the progress of the student enrolled in the course.

    Args:
        Base (_type_): _description_
        
    Parameters:
        course_info (Course): _Information about the course stored in the Course class obj_
    """
    __tablename__ = 'course_progress'
    id: Mapped[int] = mapped_column(primary_key=True)
    cleared: Mapped[bool] = mapped_column(nullable=False,default=False) # flip to true once they click through the screen, allows student eligibility to try assessment
    
    # FK
    student_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'), nullable=False)
    
    course_info: Mapped['Course'] = relationship(back_populates='students_enrolled')
    
    
    
    
    


currentPath = os.path.dirname(os.path.abspath(__file__))

class CourseProgressDB:
    def __init__(self):
        self.session = SessionLocal()

    def joinCourse(self, cleared: bool, student_id: int, course_id: int):
        """User joins a course, insert into the database"""
        
        sql = text("""
                   INSERT INTO course_progress (
                   cleared,
                   student_id,
                   course_id)
                   VALUES (
                   :cleared,
                   :student_id,
                   :course_id
                   )
                   RETURNING id;
                   """)
        values = {
            "cleared": cleared,
            "student_id": student_id,
            "course_id": course_id
        }

        try:
            result = self.session.execute(sql, values)
            self.session.commit()
            course_progress_id = result.scalar()
            print(course_progress_id)
            return course_progress_id
        except SQLAlchemyError as e:
            print(f"ERROr in joinCourse: {e}")
            self.session.rollback()
            return None
    
    def updateCourseProgress(self, course_progress_id: int, cleared: bool):
        """Update course progress using course_progress_id"""

        sql = text("""
            UPDATE course_progress
            SET cleared = :cleared
            WHERE id = :course_progress_id
            RETURNING id;
        """)

        values = {
            "cleared": cleared,
            "course_progress_id": course_progress_id
        }

        try:
            result = self.session.execute(sql, values)
            self.session.commit()
            updated_id = result.scalar()
            
            if updated_id:
                print(f"Updated course_progress ID: {updated_id}")
            else:
                print("No matching record found to update.")

            return updated_id
        except SQLAlchemyError as e:
            print(f"Error in update_course_progress: {e}")
            self.session.rollback()
            return None


class CourseDB:
    def __init__(self):
        self.session = SessionLocal()
    
    def createCourse(self, name: String, details: String, industry_id: int, cert_id: int):
        """Insert a new course into the database."""
        new_course = Course(name=name, details=details, industry_id=industry_id, cert_id=cert_id)
        try:
            self.session.add(new_course)
            self.session.commit()
            self.session.refresh(new_course)
            return new_course.id
        except SQLAlchemyError.Error as e:
            self.session.rollback()
            print(f"Database error during createCourse: {e}")
            return None

    def updateCourse(self, courseObj):
        """Update the amount of an existing course by courseId."""
        sql = '''UPDATE courses
                 SET name = ?, instructor=?
                 WHERE courseId = ?'''
        try:
            self.cursor.execute(sql, (courseObj['name'], courseObj['instructor'], courseObj['courseId']))
            self.conn.commit()
            return self.cursor.rowcount  # Number of rows affected
        except sqlite3.Error as e:
            print(f"Database error during updateCourse: {e}")
            self.conn.rollback()
            return False

    def getAllCourse(self):
        try:
            sql = text("""
            SELECT 
                course.id,
                course.name,
                course.details,
                course.industry_id,
                course.cert_id,
                industry.name AS industry_name  -- Add this line to select the name of the industry
            FROM course
            JOIN industry ON course.industry_id = industry.id
            """)            
            result = self.session.execute(sql)
            courses = result.mappings().all()

            return courses if courses else []
        except SQLAlchemyError as e:
            print(f"Database error during getAllCourse: {e}")
            return []
        
    def getCourseById(self, id: int):
        try:
            sql = text("""
            SELECT 
                course.id,
                course.name,
                course.details,
                course.industry_id,
                course.cert_id,
                industry.name AS industry_name
            FROM course
            JOIN industry ON course.industry_id = industry.id
            WHERE course.id = :id
            """)
            result = self.session.execute(sql, {"id": id})
            course = result.mappings().first()  # Using first() to get a single result

            return course if course else None
        except SQLAlchemyError as e:
            print(f"Database error during getCourse: {e}")
            return None


    def deleteCourse(self, courseId):
        """Delete an course by courseId."""
        sql = '''DELETE FROM courses WHERE courseId = ?'''
        try:
            self.cursor.execute(sql, (courseId,))
            self.conn.commit()
            return self.cursor.rowcount  # Number of rows affected
        except sqlite3.Error as e:
            print(f"Database error during deleteCourse: {e}")
            self.conn.rollback()
            return False

    def close(self):
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()
