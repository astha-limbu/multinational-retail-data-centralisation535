# Multinational Retail Data Centralisation

# Table of Contents
1. [Introduction](#introduction)
    - [About the project](#About-the-project)
    - [Motivation for project](#Motivation-for-project)
    - [Topics covered](#Topics-covered)
2. [Features](#features)
    - [User Interaction](#User-Interaction)
    - [Feedback Managment](#Feedback-Managment)
    - [Game ending](#Game-ending)
3. [Installation instructions](#Installation-instructions)
4. [Usage instructions](#Usage-instructions)
5. [File structure](#File-structure)
6. [License information](#License-information)

## Introduction

### About the project
This project focuses on developing a centralised database system to store and manage the company's global sales data. This project  integrates the company's sales data that is spread across various sources from multiple sources into one cohesive and easily accessible platform.

The initial phase of the project focuses on building the database to store current sales data, ensuring data integrity and accessibility. In the subsequent phase, the project involves querying the database to generate real-time business metrics, enabling the organization to monitor performance, identify trends, and make informed decisions based on accurate and comprehensive sales data. 

### Motivation for project
The motivation behind this project stems from the need to streamline access to sales data, which is currently scattered across multiple platforms. By bringing all data into a unified database, the project aims to simplify the process of retrieving, cleaning, and analysing data

This project was created to apply the skills acquired during the AiCore bootcamp.

### Topics covered 
- Data Extraction: Retrieving data from various sources, including AWS RDS, PDFs, APIs, and S3 buckets, using Python scripts.
- Data Cleaning: Methods for processing and cleaning raw data using pandas to remove inconsistencies, handle missing values, and standardise formats.
- Database Management: Setting up, managing, and interacting with a centralised database using Python and PostgreSQL.
- Creating database Schema: Developing star-based schema of the database on PostgreSQL, ensuring columns are correct data types.
- SQL Queries: Running queries on PostgreSQL to extract meaningful insights from the centralised data.

## Features 

### Requirements.txt file 
- used to list third-party packages that need to be installed

### ETL Process Implementation:
- Extract: Retrieving data from multiple disparate sources including RDS databases, S3 buckets, CSV files, APIs, and PDFs.
- Transform: Cleaning, normalising, and transforming raw data into a consistent format using custom functions.
- Load: Uploading the cleaned data into a local PostgreSQL database.   

### Automated Data Pipeline:
- A system that automatically extracts, cleans, and uploads data to a database, reducing manual intervention and errors.

### API Integration
- Implementing interaction with external APIs to fetch real-time data

### Data Type Conversion and Standardization
- Handling non-standard and inconsistent data formats, such as converting weights to a standard unit (e.g. kg), and correcting non-standard dates.

### Error Handling and Logging
- Implementing error handling mechanisms to capture and log errors during data extraction, transformation, and loading processes for better debugging and reliability.

## Installation instructions
1. Clone the Repository: `git clone URL`
2. Install Required Packages:
    - Ensure you have Python 3.x installed.
    - Install the required Python packages: `pip install -r requirements.txt`
3. Install PostgreSQL
4. Install pgAdmin4, an administration and development platform for PostgreSQL, if needed
5. Set Up the Database:
    - Ensure your PostgreSQL server is running.
    - Create a local PostgreSQL database
6. Configure Database Credentials:
    - Ensure you have these files to connect to the databases:
        1. `db_creds.yaml` file with necessary credentials to connect to AWS RDS 
        2. `local_db_creds.yaml` file with necessary credentials to connect to the local PostgreSQL database

## Necessary Credentials

### AWS RDS Credentials 
Make sure your `db_creds.yaml` file includes the following information:
- **Username**: Your AWS RDS username
- **Password**: Your AWS RDS password
- **Host**: The hostname or endpoint of your AWS RDS instance
- **Port**: The port number for the AWS RDS instance 
- **Database Name**: The name of the database you want to connect to

### Local PostgreSQL Credentials 
Make sure your local_db_creds.yaml file includes the following information:
- **Username**: Your local PostgreSQL username
- **Password**: Your local PostgreSQL password
- **Host**: The hostname for your local PostgreSQL server 
- **Port**: The port number for your local PostgreSQL server
- **Database Name**: The name of the local PostgreSQL database you want to connect to

## Usage instructions
1. Run the Main Script: 
    - Navigate to the directory containing the main.py file.
    - Run the script to start the data extraction, cleaning, and upload processes: `python main.py`
2. Execute SQL queries to set up your local database schema:
Ensure PostgreSQL is installed and running on your system.
    - Locate the Query File.
    - Execute the SQL Query: 
        - ••Using pgAdmin4••: connect to your PostgreSQL server and Load the query.sql file by clicking on the "Open File" icon.
        - ••Using the psql Command-Line Tool••: Replace [your_database] with the name of your local database and run the following command: `psql -U [your_username] -d [your_database] -f `


## File structure
├── main.py                   # Main script to run the entire data pipeline
├── database_utils.py         # DatabaseConnector class for interacting with the database
├── data_extraction.py        # DataExtractor class for extracting data from various sources
├── data_cleaning.py          # DataCleaning class for cleaning and processing the data
├── requirements.txt          # List of required Python packages
├── README.md                 # Project documentation

## License information
Distributed under the MIT License. See LICENSE for more information.

