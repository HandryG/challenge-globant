# challenge-globant

## Overview
This project provides a FastAPI-based REST API for managing employee data, including job roles, departments, and hiring records. The API is containerized using Docker and interacts with a PostgreSQL database.

## Features
- **CRUD Operations** for employees, jobs, and departments.
- **Backup & Restore**: Save and restore table data using Avro files.
- **Quarterly Hiring Report**: Retrieve employee hiring statistics per quarter.
- **Dockerized Deployment** for easy setup and scaling.

## Technologies Used
- FastAPI
- PostgreSQL
- Docker & Docker Compose
- Avro (for backups)
- Psycopg2 (PostgreSQL connector)

## Setup Instructions

### Prerequisites
- Docker & Docker Compose installed
- `.env` file configured with necessary environment variables

### Installation & Running
1. Clone the repository:
   ```sh
   git clone https://github.com/HandryG/challenge-globant.git
   cd challenge-globant
   ```

2. Start the services using Docker Compose:
   ```sh
   docker-compose up -d --build
   ```

3. Check if the API is running:
   ```sh
   curl http://localhost:8000/api
   ```

## API Endpoints

### Employee Operations

- `POST api/upload/{table_name}` - Add a new row for any table

### Backup & Restore
- `GET api/backup/{table_name}` - Backup a table as an Avro file
- `POST api/restore/{table_name}` - Restore a table from an Avro file

### Reports
- `GET api/hired-employees-per-quarter` 
- `GET api/departments-above-mean-hires` 
  
## Checking Backup Files
To verify that a backup was saved in the Docker volume:
```sh
docker volume inspect challenge-globant_backup_volume
```
To list files inside the volume:
```sh
docker run --rm -v challenge-globant_backup_volume:/data busybox ls /data
```

## Running Queries

```sh
psql -h localhost -p 5432 -U postgres -d employee_db
```

## Stopping & Cleaning Up
To stop and remove all containers:
```sh
docker-compose down
```
To remove volumes (including backups and database data):
```sh
docker-compose down -v
```

