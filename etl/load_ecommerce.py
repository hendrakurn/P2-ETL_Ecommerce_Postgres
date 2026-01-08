import sqlite3
import pandas as pd
import psycopg2
import os
from psycopg2.extras import execute_values
import numpy as np

from extract_ecommerce import (
        extract_customers,
        extract_orders,
        extract_order_items,
        extract_products,
        extract_sellers
    )

from transform_ecommerce import (
        clean_customers,
        clean_orders,
        clean_order_items,
        clean_products,
        clean_sellers,
        fact_table
    )


def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "database_ecommerce"),
        user=os.getenv("DB_USER", "ecommerce"),
        password=os.getenv("DB_PASSWORD", "securepassword"),
    )
    return conn

def insert_df(cur, df, table_name):
    if df.empty:
        return
    df = df.replace([np.nan, pd.NaT], [None, None])
    
    cols = df.columns.tolist()
    cols_str = ",".join([f'"{c}"' for c in cols])
    vals_str = ",".join(["%s"] * len(cols))
    insert_query = f'INSERT INTO {table_name} ({cols_str}) VALUES %s'
    tuples = [tuple(x) for x in df.to_numpy()]
    execute_values(cur, insert_query, tuples)


def main():
    customers_raw = extract_customers()
    customers_clean = clean_customers(customers_raw)
    orders_raw = extract_orders()
    orders_clean = clean_orders(orders_raw)
    order_items_raw = extract_order_items()
    order_items_clean = clean_order_items(order_items_raw)
    products_raw = extract_products()
    products_clean = clean_products(products_raw)

    sellers_raw = extract_sellers()
    sellers_clean = clean_sellers(sellers_raw)




    #conn  = sqlite3.connect("ecommerce.db")
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id TEXT PRIMARY KEY,
        customer_unique_id TEXT,
        customer_zip_code_prefix INTEGER,
        customer_city TEXT,
        customer_state TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        product_category_name TEXT,
        product_name_length INTEGER,
        product_description_length INTEGER,
        product_photos_qty INTEGER,
        product_weight_g INTEGER,
        product_length_cm INTEGER,
        product_height_cm INTEGER,
        product_width_cm INTEGER
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sellers (
        seller_id TEXT PRIMARY KEY,
        seller_zip_code_prefix INTEGER,
        seller_city TEXT,
        seller_state TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        customer_id TEXT,
        order_status TEXT,
        order_purchase_timestamp TIMESTAMP,
        order_approved_at TIMESTAMP,
        order_delivered_carrier_date TIMESTAMP,
        order_delivered_customer_date TIMESTAMP,
        order_estimated_delivery_date TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        order_id TEXT,
        order_item_id INTEGER,
        product_id TEXT,
        seller_id TEXT,
        shipping_limit_date TIMESTAMP,
        price REAL,
        freight_value REAL,

        order_status TEXT,
        order_purchase_timestamp TIMESTAMP,

        product_category_name TEXT,

        customer_city TEXT,
        customer_state TEXT,

        seller_city TEXT,
        seller_state TEXT
    );
    """)
    insert_df(cur, customers_clean, "customers")
    insert_df(cur, orders_clean, "orders")
    insert_df(cur, order_items_clean, "order_items")
    insert_df(cur, products_clean, "products")
    insert_df(cur, sellers_clean, "sellers")

    con.commit()
    cur.close()
    con.close()
'''
    customers_clean.to_sql( "customers", con, if_exists="replace", index=False
    )
    orders_clean.to_sql( "orders", con, if_exists="replace", index=False
    )
    order_items_clean.to_sql( "order_items", con, if_exists="replace", index=False
    )
    products_clean.to_sql( "products", con, if_exists="replace", index=False
    )
    sellers_clean.to_sql( "sellers", con, if_exists="replace", index=False
    )  
    fact_table_df = fact_table()
    fact_table_df.to_sql( "fact_table", con, if_exists="replace", index=False
    ) 

    con.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);")
    con.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);")
    con.execute("CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);")
'''



if __name__ == "__main__":
    main()
