import sqlite3
from datetime import datetime
import os

currentPath = os.path.dirname(os.path.abspath(__file__))
class JobDB:
    def __init__(self):
        # SQLite database file
        db_path = currentPath + '/jobs.db'
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Access rows as dictionaries
        self.cursor = self.conn.cursor()

        # SQL to create jobs table
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS jobs (
            jobId TEXT PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            company TEXT NOT NULL
        )
        '''
        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            print("Table 'jobs' created successfully.")
        except sqlite3.Error as e:
            print(f"Database error during table creation: {e}")
            self.conn.rollback()
    
    def createJob(self, jobObj):
        """Insert a new job into the database."""
        sql = '''INSERT INTO jobs (jobId, name, company) 
                 VALUES (?, ?, ?)'''
        try:
            self.cursor.execute(sql, jobObj)
            self.conn.commit()
            return jobObj[0]  # Return created job ID
        except sqlite3.Error as e:
            print(f"Database error during createJob: {e}")
            self.conn.rollback()
            return False

    def updateJob(self, jobObj):
        """Update the amount of an existing job by jobId."""
        sql = '''UPDATE jobs
                 SET name = ?, company=?
                 WHERE jobId = ?'''
        try:
            self.cursor.execute(sql, (jobObj['name'], jobObj['company'], jobObj['jobId']))
            self.conn.commit()
            return self.cursor.rowcount  # Number of rows affected
        except sqlite3.Error as e:
            print(f"Database error during updateJob: {e}")
            self.conn.rollback()
            return False

    def getAllJob(self):
        try:
            sql = '''SELECT * FROM jobs'''
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            if not rows:
                return None

            # Convert rows to a list of dictionaries with ISO 8601 timestamp strings
            jobs = []
            for row in rows:
                row_dict = dict(row)
                jobs.append(row_dict)
            # sorted_rows = sorted(rows, key=lambda row: datetime.strptime(row['transactionDate'], "%d/%m/%Y"))
            return jobs
        except sqlite3.Error as e:
            print(f"Database error during getJob: {e}")
            return False
        
    def getJob(self, name=None, company=None):
        try:
            # Start SQL query and parameters list
            sql = "SELECT * FROM jobs WHERE 1=1"
            params = []

            # Dynamic conditions based on provided filters
            if name:
                sql += " AND name = ?"
                params.append(name)
            
            if company:
                sql += " AND company = ?"
                params.append(company)
        
            
            # Execute the query
            self.cursor.execute(sql, tuple(params))
            rows = self.cursor.fetchall()

            # If no rows found, return None
            if not rows:
                return None

            # Convert rows to a list of dictionaries
            jobs = []
            for row in rows:
                row_dict = dict(row)
                jobs.append(row_dict)

            return jobs
        
        except sqlite3.Error as e:
            print(f"Database error during getJob: {e}")
            return False

    def deleteJob(self, jobId):
        """Delete an job by jobId."""
        sql = '''DELETE FROM jobs WHERE jobId = ?'''
        try:
            self.cursor.execute(sql, (jobId,))
            self.conn.commit()
            return self.cursor.rowcount  # Number of rows affected
        except sqlite3.Error as e:
            print(f"Database error during deleteJob: {e}")
            self.conn.rollback()
            return False

    def close(self):
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()
