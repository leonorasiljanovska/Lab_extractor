import os
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.templating import Jinja2Templates

from ..core.templates import templates
from ..db_models import Patient, LabTest
from ..models import ExtractResponse, LaboratoryResults
from ..utils import extract_lab_results, generate_patient_id
from fastapi import Request, Form

from fastapi import Form

from fastapi import Form, Request
from fastapi.responses import RedirectResponse
from app.db import SessionLocal

router = APIRouter()


@router.post("/extract-lab-results", response_model=ExtractResponse)
async def extract_laboratory_results(file: UploadFile = File(...)):
    """Extract laboratory results from an uploaded image file"""

    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Extract results
    result = await extract_lab_results(file)

    if result["success"] and result["results"]:
        return ExtractResponse(
            success=True,
            results=LaboratoryResults(**result["results"]),
            error=None
        )
    else:
        return ExtractResponse(
            success=False,
            results=None,
            error=result.get("error", "Unknown error occurred")
        )


@router.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Lab Report Extractor API is running"}


def parse_test_date(date_str: str):
    formats = [
        "%Y-%m-%d %H:%M",   # 2022-05-07 10:30
        "%Y-%m-%d",         # 2022-05-07
        "%d-%b-%Y",         # 12-Aug-2014
        "%d-%B-%Y",         # 12-August-2014 (in case full month name)
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None  # or raise an error for invalid format




@router.post("/save-edited")
async def save_edited_lab_results(
        request: Request,
        patient_id: str = Form(...),
        gender: str = Form(None),
        hospital_name: str = Form(None),
        doctor_name: str = Form(None),
        clinic_name: str = Form(None),
        test_date: str = Form(None),
        report_date: str = Form(None),
        tests_count: int = Form(...),
):
    form_data = await request.form()

    tests = []

    # Parse test date if provided
    test_date_obj = parse_test_date(test_date) if test_date else None

    for i in range(tests_count):
        parameter = form_data.get(f"parameter_{i}")
        value = form_data.get(f"value_{i}")
        unit = form_data.get(f"unit_{i}")
        reference_range = form_data.get(f"reference_range_{i}")
        status = form_data.get(f"status_{i}")

        try:
            value = float(value)
        except (ValueError, TypeError):
            value = None

        tests.append({
            "parameter": parameter,
            "value": value,
            "unit": unit,
            "reference_range": reference_range,
            "status": status
        })

    db = SessionLocal()

    # Check if patient exists, else create
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        patient = Patient(
            id=patient_id,
            gender=gender,
            hospital_name=hospital_name
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)

    db.query(LabTest).filter(
        LabTest.patient_id == patient_id,
        LabTest.test_date == test_date_obj
    ).delete()

    db.commit()

    # Insert new test entries
    for test in tests:
        lab_test = LabTest(
            patient_id=patient.id,
            parameter=test["parameter"],
            value=test["value"],
            unit=test["unit"],
            reference_range=test["reference_range"],
            status=test["status"],
            test_date=test_date_obj
        )
        db.add(lab_test)

    db.commit()
    db.close()

    return RedirectResponse(url="/", status_code=303)
