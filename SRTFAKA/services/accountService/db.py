import sqlite3
import os
import pathlib
from sqlalchemy.orm import mapped_column, relationship, Mapped, DeclarativeBase, sessionmaker
from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from typing import Optional
from apiGateway.base import Base, Country
# from services.jobService.db import Application
# from services.certificateService.db import UserCertificate
# from services.courseService.db import CourseProgress
import traceback

engine = create_engine("postgresql+psycopg2://postgres:password@job_database:5432/academy_db")
currentPath = os.path.dirname(os.path.abspath(__file__))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class UserType(Base):
    __tablename__ = 'user_type'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String(255), nullable=False)

class User(Base):
    """User profile"""
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
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
    # applications: Mapped[Optional[list['Application']]] = relationship()  #jobService
    # certs_attained: Mapped[list['UserCertificate']] = relationship()    #certService
    # courses_enrolled: Mapped[list['CourseProgress']] = relationship()   #courseService


class AccountDB:
    """Account database management using SQLAlchemy."""
    def __init__(self):
        self.session = SessionLocal()
    
    def getAccountById(self, accountId):
        """Fetch account details by accountId using SQLAlchemy."""
        try:
            account = self.session.query(User).filter(User.id == accountId).first()
            return account if account else None
        except Exception as e:
            print(f"Error during getAccountById: {e}")
            return None

    def getAccountByEmail(self, email):
        """Fetch account details by username using SQLAlchemy."""
        try:
            account = self.session.query(User).filter(User.email == email).first()
            return account if account else None
        except Exception as e:
            print(f"Error during getAccountByEmail: {e}")
            return None

    def createAccount(self, accountData):
        """Insert a new account into the database using SQLAlchemy."""
        try:
            print(accountData)
            new_account = User(
                first_name=accountData[1],
                last_name=accountData[2],
                email=accountData[3], 
                password=accountData[4],
                country_id=accountData[5],
                address=accountData[6],
                user_type_id=accountData[7]
            )
            self.session.add(new_account)
            self.session.commit()
            return new_account.id  # Return created account's id
        except Exception as e:
            traceback.print_exc()
            print(f"Error during createAccount: {e}")
            self.session.rollback()
            return None

    def updateAccount(self, accountId, updateData):
        """Update account information using SQLAlchemy."""
        try:
            account = self.session.query(User).filter(User.id == accountId).first()
            if account:
                account.first_name = updateData['firstname']
                account.last_name = updateData['lastname']
                account.password = updateData['password']
                account.country_id = updateData['country_id']
                account.address = updateData['address']
                self.session.commit()
                return True
            return False
        except Exception as e:
            print(f"Error during updateAccount: {e}")
            self.session.rollback()
            return False

    def deleteAccount(self, accountId):
        """Delete account by accountId using SQLAlchemy."""
        try:
            account = self.session.query(User).filter(User.id == accountId).first()
            if account:
                self.session.delete(account)
                self.session.commit()
                return True
            return False
        except Exception as e:
            print(f"Error during deleteAccount: {e}")
            self.session.rollback()
            return False

    def close(self):
        """Close the session."""
        self.session.close()

