import fastavro
from ChallengeProject.config import settings
from ChallengeProject.database import get_connection
from ChallengeProject.api.data_processor import DataProcessor
import os

def backup_to_avro(table_name: str, file_path: str):
    """Backs up a PostgreSQL table into an Avro file using DataProcessor."""
    
    # Validate table name
    if table_name not in settings.TABLES:
        raise ValueError(f"Table '{table_name}' is not recognized in settings.TABLES")

    # Initialize DataProcessor for the given table
    processor = DataProcessor(table_name)
    columns = processor.columns  # Get column names
    column_types = settings.TABLES[table_name].get("types", {})  # Get column types

    # Define Avro schema dynamically
    avro_schema = {
        "type": "record",
        "name": f"{table_name}_record",
        "fields": [
            {"name": col, "type": ["null", column_types.get(col, "string")]}
            for col in columns
        ]
    }
    
    # Get database connection
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Fetch data from the table
        cursor.execute(f"SELECT {', '.join(columns)} FROM {table_name}")
        records = cursor.fetchall()

        # Convert data types to match Avro schema
        avro_records = []
        for row in records:
            record_dict = {}
            for i, col in enumerate(columns):
                value = row[i]
                expected_type = column_types.get(col, "string")

                # Convert values based on expected Avro type
                if expected_type == "int" and value is not None:
                    record_dict[col] = int(value)
                elif expected_type == "long" and value is not None:
                    record_dict[col] = int(value)
                elif expected_type == "boolean" and value is not None:
                    record_dict[col] = bool(value)
                elif expected_type == "string" and value is not None:
                    record_dict[col] = str(value)
                else:
                    record_dict[col] = None  # Maintain null values

            avro_records.append(record_dict)

        # Write records to Avro file using `fastavro`
        with open(file_path, "wb") as avro_file:
            fastavro.writer(avro_file, avro_schema, avro_records)

        print(f"Backup successful: {len(avro_records)} rows saved to {file_path}")

    except Exception as e:
        print(f"Error backing up table {table_name}: {e}")

    finally:
        cursor.close()
        conn.close()


def restore_from_avro(table_name: str, file_path: str):
    """Restores data from an Avro backup file into the specified PostgreSQL table."""
    
    # Validate table name
    if table_name not in settings.TABLES:
        raise ValueError(f"Table '{table_name}' is not recognized in settings.TABLES")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Backup file '{file_path}' not found")

    # Initialize DataProcessor
    processor = DataProcessor(table_name)
    
    # Open the Avro file and read records
    with open(file_path, "rb") as avro_file:
        reader = fastavro.reader(avro_file)
        records = [record for record in reader]

    if not records:
        print(f"No records found in {file_path}")
        return 0

    # Insert records into the database
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Prepare SQL statement dynamically
        sql, processed_records = processor.prepare_data_for_insert(records)
        cursor.executemany(sql, processed_records)
        conn.commit()

        print(f"Successfully restored {len(processed_records)} records to {table_name}")

    except Exception as e:
        conn.rollback()
        print(f"Error restoring data: {e}")
        raise

    finally:
        cursor.close()
        conn.close()

    return len(processed_records)
