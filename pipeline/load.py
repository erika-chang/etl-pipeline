import logging
import os
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

def load_data(data_to_load, config, schema, if_exists='replace'):
    """
    Loads data into the destination PostgreSQL database.

    Args:
        data_to_load (dict): Dictionary of DataFrames to load.
        config (ConfigParser): Configuration object with database details.
        schema (str): The target schema in the database (e.g., 'staging', 'analytics').
        if_exists (str): How to behave if the table already exists.
                         Options: 'fail', 'replace', 'append'.
    """
    try:
        # Get credentials from environment variables
        uid = os.environ.get('DB_USER')
        pwd = os.environ.get('DB_PASSWORD')

        # Get DB details from config
        server = config.get('postgresql', 'server')
        port = config.get('postgresql', 'port')
        database = config.get('postgresql', 'database')

        logger.info(f"Connecting to destination database: {server}/{database}")

        engine = create_engine(f'postgresql://{uid}:{pwd}@{server}:{port}/{database}')

        with engine.connect() as conn:
            # Ensure the target schema exists
            conn.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")
            conn.commit()
            logger.info(f"Schema '{schema}' ensured to exist.")

            for table_name, df in data_to_load.items():
                logger.info(f"Loading data into table: {schema}.{table_name}")

                df.to_sql(
                    name=table_name,
                    con=engine,
                    schema=schema,
                    if_exists=if_exists,
                    index=False,
                    chunksize=10000  # Load data in chunks for better memory management
                )

                logger.info(f"Successfully loaded {len(df)} rows into {schema}.{table_name}.")

    except Exception as e:
        logger.error(f"Error during data loading: {e}")
