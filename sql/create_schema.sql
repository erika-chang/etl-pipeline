-- Drop tables in reverse order of creation
DROP TABLE IF EXISTS FactInternetSales;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS ProductSubcategory;
DROP TABLE IF EXISTS ProductCategory;
DROP TABLE IF EXISTS SalesTerritory;

-- Create SalesTerritory Table
CREATE TABLE SalesTerritory (
    SalesTerritoryKey SERIAL PRIMARY KEY,
    SalesTerritoryRegion VARCHAR(50) NOT NULL,
    SalesTerritoryCountry VARCHAR(50) NOT NULL
);

-- Create ProductCategory Table
CREATE TABLE ProductCategory (
    ProductCategoryKey SERIAL PRIMARY KEY,
    EnglishProductCategoryName VARCHAR(50) NOT NULL
);

-- Create ProductSubcategory Table
CREATE TABLE ProductSubcategory (
    ProductSubcategoryKey SERIAL PRIMARY KEY,
    EnglishProductSubcategoryName VARCHAR(50) NOT NULL,
    ProductCategoryKey INT REFERENCES ProductCategory(ProductCategoryKey)
);

-- Create Product Table
CREATE TABLE Product (
    ProductKey SERIAL PRIMARY KEY,
    EnglishProductName VARCHAR(100) NOT NULL,
    Color VARCHAR(20),
    Size VARCHAR(10),
    ListPrice DECIMAL(19, 4),
    ProductSubcategoryKey INT REFERENCES ProductSubcategory(ProductSubcategoryKey)
);

-- Create FactInternetSales Table
CREATE TABLE FactInternetSales (
    SalesOrderNumber VARCHAR(20) NOT NULL,
    OrderDate DATE NOT NULL,
    OrderQuantity INT NOT NULL,
    UnitPrice DECIMAL(19, 4) NOT NULL,
    SalesAmount DECIMAL(19, 4) NOT NULL,
    TaxAmt DECIMAL(19, 4) NOT NULL,
    ProductKey INT REFERENCES Product(ProductKey),
    SalesTerritoryKey INT REFERENCES SalesTerritory(SalesTerritoryKey),
    PRIMARY KEY (SalesOrderNumber, ProductKey)
);
