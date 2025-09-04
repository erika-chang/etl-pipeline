import logging
import pandas as pd
from sqlalchemy import create_engine, text

# Configuração básica do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_data(tables_to_extract, db_url):
    """
    Connects to the PostgreSQL database and extracts data from specified tables.

    Args:
        tables_to_extract (list): A list of table names to extract.

    Returns:
        dict: A dictionary of pandas DataFrames, where keys are table names.
    """
    dataframes = {}
    try:
        engine = create_engine(db_url, echo=False)

        with engine.connect() as conn:
            for table_name in tables_to_extract:
                logger.info(f"Extracting data from table: {table_name}")
                # Garantir que o nome da tabela seja tratado como string
                query = text(f'SELECT * FROM "{table_name}"')
                df = pd.read_sql_query(query, conn)
                dataframes[table_name] = df
                logger.info(f"Successfully extracted {len(df)} rows from {table_name}.")

        return dataframes

    except Exception as e:
        logger.error(f"Error during data extraction: {e}")
        raise
