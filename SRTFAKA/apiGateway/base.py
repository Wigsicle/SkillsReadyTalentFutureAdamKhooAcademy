import os
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import declarative_base
# this file holds any models that are accessed by multiple services 

currentPath = os.path.dirname(os.path.abspath(__file__))
Base = declarative_base()
metadata = Base.metadata

class Industry(Base):
    """Industry the company is part of."""
    __tablename__ = "industry"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    short_name: Mapped[str] = mapped_column(String(255), nullable=False)

class Country(Base):
    __tablename__ = "country"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    short_name: Mapped[str] = mapped_column(String(255), nullable=False)