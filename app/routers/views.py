from fastapi import APIRouter, Request, UploadFile, Form
from fastapi.responses import HTMLResponse
from app.core.templates import templates
from app.utils import extract_lab_results
import os

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@router.post("/view-results", response_class=HTMLResponse)
async def show_results(request: Request, file: UploadFile = Form(...)):
    result = await extract_lab_results(file)
    return templates.TemplateResponse("results.html", {
        "request": request,
        "results": result["results"]
    })
