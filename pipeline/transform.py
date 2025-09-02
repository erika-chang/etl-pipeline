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

        # --- Merge dimension tables with the fact table ---
        sales_df = extracted_data['FactInternetSales']
        product_df = extracted_data['DimProduct']
        prod_sub_df = extracted_data['DimProductSubcategory']
        prod_cat_df = extracted_data['DimProductCategory']
        territory_df = extracted_data['DimSalesTerritory']

        # Join FactInternetSales with DimProduct
        analytics_df = pd.merge(sales_df, product_df, on='ProductKey', how='left')

        # Join with DimProductSubcategory
        analytics_df = pd.merge(analytics_df, prod_sub_df, on='ProductSubcategoryKey', how='left')

        # Join with DimProductCategory
        analytics_df = pd.merge(analytics_df, prod_cat_df, on='ProductCategoryKey', how='left')

        # Join with DimSalesTerritory
        analytics_df = pd.merge(analytics_df, territory_df, on='SalesTerritoryKey', how='left')

        logger.info("Dataframes merged successfully.")

        # --- Column Selection ---
        # Select and rename columns for the final analytics table
        analytics_df = analytics_df[[
            'OrderDate', 'SalesOrderNumber', 'OrderQuantity', 'UnitPrice', 'SalesAmount', 'TaxAmt',
            'EnglishProductName', 'Color', 'EnglishProductCategoryName', 'EnglishProductSubcategoryName',
            'SalesTerritoryCountry', 'SalesTerritoryRegion'
        ]]

        analytics_df = analytics_df.rename(columns={
            'EnglishProductName': 'ProductName',
            'EnglishProductCategoryName': 'ProductCategory',
            'EnglishProductSubcategoryName': 'ProductSubcategory',
            'SalesTerritoryCountry': 'Country',
            'SalesTerritoryRegion': 'Region'
        })

        # --- Create a new calculated column ---
        analytics_df['TotalRevenue'] = analytics_df['SalesAmount'] + analytics_df['TaxAmt']

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
