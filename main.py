# from fastapi import FastAPI
#
# app = FastAPI()
#
#
# @app.get("/")
# async def root():
#     return {"message": "Hello from minimal FastAPI app"}
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import main as api_router
from app.routers import views as html_router

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Lab Report Extractor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router.router, prefix="/api/v1", tags=["lab-extraction"])
app.include_router(html_router.router)  # no prefix

@app.get("/")
async def root():
    return {"message": "Hello from minimal FastAPI app"}

@app.get("/test-env")
async def test_env():
    return {"GROQ_API_KEY": os.getenv("GROQ_API_KEY")}