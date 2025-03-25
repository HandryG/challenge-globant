import csv
import io
from typing import List, Dict, Any, Iterator, Tuple
import logging
from ChallengeProject.config import settings
import psycopg2
from ChallengeProject.database import get_connection

class DataProcessor:
    """Flexible data processor for CSV import with dynamic schema support."""
    
    def __init__(self, table_name):
        """Initialize processor for a specific table."""
        if table_name not in settings.TABLES:
            raise ValueError(f"Unknown table: {table_name}")
        
        self.table_name = table_name
        self.table_config = settings.TABLES[table_name]
        self.columns = self.table_config["columns"]
        self.required = self.table_config["required"]
        self.id_field = self.table_config["id_field"]
    
    def process_csv_in_batches(self, csv_content: str, batch_size: int = settings.MAX_BATCH_SIZE) -> Iterator[List[Dict]]:
        
        reader = csv.reader(io.StringIO(csv_content))
        batch = []
        skipped_rows = [] 
        
        for row in reader:
            if len(row) < len(self.required):
                skipped_rows.append(row)
                continue
                            
            record = {}
            for i, col in enumerate(self.columns):
                if i < len(row):
                    record[col] = row[i]
                        
            if all(record.get(field) for field in self.required):
                batch.append(record)
            
            if len(batch) >= batch_size:
                yield batch
                batch = []
        
        if batch:  
            yield batch
        
        # Log skipped rows
        if skipped_rows:
            logging.warning(f"Skipped {len(skipped_rows)} rows due to missing required fields.")
            for row in skipped_rows:
                logging.warning(f"Skipped row: {row}")
    
    def prepare_data_for_insert(self, records: List[Dict]) -> Tuple[str, List[tuple]]:
       
        columns = []
        placeholders = []
        update_clauses = []
        
        for col in self.columns:
            if col in records[0]:
                columns.append(col)
                placeholders.append(f"%({col})s")
                if col != self.id_field:  
                    update_clauses.append(f"{col} = EXCLUDED.{col}")
        
        
        sql = f"""
            INSERT INTO {self.table_name} ({', '.join(columns)})
            VALUES ({', '.join(placeholders)})
            ON CONFLICT ({self.id_field}) DO UPDATE SET {', '.join(update_clauses)}
        """
        
        
        processed_records = []
        for record in records:
            processed = {}
            for col in columns:
                val = record.get(col, None)
                
                if col == self.id_field and val is not None:
                    processed[col] = int(val)
                elif col in ['department_id', 'job_id'] and val:
                    processed[col] = int(val)
                else:
                    processed[col] = val
                    
            processed_records.append(processed)
        
        return sql, processed_records
    
    async def process_csv_file(self, file_content):
        
        total_rows = 0
        conn = get_connection()
        
        try:
            cursor = conn.cursor()
            
            # Process the CSV in batches
            for batch in self.process_csv_in_batches(file_content.decode('utf-8')):
                if not batch:
                    continue
                
                # Prepare data for insertion
                sql, records = self.prepare_data_for_insert(batch)
                
                cursor.executemany(sql, records)
                total_rows += len(records)
            
            conn.commit()
            return total_rows
        
        except Exception as e:
            conn.rollback()
            raise e
            
        finally:
            conn.close()