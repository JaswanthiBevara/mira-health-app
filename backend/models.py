"""
models.py
─────────
SQLAlchemy ORM model → maps to `patients` table in MySQL.
Running the app for the first time auto-creates the table.
"""

from sqlalchemy import Column, Integer, String, Date, Float, Text
from backend.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id           = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name    = Column(String(150), nullable=False)
    dob          = Column(Date,        nullable=False)        # Date of birth
    email        = Column(String(200), nullable=False, unique=True)
    glucose      = Column(Float,       nullable=False)        # mg/dL
    haemoglobin  = Column(Float,       nullable=False)        # g/dL
    cholesterol  = Column(Float,       nullable=False)        # mg/dL
    remarks      = Column(Text,        nullable=True)         # AI-generated prediction

    def __repr__(self):
        return f"<Patient id={self.id} name={self.full_name}>"
