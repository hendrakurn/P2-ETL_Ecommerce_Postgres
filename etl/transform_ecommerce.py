import pandas as pd


from extract_ecommerce import (
    extract_customers,
    extract_orders,
    extract_order_items,
    extract_products,
    extract_sellers
)


def clean_customers(customers: pd.DataFrame) -> pd.DataFrame:
    customers_clean = customers.drop_duplicates()
    return customers_clean


def clean_orders(orders: pd.DataFrame) -> pd.DataFrame:
    orders_clean = orders.drop_duplicates()

    date_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for col in date_cols:
        orders_clean[col] = pd.to_datetime(orders_clean[col], errors="coerce")

    orders_clean[date_cols] = orders_clean[date_cols].where(pd.notna(orders_clean[date_cols]), None)

    return orders_clean

def clean_order_items(order_items: pd.DataFrame) -> pd.DataFrame:
    order_items_clean = order_items.drop_duplicates()

    # optional sanity check
    pair_unique = order_items_clean[
        ["order_id", "order_item_id"]
    ].drop_duplicates().shape[0]

    assert pair_unique == len(order_items_clean)

    return order_items_clean

def clean_products(products: pd.DataFrame) -> pd.DataFrame:
    products_clean = products.drop_duplicates()

    products_clean = products_clean.rename(columns={
        "product_name_lenght": "product_name_length",
        "product_description_lenght": "product_description_length"
    })

    

    # drop 2 baris yang ukuran fisiknya NaN
    products_clean = products_clean.dropna(
        subset=[
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm"
        ]
    )

    return products_clean

def clean_sellers(sellers: pd.DataFrame) -> pd.DataFrame:
    return sellers.drop_duplicates()


  
def customers_clean():
    df_customers = extract_customers()
    return clean_customers(df_customers)
def orders_clean():
    df_orders = extract_orders()
    return clean_orders(df_orders)
def order_items_clean():
    df_order_items = extract_order_items()
    return clean_order_items(df_order_items)
def products_clean():
    df_products = extract_products()
    return clean_products(df_products)
def sellers_clean():
    df_sellers = extract_sellers()
    return clean_sellers(df_sellers)
def fact_table():
    df_customers = customers_clean()
    df_orders = orders_clean()
    df_order_items = order_items_clean()
    df_products = products_clean()

    fact_df = pd.merge(
        df_order_items,
        df_orders,
        on="order_id",
        how="left"
    )

    fact_df = pd.merge(
        fact_df,
        df_products,
        on="product_id",
        how="left"
    )

    fact_df = pd.merge(
        fact_df,
        df_customers,
        on="customer_id",
        how="left"
    )

    return fact_df



if __name__ == "__main__":
    customers = extract_customers()
    orders = extract_orders()
    order_items = extract_order_items()
    products = extract_products()
    sellers = extract_sellers()

    customers_clean = clean_customers(customers)
    orders_clean = clean_orders(orders)
    order_items_clean = clean_order_items(order_items)
    products_clean = clean_products(products)
    sellers_clean = clean_sellers(sellers)

    print("Customers clean:", customers_clean.shape)
    print("Orders clean:", orders_clean.shape)
    print("Order Items clean:", order_items_clean.shape)
    print("Products clean:", products_clean.shape)
    print("Sellers clean:", sellers_clean.shape)    

    fact_df = pd.merge(
        order_items_clean,
        orders_clean,
        on="order_id",
        how="left"
    )

    fact_df = pd.merge(
        fact_df,
        products_clean,
        on="product_id",
        how="left"
    )

    fact_df = pd.merge(
        fact_df,
        customers_clean,
        on="customer_id",
        how="left"
    )

    print("\n","="*30,"Kolom tabel hasil merge", "="*30)
    print(fact_df.info())
    print("\n","="*30,"Contoh 10 baris data tabel hasil merge", "="*30)
    
    print(fact_df.head(10))
    print("Ukuran tabel hasil merge:", fact_df.shape)



#print("Transforming Customers Dataset...")
#df_customers = extract_customers()
#df_customers_clean = clean_customers(df_customers)
#print("Customers Dataset transformed. Shape:", df_customers_clean.shape)
