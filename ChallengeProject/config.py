import os
from pydantic_settings import BaseSettings
from typing import ClassVar, Dict
import pathlib

# Get the base directory
BASE_DIR = pathlib.Path(__file__).parent.parent  

class Settings(BaseSettings):
    DATABASE_URL: str 
    MAX_BATCH_SIZE: int 
    BACKUP_DIR: pathlib.Path = pathlib.Path(os.getenv("BACKUP_DIR", BASE_DIR / "backups"))

    
    SQL_DIR: pathlib.Path = BASE_DIR / "sql"
    
    
    TABLES: ClassVar[Dict] = {
        "departments": {
            "columns": ["id", "department"],
            "required": ["id", "department"],
            "id_field": "id",
            "types": { 
                "id": "int",
                "department": "string"
            }
        },
        "jobs": {
            "columns": ["id", "job"],
            "required": ["id", "job"],
            "id_field": "id",
            "types": {
                "id": "int",
                "job": "string"
            }
        },
        "hired_employees": {
            "columns": ["id", "name", "datetime", "department_id", "job_id"],
            "required": ["id", "name", "datetime"],
            "id_field": "id",
            "types": {
                "id": "int",
                "name": "string",
                "datetime": "string",
                "department_id": "int",
                "job_id": "int"
            }
        }
    }
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Ensure the backup directory exists
settings.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
