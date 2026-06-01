"""
main.py
───────
FastAPI application — all CRUD routes for patient records.
Auto-creates MySQL table on startup.

Run with:
    uvicorn backend.main:app --reload --port 8000
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database   import engine, Base, get_db
from backend.models     import Patient
from backend.schemas    import PatientCreate, PatientUpdate, PatientResponse
from backend.ai_service import get_health_prediction

# ── Create all tables on startup ──────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title       = "MIRA — Medical Intelligence Robotic Automation",
    description = "Health prediction API using patient data and Groq AI.",
    version     = "1.0.0",
)


# ─────────────────────────────────────────────────────────────────────────────
#  CREATE  —  POST /patients
# ─────────────────────────────────────────────────────────────────────────────
@app.post(
    "/patients",
    response_model = PatientResponse,
    status_code    = status.HTTP_201_CREATED,
    summary        = "Create a new patient record",
)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):

    # Check duplicate email
    existing = db.query(Patient).filter(Patient.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail      = f"A patient with email '{payload.email}' already exists.",
        )

    # Call Groq AI with full patient context including age
    remarks = get_health_prediction(
        full_name   = payload.full_name,
        dob         = str(payload.dob),
        glucose     = payload.glucose,
        haemoglobin = payload.haemoglobin,
        cholesterol = payload.cholesterol,
    )

    # Save to DB
    patient = Patient(**payload.model_dump(), remarks=remarks)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


# ─────────────────────────────────────────────────────────────────────────────
#  READ ALL  —  GET /patients
# ─────────────────────────────────────────────────────────────────────────────
@app.get(
    "/patients",
    response_model = list[PatientResponse],
    summary        = "Retrieve all patient records",
)
def get_all_patients(db: Session = Depends(get_db)):
    return db.query(Patient).order_by(Patient.id).all()


# ─────────────────────────────────────────────────────────────────────────────
#  READ ONE  —  GET /patients/{id}
# ─────────────────────────────────────────────────────────────────────────────
@app.get(
    "/patients/{patient_id}",
    response_model = PatientResponse,
    summary        = "Retrieve a single patient by ID",
)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = f"Patient with id={patient_id} not found.",
        )
    return patient


# ─────────────────────────────────────────────────────────────────────────────
#  UPDATE  —  PUT /patients/{id}
# ─────────────────────────────────────────────────────────────────────────────
@app.put(
    "/patients/{patient_id}",
    response_model = PatientResponse,
    summary        = "Update a patient record and refresh AI prediction",
)
def update_patient(
    patient_id: int,
    payload:    PatientUpdate,
    db:         Session = Depends(get_db),
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = f"Patient with id={patient_id} not found.",
        )

    # Check email uniqueness if it changed
    if payload.email != patient.email:
        duplicate = db.query(Patient).filter(Patient.email == payload.email).first()
        if duplicate:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail      = f"Email '{payload.email}' is already used by another patient.",
            )

    # Re-generate AI remarks with updated patient context including age
    remarks = get_health_prediction(
        full_name   = payload.full_name,
        dob         = str(payload.dob),
        glucose     = payload.glucose,
        haemoglobin = payload.haemoglobin,
        cholesterol = payload.cholesterol,
    )

    # Apply all updates
    for field, value in payload.model_dump().items():
        setattr(patient, field, value)
    patient.remarks = remarks

    db.commit()
    db.refresh(patient)
    return patient


# ─────────────────────────────────────────────────────────────────────────────
#  DELETE  —  DELETE /patients/{id}
# ─────────────────────────────────────────────────────────────────────────────
@app.delete(
    "/patients/{patient_id}",
    status_code = status.HTTP_200_OK,
    summary     = "Delete a patient record",
)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = f"Patient with id={patient_id} not found.",
        )
    db.delete(patient)
    db.commit()
    return {"message": f"Patient id={patient_id} deleted successfully."}


# ─────────────────────────────────────────────────────────────────────────────
#  HEALTH CHECK  —  GET /
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/", summary="API health check")
def root():
    return {"status": "MIRA API is running", "docs": "/docs"}