
CREATE TABLE IF NOT EXISTS departments (
    department_key SERIAL PRIMARY KEY,
    id INTEGER ,
    department VARCHAR(100) NOT NULL
);


CREATE TABLE IF NOT EXISTS jobs (
    job_key SERIAL PRIMARY KEY,
    id INTEGER ,
    job VARCHAR(100) NOT NULL
);


CREATE TABLE IF NOT EXISTS hired_employees (
    hire_key SERIAL PRIMARY KEY,
    id INTEGER ,
    name VARCHAR(100) NOT NULL,
    datetime TIMESTAMP NOT NULL,
    department_id INTEGER,
    job_id INTEGER
);

