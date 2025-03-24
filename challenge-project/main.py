from fastapi import FastAPI
from challenge-project.api.routes import router

challenge_project = FastAPI(
    title="Employee Data API",
    description="API for managing employee data from CSV files",
    version="1.0.0"
)

challenge_project.include_router(router, prefix="/api", tags=["data-upload"])

@challenge_project.get("/")
async def root():
    return {
        "message": "Employee Data API is running", 
        "documentation": "/docs",
        "health": "OK"
    }

@challenge_project.get("/health")
async def health():
    return {"status": "healthy"}