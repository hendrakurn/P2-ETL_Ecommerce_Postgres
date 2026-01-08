import pandas as pd

df_customers = pd.read_csv('data/olist_customers_dataset.csv')
df_orders = pd.read_csv('data/olist_orders_dataset.csv')
df_order_items = pd.read_csv('data/olist_order_items_dataset.csv')
df_products = pd.read_csv('data/olist_products_dataset.csv')
df_sellers = pd.read_csv('data/olist_sellers_dataset.csv')

def extract_customers():
    return pd.read_csv("data/olist_customers_dataset.csv")

def extract_orders():
    return pd.read_csv("data/olist_orders_dataset.csv")

def extract_order_items():
    return pd.read_csv("data/olist_order_items_dataset.csv")

def extract_products():
    return pd.read_csv("data/olist_products_dataset.csv")

def extract_sellers():
    return pd.read_csv("data/olist_sellers_dataset.csv")


# tampilkan informasi tiap datao

if __name__ == "__main__":
#customers
    print("="*70)
    print("Customers Dataset Info:")
    print("="*5, "5 DATA PERTAMA", "="*5)
    print(df_customers.head())
    print("\n", "="*5, "JUMLAH DATA", "="*5)
    print(df_customers.shape)
    print("\n", "="*5, "TIPE DATA", "="*5)
    print(df_customers.dtypes)
    print("\n", "="*5, "NaN VALUE", "="*5)
    print(df_customers.isnull().sum())
    print("\n", "="*5, "CUSTOMER_ID", "="*5)
    print(df_customers["customer_id"].nunique())
    print("NaN value customer_id:", df_customers["customer_id"].isna().sum())
    print("\n", "="*5, "INFO DATAFRAME", "="*5)
    print(df_customers.info())
    print("\n\n")

    #orders
    print("="*70)
    print("Orders Dataset Info:")
    print("="*5, "5 DATA PERTAMA", "="*5)
    print(df_orders.head())
    print("\n", "="*5, "JUMLAH DATA", "="*5)
    print(df_orders.shape)
    print("\n", "="*5, "NaN VALUE", "="*5)
    print(df_orders.isnull().sum())
    print("\n", "="*5, "ORDER_ID", "="*5)
    print(df_orders["order_id"].nunique())
    print("NaN value order_id:", df_orders["order_id"].isna().sum())
    print("\n", "="*5, "TIPE DATA", "="*5)
    print(df_orders.dtypes)
    print("\n", "="*5, "INFO DATAFRAME", "="*5)
    print(df_orders.info())
    print("\n\n")   

    #order items
    print("="*70)
    print("Order Items Dataset Info:")
    print("="*5, "5 DATA PERTAMA", "="*5)
    print(df_order_items.head())
    print("\n", "="*5, "JUMLAH DATA", "="*5)
    print(df_order_items.shape)
    print("\n", "="*5, "NaN VALUE", "="*5)
    print(df_order_items.isnull().sum())
    print("\n", "="*5, "ORDER_ID", "="*5)
    print(df_order_items["order_id"].nunique())
    print("NaN value order_id:", df_order_items["order_id"].isna().sum())
    print("\n", "="*5, "TIPE DATA", "="*5)
    print(df_order_items.dtypes)
    print("\n", "="*5, "INFO DATAFRAME", "="*5)
    print(df_order_items.info())
    print("\n\n")   


    #products
    print("="*70)
    print("Products Dataset Info:")
    print("="*5, "5 DATA PERTAMA", "="*5)
    print(df_products.head())
    print("\n", "="*5, "JUMLAH DATA", "="*5)
    print(df_products.shape)
    print("\n", "="*5, "NaN VALUE", "="*5)
    print(df_products.isnull().sum())
    print("\n", "="*5, "PRODUCT_ID", "="*5)
    print(df_products["product_id"].nunique())
    print("NaN value product_id:", df_products["product_id"].isna().sum())
    print("\n", "="*5, "TIPE DATA", "="*5)
    print(df_products.dtypes)
    print("\n", "="*5, "INFO DATAFRAME", "="*5)
    print(df_products.info())
    print("\n\n")   

    #sellers
    print("="*70)
    print("Sellers Dataset Info:")      
    print("="*5, "5 DATA PERTAMA", "="*5)
    print(df_sellers.head())
    print("\n", "="*5, "JUMLAH DATA", "="*5)
    print(df_sellers.shape)
    print("\n", "="*5, "NaN VALUE", "="*5)
    print(df_sellers.isnull().sum())
    print("\n", "="*5, "SELLER_ID", "="*5)
    print(df_sellers["seller_id"].nunique())
    print("NaN value seller_id:", df_sellers["seller_id"].isna().sum())
    print("\n", "="*5, "TIPE DATA", "="*5)
    print(df_sellers.dtypes)
    print("\n", "="*5, "INFO DATAFRAME", "="*5)
    print(df_sellers.info())
    print("\n\n")
    # Merge datasets

    print(df_customers.shape)
    print(df_orders.shape)
    print(df_order_items.shape)
    print(df_products.shape)
    print(df_sellers.shape)
