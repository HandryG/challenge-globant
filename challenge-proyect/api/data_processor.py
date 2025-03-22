import csv
import io
from typing import List, Dict, Any, Iterator, Tuple
from challenge-proyect.config import settings
import psycopg2
from challenge-proyect.database import get_connection

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
        """
        Process a CSV content in batches.
        
        Args:
            csv_content: The CSV content as a string
            batch_size: Maximum number of rows per batch
            
        Yields:
            Batches of CSV rows as dictionaries
        """
        reader = csv.reader(io.StringIO(csv_content))
        batch = []
        
        for row in reader:
            # Skip rows that don't have the minimum required fields
            if len(row) < len(self.required):
                continue
                
            # Convert row to dictionary with dynamic column mapping
            record = {}
            for i, col in enumerate(self.columns):
                if i < len(row):
                    record[col] = row[i]
            
            # Validate required fields
            if all(record.get(field) for field in self.required):
                batch.append(record)
            
            if len(batch) >= batch_size:
                yield batch
                batch = []
        
        if batch:  # Don't forget the last batch if it's not empty
            yield batch
    
    def prepare_data_for_insert(self, records: List[Dict]) -> Tuple[str, List[tuple]]:
        """
        Prepare data for database insertion with dynamic schema support.
        
        Args:
            records: List of record dictionaries
            
        Returns:
            A tuple containing (sql_statement, parameter_tuples)
        """
        # Build columns and placeholders dynamically
        columns = []
        placeholders = []
        update_clauses = []
        
        for col in self.columns:
            if col in records[0]:
                columns.append(col)
                placeholders.append(f"%({col})s")
                if col != self.id_field:  # Don't update primary key
                    update_clauses.append(f"{col} = EXCLUDED.{col}")
        
        # Build the SQL statement
        sql = f"""
            INSERT INTO {self.table_name} ({', '.join(columns)})
            VALUES ({', '.join(placeholders)})
            ON CONFLICT ({self.id_field}) DO UPDATE SET {', '.join(update_clauses)}
        """
        
        # Process the records to handle data types properly
        processed_records = []
        for record in records:
            processed = {}
            for col in columns:
                val = record.get(col, None)
                
                # Handle data type conversions as needed
                if col == self.id_field and val is not None:
                    processed[col] = int(val)
                elif col in ['department_id', 'job_id'] and val:
                    processed[col] = int(val)
                else:
                    processed[col] = val
                    
            processed_records.append(processed)
        
        return sql, processed_records
    
    async def process_csv_file(self, file_content):
        """
        Process a CSV file and insert data into the database.
        
        Args:
            file_content: CSV file content
            
        Returns:
            Number of rows processed
        """
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
                
                # Execute batch insert using executemany
                cursor.executemany(sql, records)
                total_rows += len(records)
            
            conn.commit()
            return total_rows
        
        except Exception as e:
            conn.rollback()
            raise e
            
        finally:
            conn.close()