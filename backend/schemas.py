"""
schemas.py
──────────
Pydantic models for request validation and response serialization.
FastAPI uses these to auto-validate incoming JSON and generate API docs.
"""

import re
from datetime import date
from pydantic import BaseModel, EmailStr, field_validator


# ── Shared validators ─────────────────────────────────────────────────────────
class PatientBase(BaseModel):
    full_name:   str
    dob:         date
    email:       str
    glucose:     float
    haemoglobin: float
    cholesterol: float

    @field_validator("full_name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Full name cannot be empty.")
        return v.strip()

    @field_validator("email")
    @classmethod
    def valid_email(cls, v):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email address format.")
        return v.lower().strip()

    @field_validator("dob")
    @classmethod
    def dob_not_future(cls, v):
        if v >= date.today():
            raise ValueError("Date of birth cannot be today or a future date.")
        return v

    @field_validator("glucose", "haemoglobin", "cholesterol")
    @classmethod
    def blood_values_positive(cls, v):
        if v <= 0:
            raise ValueError("Blood test values must be positive numbers.")
        return v


# ── Request schemas ───────────────────────────────────────────────────────────
class PatientCreate(PatientBase):
    """Used when creating a new patient (POST)."""
    pass


class PatientUpdate(PatientBase):
    """Used when updating an existing patient (PUT)."""
    pass


# ── Response schema ───────────────────────────────────────────────────────────
class PatientResponse(PatientBase):
    """Returned to the client — includes DB-generated fields."""
    id:      int
    remarks: str | None = None

    model_config = {"from_attributes": True}  # Allows ORM → Pydantic conversion
