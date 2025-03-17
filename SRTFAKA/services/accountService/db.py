import sqlite3
import os
import pathlib
from sqlalchemy.orm import mapped_column, relationship, Mapped, DeclarativeBase
from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from apiGateway.base import Base, Country
from services.jobService.db import Application
from certificateService.db import UserCertificate
from services.courseService.db import CourseProgress

engine = create_engine("postgresql+psycopg2://postgres:password@127.0.0.1:5433/academy_db")
currentPath = os.path.dirname(os.path.abspath(__file__))

class UserType(Base):
    __tablename__ = 'user_type'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String(255), nullable=False)

class User(Base):
    """User profile"""
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)

    #FK
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey('country.id'))
    user_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('user_type.id'))
    #RS
    country: Mapped[Country] = relationship("Country")
    user_type: Mapped[UserType] = relationship("UserType")
    
    # RS objects connected from other classes
    applications: Mapped[list['Application']] = relationship()  #jobService
    certs_attained: Mapped[list['UserCertificate']] = relationship()    #certService
    courses_enrolled: Mapped[list['CourseProgress']] = relationship()   #courseService


class AccountDB:
    def __init__(self):
        # SQLite database file (creates a new file if it doesn't exist)
        db_path = currentPath + '/accounts.db'
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # To access rows as dictionaries
        self.cursor = self.conn.cursor()

        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS accounts (
            accountId TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            accountStatus BOOLEAN NOT NULL
        );
        '''
        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            print("Table 'accounts' created successfully.")
        except sqlite3.Error as e:
            print(f"Database error during table creation: {e}")
            self.conn.rollback()
    
    def getAccountById(self, accountId):
        """Fetch account details by accountId."""
        try:
            sql = 'SELECT * FROM accounts WHERE accountId = ?'
            self.cursor.execute(sql, (accountId,))
            result = self.cursor.fetchone()
            return dict(result) if result else False
        except sqlite3.Error as e:
            print(f"Database error during getAccountById: {e}")
            self.conn.rollback()
            return False

    def getAccountByUsername(self, username):
        """Fetch account details by username."""
        try:
            sql = 'SELECT * FROM accounts WHERE username = ?'
            self.cursor.execute(sql, (username,))
            result = self.cursor.fetchone()
            return dict(result) if result else False
        except sqlite3.Error as e:
            print(f"Database error during getAccountByUsername: {e}")
            self.conn.rollback()
            return False

    def createAccount(self, accountData):
        """Insert a new account into the database."""
        sql = '''
            INSERT INTO accounts (accountId, name, username, password, accountStatus) 
            VALUES (?, ?, ?, ?, ?)
        '''
        try:
            self.cursor.execute(sql, accountData)
            self.conn.commit()
            return accountData[0]  # Return created account's accountId
        except sqlite3.Error as e:
            print(f"Database error during createAccount: {e}")
            self.conn.rollback()
            return False

    def updateAccount(self, accountId, updateData):
        """Update account information for the given accountId."""
        sql = '''
            UPDATE accounts 
            SET name = ?, password = ?
            WHERE accountId = ?
        '''
        try:
            self.cursor.execute(sql, (updateData['name'], updateData['password'], accountId))
            self.conn.commit()
            return self.cursor.rowcount > 0  # True if the account was updated
        except sqlite3.Error as e:
            print(f"Database error during updateAccount: {e}")
            self.conn.rollback()
            return False

    def deleteAccount(self, accountId):
        """Delete account by accountId."""
        sql = 'DELETE FROM accounts WHERE accountId = ?'
        try:
            self.cursor.execute(sql, (accountId,))
            self.conn.commit()
            return self.cursor.rowcount > 0  # True if the account was deleted
        except sqlite3.Error as e:
            print(f"Database error during deleteAccount: {e}")
            self.conn.rollback()
            return False
    
    def close(self):
        self.cursor.close()
        self.conn.close()
