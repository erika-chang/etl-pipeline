from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SalesTerritory(Base):
    __tablename__ = 'salesterritory'
    sales_territory_key = Column(Integer, primary_key=True)
    sales_territory_region = Column(String(50), nullable=False)
    sales_territory_country = Column(String(50), nullable=False)

class ProductCategory(Base):
    __tablename__ = 'productcategory'
    product_category_key = Column(Integer, primary_key=True)
    english_product_category_name = Column(String(50), nullable=False)

class ProductSubcategory(Base):
    __tablename__ = 'productsubcategory'
    product_subcategory_key = Column(Integer, primary_key=True)
    english_product_subcategory_name = Column(String(50), nullable=False)
    product_category_key = Column(Integer, ForeignKey('productcategory.product_category_key'))

class Product(Base):
    __tablename__ = 'product'
    product_key = Column(Integer, primary_key=True)
    english_product_name = Column(String(100), nullable=False)
    color = Column(String(20))
    size = Column(String(10))
    list_price = Column(Numeric(19, 4))
    product_subcategory_key = Column(Integer, ForeignKey('productsubcategory.product_subcategory_key'))

class FactInternetSales(Base):
    __tablename__ = 'factinternetsales'
    sales_order_number = Column(String(20), primary_key=True)
    product_key = Column(Integer, ForeignKey('product.product_key'), primary_key=True)
    order_date = Column(Date, nullable=False)
    order_quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(19, 4), nullable=False)
    sales_amount = Column(Numeric(19, 4), nullable=False)
    tax_amt = Column(Numeric(19, 4), nullable=False)
    sales_territory_key = Column(Integer, ForeignKey('salesterritory.sales_territory_key'))
