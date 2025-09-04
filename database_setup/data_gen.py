from faker import Faker
from sqlalchemy import create_engine, MetaData, insert, text
from sqlalchemy.orm import sessionmaker
import random

# --- Configuration ---
fake = Faker('en_US')

DB_URL = 'postgresql://etl_user:etl_paswd@localhost:5432/etl_db'
engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()
metadata.reflect(bind=engine)

# --- Tables ---
sales_territories = metadata.tables['salesterritory']
product_categories = metadata.tables['productcategory']
product_subcategories = metadata.tables['productsubcategory']
products = metadata.tables['product']
sales_fact = metadata.tables['factinternetsales']

# 🔄 Cleaning tables before populating
session.execute(
    text("""
    TRUNCATE TABLE factinternetsales,
                  product,
                  productsubcategory,
                  productcategory,
                  salesterritory RESTART IDENTITY CASCADE;
    """)
)
session.commit()

# --- Populate SalesTerritory ---
territory_records = [{
    'salesterritoryregion': fake.state(),
    'salesterritorycountry': fake.country()
} for _ in range(10)]

result = session.execute(
    insert(sales_territories).returning(sales_territories.c.salesterritorykey),
    territory_records
)
territory_keys = [r[0] for r in result.fetchall()]

# --- Populate ProductCategory ---
categories = ['Bikes', 'Components', 'Clothing', 'Accessories']
category_records = [{'englishproductcategoryname': c} for c in categories]

result = session.execute(
    insert(product_categories).returning(product_categories.c.productcategorykey),
    category_records
)
category_keys = [r[0] for r in result.fetchall()]

# --- Populate ProductSubcategory ---
subcategories = [
    {'englishproductsubcategoryname': 'Mountain Bikes', 'productcategorykey': category_keys[0]},
    {'englishproductsubcategoryname': 'Road Bikes', 'productcategorykey': category_keys[0]},
    {'englishproductsubcategoryname': 'Helmets', 'productcategorykey': category_keys[3]},
    {'englishproductsubcategoryname': 'Jerseys', 'productcategorykey': category_keys[2]},
    {'englishproductsubcategoryname': 'Wheels', 'productcategorykey': category_keys[1]}
]

result = session.execute(
    insert(product_subcategories).returning(product_subcategories.c.productsubcategorykey),
    subcategories
)
subcategory_keys = [r[0] for r in result.fetchall()]

# --- Populate Product ---
product_records = []
for _ in range(200):
    sub_idx = random.randint(0, len(subcategories)-1)
    subcat_key = subcategory_keys[sub_idx]
    subcat_name = subcategories[sub_idx]['englishproductsubcategoryname']
    product_records.append({
        'englishproductname': f"{fake.word().capitalize()} {subcat_name[:-1]}",
        'color': fake.color_name(),
        'size': random.choice(['S', 'M', 'L', 'XL']),
        'listprice': round(random.uniform(50.0, 3000.0), 2),
        'productsubcategorykey': subcat_key
    })

result = session.execute(
    insert(products).returning(products.c.productkey),
    product_records
)
product_keys = [r[0] for r in result.fetchall()]

session.commit()

# --- Populate FactInternetSales ---
sales_records = []
for i in range(10000):
    product_idx = random.randint(0, len(product_keys)-1)
    product_key = product_keys[product_idx]
    territory_key = random.choice(territory_keys)
    unit_price = product_records[product_idx]['listprice']
    qty = random.randint(1, 5)
    sales_amount = round(unit_price * qty, 2)
    tax_amt = round(sales_amount * random.uniform(0.05, 0.12), 2)

    sales_records.append({
        'salesordernumber': f'SO{70000 + i}',
        'orderdate': fake.date_between(start_date='-3y', end_date='today'),
        'orderquantity': qty,
        'unitprice': unit_price,
        'salesamount': sales_amount,
        'taxamt': tax_amt,
        'productkey': product_key,
        'salesterritorykey': territory_key
    })

# Insert in batches
batch_size = 1000
for i in range(0, len(sales_records), batch_size):
    session.execute(insert(sales_fact), sales_records[i:i+batch_size])

session.commit()
session.close()
print("Database populated successfully!")
