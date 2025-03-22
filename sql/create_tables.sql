
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY,
    department VARCHAR(100) NOT NULL
);


CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY,
    job VARCHAR(100) NOT NULL
);


CREATE TABLE IF NOT EXISTS hired_employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    datetime VARCHAR(50) NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    job_id INTEGER REFERENCES jobs(id)
);


-- To run this script from PostgreSQL console:
-- psql -U postgres -d employee_db -f /sql/create_tables.sql