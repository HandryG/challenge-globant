from fastapi import FastAPI
from challenge-proyect.api.routes import router

challenge_proyect = FastAPI(
    title="Employee Data API",
    description="API for managing employee data from CSV files",
    version="1.0.0"
)

challenge_proyect.include_router(router, prefix="/api", tags=["data-upload"])

@challenge_proyect.get("/")
async def root():
    return {
        "message": "Employee Data API is running", 
        "documentation": "/docs",
        "health": "OK"
    }

@challenge_proyect.get("/health")
async def health():
    return {"status": "healthy"}