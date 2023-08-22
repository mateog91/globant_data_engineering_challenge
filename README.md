
# Globan Data Engineer Challenge

Simulate a Data Engineer migration of historical data and ingestion of new data for a School having three tables: Jobs, Departments and Hired Employees.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Description

The Employee Management System is a web application built using FastAPI and SQLAlchemy, allowing users to manage and track various aspects of employee information. It provides functionalities to add and retrieve data related to departments, jobs, and hired employees.

## Features

- Add and manage departments with their respective details.
- Define different job roles and responsibilities.
- Track hired employees, including their names, departments, and job roles.
- Efficiently import and export data using CSV files.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mateog91/globant_data_engineering_challenge.git
   ```
   
2. Navigate to directory:
    ```bash
    cd globant_data_engineering_challenge
    ```
3. Run docker compose
    ```bash
    docker-compose up --build
    ```
    This will start FastAPI and the Postgres Containers

## Usage
1. Access the API documentation at http://localhost:8000/docs to interact with the endpoints using the Swagger UI.

2. The database will initiate empty, so the first step is to do the migration using the migration/upolaodfile/
Select the Filetype (Job, Department, Hired Employee) table you want to migrate.

Restrictions: Works only for one file per filetype, if you re upolaod a file for the same filetype it will be overwritten. 

3. Use the endpoints: "create_jobs", "create_departments" or "create_hired_employees" to add new rows to each table.

Note: for Hired Employees, the job and department must be created first


