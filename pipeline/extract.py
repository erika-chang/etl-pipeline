import logging
import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

logger = logging.getLogger(__name__)

def extract_data(config, tables_to_extract):
    """
    Connects to the source SQL Server and extracts data from specified tables.

    Args:
        config (ConfigParser): Configuration object with database details.
        tables_to_extract (list): A list of table names to extract.

    Returns:
        dict: A dictionary of pandas DataFrames, where keys are table names.
    """
    dataframes = {}
    try:
        # Get credentials from environment variables
        uid = os.environ.get('DB_USER')
        pwd = os.environ.get('DB_PASSWORD')

        # Get DB details from config
        driver = config.get('sql_server', 'driver')
        server = config.get('sql_server', 'server')
        database = config.get('sql_server', 'database')

        logger.info(f"Connecting to source database: {server}/{database}")

        connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={uid};PWD={pwd}'
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

        engine = create_engine(connection_url)

        with engine.connect() as conn:
            for table_name in tables_to_extract:
                logger.info(f"Extracting data from table: {table_name}")
                query = f"SELECT * FROM {table_name}"
                df = pd.read_sql_query(text(query), conn)
                dataframes[table_name] = df
                logger.info(f"Successfully extracted {len(df)} rows from {table_name}.")

        return dataframes

    except Exception as e:
        logger.error(f"Error during data extraction: {e}")
