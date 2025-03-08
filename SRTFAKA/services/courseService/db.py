import sqlite3
from datetime import datetime
import os
from sqlalchemy.orm import mapped_column, relationship, Mapped, DeclarativeBase
from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from apiGateway.base import Base, Industry
from services.assessmentService.db import Assessment
from certificateService.db import Certificate

class Course(Base):
    __tablename__ = 'course'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[str] = mapped_column(String(255))
    
    # FK
    industry_id: Mapped[int] = mapped_column(ForeignKey('industry.id'))
    cert_id: Mapped[int] = mapped_column(nullable=False)    # 1 to 1 RS 
    
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
class CourseDB:
    def __init__(self):
        # SQLite database file
        db_path = currentPath + '/courses.db'
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Access rows as dictionaries
        self.cursor = self.conn.cursor()

        # SQL to create courses table
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS courses (
            courseId TEXT PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            instructor TEXT NOT NULL
        )
        '''
        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            print("Table 'courses' created successfully.")
        except sqlite3.Error as e:
            print(f"Database error during table creation: {e}")
            self.conn.rollback()
    
    def createCourse(self, courseObj):
        """Insert a new course into the database."""
        sql = '''INSERT INTO courses (courseId, name, instructor) 
                 VALUES (?, ?, ?)'''
        try:
            self.cursor.execute(sql, courseObj)
            self.conn.commit()
            return courseObj[0]  # Return created course ID
        except sqlite3.Error as e:
            print(f"Database error during createCourse: {e}")
            self.conn.rollback()
            return False

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
            sql = '''SELECT * FROM courses'''
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            if not rows:
                return None

            # Convert rows to a list of dictionaries with ISO 8601 timestamp strings
            courses = []
            for row in rows:
                row_dict = dict(row)
                courses.append(row_dict)
            # sorted_rows = sorted(rows, key=lambda row: datetime.strptime(row['transactionDate'], "%d/%m/%Y"))
            return courses
        except sqlite3.Error as e:
            print(f"Database error during getCourse: {e}")
            return False
        
    def getCourse(self, name=None, instructor=None):
        try:
            # Start SQL query and parameters list
            sql = "SELECT * FROM courses WHERE 1=1"
            params = []

            # Dynamic conditions based on provided filters
            if name:
                sql += " AND name = ?"
                params.append(name)
            
            if instructor:
                sql += " AND instructor = ?"
                params.append(instructor)
        
            
            # Execute the query
            self.cursor.execute(sql, tuple(params))
            rows = self.cursor.fetchall()

            # If no rows found, return None
            if not rows:
                return None

            # Convert rows to a list of dictionaries
            courses = []
            for row in rows:
                row_dict = dict(row)
                courses.append(row_dict)

            return courses
        
        except sqlite3.Error as e:
            print(f"Database error during getCourse: {e}")
            return False

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
