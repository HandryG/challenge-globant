import os
from pydantic import BaseSettings
import pathlib

# Get the base directory
BASE_DIR = pathlib.Path(__file__).parent.parent

class Settings(BaseSettings):
    """Application settings."""
    DATABASE_URL: str 
    MAX_BATCH_SIZE: int 
    
    # Path to SQL files
    SQL_DIR: pathlib.Path = BASE_DIR / "sql"
    
    # Table definitions
    TABLES = {
        "departments": {
            "columns": ["id", "department"],
            "required": ["id", "department"],
            "id_field": "id"
        },
        "jobs": {
            "columns": ["id", "job"],
            "required": ["id", "job"],
            "id_field": "id"
        },
        "hired_employees": {
            "columns": ["id", "name", "datetime", "department_id", "job_id"],
            "required": ["id", "name", "datetime"],
            "id_field": "id"
        }
    }
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()