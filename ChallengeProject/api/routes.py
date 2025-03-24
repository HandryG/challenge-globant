from fastapi import APIRouter, UploadFile, File, HTTPException
from ChallengeProject.api.data_processor import DataProcessor
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
        # Initialize the data processor for the specified table
        processor = DataProcessor(table_name)
        
        # Read the file content
        content = await file.read()
        
        # Process the CSV file
        total_rows = await processor.process_csv_file(content)
        
        return {"message": f"Successfully uploaded {total_rows} rows to {table_name}"}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        error_detail = str(e) + "\n" + traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Error uploading data: {error_detail}")