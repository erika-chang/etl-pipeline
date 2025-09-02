# Simple Sales Data ETL Pipeline

## Overview
This project is a simple, portfolio-ready ETL (Extract, Transform, Load) pipeline. It extracts sales and product data from a source SQL Server database (using the AdventureWorks sample dataset), performs transformations to create an aggregated analytics table, and loads the final result into a destination PostgreSQL database.

The primary goal of this project is to demonstrate best practices in building a data pipeline, including a modular structure, configuration management, logging, and clear documentation.

## Features
Modular Design: The ETL process is broken down into separate, reusable modules for extraction, transformation, and loading.

Configuration Driven: Database connections and table lists are managed in an external config.ini file, not hardcoded.

Credential Management: Sensitive credentials (username, password) are handled securely using a .env file and environment variables.

Meaningful Transformation: The pipeline joins fact and dimension tables to create a denormalized table ready for analytics.

Robust Logging: Implements the standard Python logging module to track the pipeline's execution and handle errors.

## Project Structure
```bash
etl-pipeline/
├── pipeline/
│   ├── __init__.py
│   ├── extract.py      # Handles data extraction from source
│   ├── transform.py    # Performs all data transformations
│   └── load.py         # Loads transformed data to destination
├── logs/
│   └── etl_pipeline.log # Log file will be generated here
├── .env.example        # Example environment file for credentials
├── config.ini          # Configuration for databases and tables
├── main.py             # Main script to run the ETL pipeline
└── requirements.txt    # Python dependencies
```

## Prerequisites
Python 3.8+

Access to a SQL Server instance with the AdventureWorksDW2019 sample database.

Access to a PostgreSQL instance.

[Optional but Recommended] Docker to easily spin up database instances.

## Setup Instructions
1. Clone the Repository:

```bash
git clone <your-repo-url>
cd simple-etl-portfolio
```

2. Create a Virtual Environment:
It's highly recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install Dependencies:

```bash
pip install -r requirements.txt
```

4. Configure Credentials:
Create a .env file in the project root by copying the example file.

```bash
cp .env.example .env
```

5. Now, edit the .env file and add your database credentials:

```bash
DB_USER=your_database_username
DB_PASSWORD=your_database_password
```

6. Update Configuration:
Open config.ini and update the [sql_server] and [postgresql] sections with your specific server details (e.g., hostname, database names) if they are not running on localhost.

7. Running the Pipeline
To execute the full ETL process, simply run the main.py script from the project root directory:

```bash
python main.py
```

The script will log its progress to both the console and the logs/etl_pipeline.log file.

## ETL Logic Explained
1. Extract
The extract.py module connects to the source SQL Server database specified in config.ini. It reads each of the tables listed under [etl_tables] and loads them into a dictionary of Pandas DataFrames.

2. Transform
The transform.py module takes the raw DataFrames from the extract step. Its main function is to:

Join FactInternetSales with dimension tables (DimProduct, DimProductSubcategory, DimProductCategory, DimSalesTerritory).

Select a subset of relevant columns for analysis.

Create a new calculated column, for example, TotalRevenue.

This process denormalizes the data into a single, wide table (analytics_sales) that is optimized for reporting and analysis.

3. Load
The load.py module takes the transformed DataFrames. It connects to the destination PostgreSQL database and performs the following:

Loads the raw, extracted tables into a staging schema. This is useful for data validation and debugging.

Loads the final, transformed analytics_sales table into an analytics schema. This table is the final product, ready for use by BI tools or data analysts.
