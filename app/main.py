from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.templates import templates

from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env
groq_api_key = os.getenv("GROQ_API_KEY")


app = FastAPI(
    title="Lab Report Extractor API",
    description="API for extracting laboratory results from document images",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# import your routers here *after* templates is set up
from app.routers import views as html_router
from app.routers import main as api_router

# Include routers
app.include_router(api_router.router, prefix="/api/v1", tags=["lab-extraction"])
app.include_router(html_router.router)  # for HTML form + result rendering

# Optional: static file mounting
# app.mount("/static", StaticFiles(directory="static"), name="static")
