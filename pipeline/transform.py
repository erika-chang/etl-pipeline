import logging
import pandas as pd

logger = logging.getLogger(__name__)

def transform_data(extracted_data):
    """
    Performs transformations on the extracted data.

    Args:
        extracted_data (dict): A dictionary of pandas DataFrames from the extract step.

    Returns:
        dict: A dictionary containing the transformed DataFrame(s).
    """
    transformed_data = {}

    try:
        logger.info("Starting data transformation.")

        # --- Rename extracted tables according to actual Postgres names ---
        sales_df = extracted_data['factinternetsales']
        product_df = extracted_data['product']
        prod_sub_df = extracted_data['productsubcategory']
        prod_cat_df = extracted_data['productcategory']
        territory_df = extracted_data['salesterritory']

        # Join FactInternetSales with Product
        analytics_df = pd.merge(sales_df, product_df, on='productkey', how='left')

        # Join with ProductSubcategory
        analytics_df = pd.merge(analytics_df, prod_sub_df, on='productsubcategorykey', how='left')

        # Join with ProductCategory
        analytics_df = pd.merge(analytics_df, prod_cat_df, on='productcategorykey', how='left')

        # Join with SalesTerritory
        analytics_df = pd.merge(analytics_df, territory_df, on='salesterritorykey', how='left')

        logger.info("Dataframes merged successfully.")

        # --- Column Selection and Renaming ---
        analytics_df = analytics_df[[
            'orderdate', 'salesordernumber', 'orderquantity', 'unitprice', 'salesamount', 'taxamt',
            'englishproductname', 'color', 'englishproductcategoryname', 'englishproductsubcategoryname',
            'salesterritorycountry', 'salesterritoryregion'
        ]]

        analytics_df = analytics_df.rename(columns={
            'englishproductname': 'ProductName',
            'englishproductcategoryname': 'ProductCategory',
            'englishproductsubcategoryname': 'ProductSubcategory',
            'salesterritorycountry': 'Country',
            'salesterritoryregion': 'Region'
        })

        # --- Calculated Column ---
        analytics_df['TotalRevenue'] = analytics_df['salesamount'] + analytics_df['taxamt']

        logger.info("Columns selected, renamed, and new 'TotalRevenue' column created.")

        transformed_data['analytics_sales'] = analytics_df

        logger.info(f"Transformation complete. Final analytics table has {len(analytics_df)} rows.")

        return transformed_data

    except KeyError as e:
        logger.error(f"Transformation failed: A required table is missing from extracted_data: {e}")
        raise
    except Exception as e:
        logger.error(f"An error occurred during data transformation: {e}")
        raise
