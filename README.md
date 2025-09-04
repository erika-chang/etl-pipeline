# 🚀 Simple Sales Data ETL Pipeline

## 📖 Overview

This project is a simple ETL (Extract, Transform, Load) pipeline. It extracts sales and product data from a source SQL Server database, performs transformations to create an aggregated analytics table, and loads the result into a PostgreSQL database.

The goal is to demonstrate best practices in building a data pipeline, including a modular structure, logging, and clear documentation. The project is fully reproducible thanks to Docker for the PostgreSQL database and Python scripts for source data creation.

## ✨ Features

🐳 Containerized Destination: Easily run PostgreSQL with Docker and Docker Compose.

🔁 Fully Reproducible: Scripts create and populate the source database from scratch.

🛠 Modular Design: ETL is split into extract, transform, and load modules.

📊 Meaningful Transformation: Joins fact and dimension tables into a denormalized analytics table.

📜 Robust Logging: Tracks pipeline execution with Python's logging module.


## 📂 Project Structure
```bash
etl-pipeline/
├── README.md
├── database_setup
│   ├── data_gen.py
│   └── models.py
├── docker-compose.yml
├── logs
├── main.py
├── pipeline
│   ├── __init__.py
│   ├── extract.py
│   ├── load.py
│   └── transform.py
├── requirements.txt
└── sql
    └── create_schema.sql
```

## 🛠 Prerequisites

- Python 3.8+

- Docker & Docker Compose


## ⚡ How to Run

The pipeline has three main stages: Configuration → Database Setup → Run ETL.

### 1️⃣ Initial Configuration

Clone the repository:

```bash
git clone <your-repo-url>
cd etl-pipeline
```

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```


### 2️⃣ Setting Up Databases

Start PostgreSQL container:

```bash
docker-compose up -d
```

Check if it’s running:

```bash
docker ps
```

Populate source SQL Server database:

```bash
cd database_setup
python populate_database.py
cd ..
```

### 3️⃣ Run the ETL Pipeline

```bash
python main.py
```

Logs appear in the console and in logs/etl_pipeline.log.

Final analytics data is stored in the PostgreSQL analytics schema.

### 🛑 Stopping the Environment

```bash
docker-compose down
```

Stops the container.

Data is preserved in the postgres_data volume.

## 📈 Key Outcome

✅ Cleaned and transformed sales data in PostgreSQL.

✅ Modular ETL code, easy to extend.

✅ Fully reproducible setup using Docker.
