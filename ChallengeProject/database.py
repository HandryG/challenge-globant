import psycopg2
from psycopg2.extras import DictCursor
from ChallengeProject.config import settings

def get_connection():
    """Get PostgreSQL connection."""
    conn = psycopg2.connect(
        settings.DATABASE_URL,
        cursor_factory=DictCursor
    )
    return conn

def get_hired_employees_per_quarter():
   
    query = """
        SELECT 
            d.department,
            j.job,
            COALESCE(SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 1 THEN 1 ELSE 0 END), 0) AS Q1,
            COALESCE(SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 2 THEN 1 ELSE 0 END), 0) AS Q2,
            COALESCE(SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 3 THEN 1 ELSE 0 END), 0) AS Q3,
            COALESCE(SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 4 THEN 1 ELSE 0 END), 0) AS Q4
        FROM hired_employees he
        JOIN departments d ON he.department_id = d.id
        JOIN jobs j ON he.job_id = j.id
        WHERE EXTRACT(YEAR FROM he.datetime) = 2021
        GROUP BY d.department, j.job
        ORDER BY d.department, j.job;
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        results = cursor.fetchall()

        data = [
            {"department": row[0], "job": row[1], "Q1": row[2], "Q2": row[3], "Q3": row[4], "Q4": row[5]}
            for row in results
        ]

        return data

    except Exception as e:
        print(f"Database query error: {e}")
        return []

    finally:
        cursor.close()
        conn.close()

def get_departments_above_mean_hires():
   
    query = """
        WITH department_hires AS (
            SELECT 
                he.department_id,
                d.department AS name,
                COUNT(*) AS total_hired
            FROM hired_employees he
            JOIN departments d ON he.department_id = d.id
            WHERE EXTRACT(YEAR FROM he.datetime) = 2021
            GROUP BY he.department_id, d.department
        ),
        mean_hires AS (
            SELECT AVG(total_hired) AS avg_hires FROM department_hires
        )
        SELECT 
            dh.department_id AS id,
            dh.name,
            dh.total_hired
        FROM department_hires dh
        JOIN mean_hires mh ON dh.total_hired > mh.avg_hires
        ORDER BY dh.total_hired DESC;
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        results = cursor.fetchall()

        data = [
            {"id": row[0], "name": row[1], "total_hired": row[2]}
            for row in results
        ]

        return data

    except Exception as e:
        print(f"Database query error: {e}")
        return []

    finally:
        cursor.close()
        conn.close()
