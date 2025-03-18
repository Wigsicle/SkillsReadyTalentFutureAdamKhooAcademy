import os
from typing import Any, List, TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship
from sqlalchemy.types import Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
# this file holds any models that are accessed by multiple services 

if TYPE_CHECKING:
    from services.jobService.db import Application, Company
    from services.accountService.db import User
    from services.courseService.db import Course

currentPath = os.path.dirname(os.path.abspath(__file__))

class Base(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSON}
    
metadata = Base.metadata

class Industry(Base):
    """Industry the company is part of."""
    __tablename__ = "industry"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    short_name: Mapped[str] = mapped_column(String(255), nullable=False)

    applications: Mapped[List["Application"]] = relationship("Application", back_populates='industry')
    companies: Mapped[List["Company"]] = relationship("Company", back_populates='industry')
    courses: Mapped[List["Course"]] = relationship("Course", back_populates='industry')


class Country(Base):
    __tablename__ = "country"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    short_name: Mapped[str] = mapped_column(String(255), nullable=False)

    companies: Mapped[List["Company"]] = relationship("Company", back_populates='country')
    residents: Mapped[List["User"]] = relationship("User", back_populates='country')