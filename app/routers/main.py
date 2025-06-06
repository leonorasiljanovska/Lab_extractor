# from fastapi import APIRouter, UploadFile, File, HTTPException
# from ..models import ExtractResponse
# from ..utils import extract_lab_results
#
# router = APIRouter()
#
#
# @router.post("/extract-lab-results", response_model=ExtractResponse)
# async def extract_laboratory_results(file: UploadFile = File(...)):
#     """
#     Extract laboratory results from an uploaded image file
#     """
#     # Validate file type
#     if not file.content_type.startswith('image/'):
#         raise HTTPException(status_code=400, detail="File must be an image")
#
#     # Extract results
#     result = await extract_lab_results(file)
#
#     return ExtractResponse(**result)
#
#
# @router.get("/health")
# async def health_check():
#     """
#     Health check endpoint
#     """
#     return {"status": "healthy", "message": "Lab Report Extractor API is running"}

from fastapi import APIRouter, UploadFile, File, HTTPException
from ..models import ExtractResponse, LaboratoryResults
from ..utils import extract_lab_results

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