import psycopg2
from psycopg2.extras import DictCursor
from challenge-project.config import settings
import os

def get_connection():
    """Get PostgreSQL connection."""
    conn = psycopg2.connect(
        settings.DATABASE_URL,
        cursor_factory=DictCursor
    )
    return conn

def get_sql_file_content(filename):
    """Read SQL file content."""
    sql_path = os.path.join(settings.SQL_DIR, filename)
    with open(sql_path, 'r') as f:
        return f.read()

def execute_sql_file(conn, filename):
    """Execute SQL file on database connection."""
    cursor = conn.cursor()
    sql = get_sql_file_content(filename)
    cursor.execute(sql)
    conn.commit()
    cursor.close()