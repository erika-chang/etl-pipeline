import configparser
import logging
import os
from dotenv import load_dotenv

from pipeline.extract import extract_data
from pipeline.transform import transform_data
from pipeline.load import load_data

# --- Logging Configuration ---
# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/etl_pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """
    Main function to orchestrate the ETL pipeline.
    """
    logger.info("ETL pipeline started.")

    # --- Configuration Loading ---
    load_dotenv() # Load environment variables from .env file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get tables to process from config
    tables_to_process = config.get('etl_tables', 'tables').split(',')

    try:
        # --- EXTRACT ---
        logger.info("Starting Extract phase...")
        extracted_data = extract_data(config, tables_to_process)
        logger.info("Extract phase completed successfully.")

        # --- TRANSFORM ---
        logger.info("Starting Transform phase...")
        transformed_data = transform_data(extracted_data)
        logger.info("Transform phase completed successfully.")

        # --- LOAD ---
        # We load both the original staged data and the final transformed data
        logger.info("Starting Load phase for staging data...")
        load_data(extracted_data, config, schema='staging', if_exists='replace')
        logger.info("Staging data loaded successfully.")

        logger.info("Starting Load phase for analytics data...")
        load_data(transformed_data, config, schema='analytics', if_exists='replace')
        logger.info("Analytics data loaded successfully.")

        logger.info("ETL pipeline finished successfully.")

    except Exception as e:
        logger.error(f"An error occurred during the ETL process: {e}", exc_info=True)

if __name__ == "__main__":
    main()
