from fastapi import APIRouter, Request, UploadFile, Form
from fastapi.responses import HTMLResponse
from app.core.templates import templates
from app.utils import extract_lab_results
import os

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


# @router.post("/view-results", response_class=HTMLResponse)
# async def show_results(request: Request, file: UploadFile = Form(...)):
#     result = await extract_lab_results(file)
#     return templates.TemplateResponse("results.html", {
#         "request": request,
#         "results": result["results"]
#     })
from app.utils import generate_patient_id


@router.post("/view-results", response_class=HTMLResponse)
async def show_results(request: Request, file: UploadFile = Form(...)):
    result = await extract_lab_results(file)

    if result["success"] and result["results"]:
        # Extract patient's name and surname from results (you need to know structure)
        patient_fullname = result["results"].get("patient_name", "")
        # Assuming patient name is two parts, you can split:
        name, surname = patient_fullname.split(" ", 1) if " " in patient_fullname else (patient_fullname, "")
        hashed_patient_id = generate_patient_id(name, surname)

        return templates.TemplateResponse("results.html", {
            "request": request,
            "results": result["results"],
            "hashed_patient_id": hashed_patient_id
        })
    else:
        # error handling
        return templates.TemplateResponse("results.html", {
            "request": request,
            "results": None,
            "hashed_patient_id": ""
        })
