from fastapi import APIRouter, UploadFile, File, HTTPException
from ChallengeProject.api.data_processor import DataProcessor
from ChallengeProject.api.backup_service import backup_to_avro, restore_from_avro
from ChallengeProject.config import settings
from ChallengeProject.database import get_hired_employees_per_quarter, get_departments_above_mean_hires
import os
import traceback

router = APIRouter()

@router.post("/upload/{table_name}")
async def upload_csv(table_name: str, file: UploadFile = File(...)):
    """
    Generic endpoint for uploading CSV data to any table.
    
    Args:
        table_name: Name of the table to upload data to
        file: CSV file
        
    Returns:
        Success message with the number of rows processed
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    try:
        
        processor = DataProcessor(table_name)
        
        
        content = await file.read()
        
        
        total_rows = await processor.process_csv_file(content)
        
        return {"message": f"Successfully uploaded {total_rows} rows to {table_name}"}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        error_detail = str(e) + "\n" + traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Error uploading data: {error_detail}")

@router.get("/backup/{table_name}")
async def backup_table(table_name: str):
    """
    Endpoint to backup table data to an Avro file.
    
    Args:
        table_name: Name of the table to back up.

    Returns:
        Message with backup file path.
    """
    backup_dir = settings.BACKUP_DIR
    os.makedirs(backup_dir, exist_ok=True)

    file_path = backup_dir / f"{table_name}_backup.avro"

    try:
        backup_to_avro(table_name, file_path)  
        return {"message": f"Backup saved at {file_path}"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        error_detail = str(e) + "\n" + traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Error in backup: {error_detail}")


@router.post("/restore/{table_name}")
async def restore_table(table_name: str):
    """
    Endpoint to restore table data from an Avro file.
    
    Args:
        table_name: Name of the table to restore.

    Returns:
        Message with the number of rows restored.
    """
    backup_dir = settings.BACKUP_DIR
    os.makedirs(backup_dir, exist_ok=True)

    file_path = backup_dir / f"{table_name}_backup.avro"

    try:
        restored_rows = restore_from_avro(table_name, file_path)
        return {"message": f"Restored {restored_rows} rows to {table_name}"}

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        error_detail = str(e) + "\n" + traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Error restoring data: {error_detail}")



@router.get("/hired-employees-per-quarter")
async def hired_employees_per_quarter():
    """
    API Endpoint to get the number of employees hired per job and department in 2021, by quarter.
    """
    try:
        data = get_hired_employees_per_quarter()
        return {"data": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/departments-above-mean-hires")
async def departments_above_mean_hires():
    """
    API Endpoint to get departments that hired more employees than the mean in 2021.
    """
    try:
        data = get_departments_above_mean_hires()
        return {"data": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))