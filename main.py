# main.py
import logging
import os

from pipeline.extract import extract_data
from pipeline.transform import transform_data
from pipeline.load import load_data

# --- Logging Configuration ---
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
    db_url = 'postgresql://etl_user:etl_paswd@localhost:5432/etl_db'
    try:
        # --- EXTRACT ---
        logger.info("Starting Extract phase...")
        tables_to_extract = ['salesterritory', 'productcategory', 'productsubcategory', 'product', 'factinternetsales']
        extracted_data = extract_data(tables_to_extract, db_url)
        logger.info("Extract phase completed successfully.")

        # --- TRANSFORM ---
        logger.info("Starting Transform phase...")
        transformed_data = transform_data(extracted_data)
        logger.info("Transform phase completed successfully.")

        # --- LOAD ---
        logger.info("Starting Load phase ...")
        load_data(extracted_data, db_url, schema='staging', if_exists='replace')
        logger.info("Data loaded successfully.")
        load_data(transformed_data, db_url, schema='analytics', if_exists='replace')
        logger.info("Transformed data loaded successfully.")

        logger.info("ETL pipeline finished successfully.")

    except Exception as e:
        logger.error(f"An error occurred during the ETL process: {e}", exc_info=True)

if __name__ == "__main__":
    main()
