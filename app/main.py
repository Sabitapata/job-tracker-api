from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routers.applications import router as applications_router
from app.routers.users import router as users_router

from app.models import JobApplication, User


app = FastAPI(
    title="Job Tracker API",
    description="Track job applications with a Python API and SQLite database",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def home():
    return {
        "message": "Welcome to my Job Tracker API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


app.include_router(applications_router)
app.include_router(users_router)