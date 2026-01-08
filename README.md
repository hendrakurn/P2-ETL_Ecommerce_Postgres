#  E-Commerce ETL Pipeline dengan Docker & PostgreSQL

Project ini merupakan **end-to-end ETL (Extract, Transform, Load) pipeline** untuk data e-commerce menggunakan **Python**, **Docker**, dan **PostgreSQL**. Pipeline ini mengolah data transaksi e-commerce dari [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) untuk analisis bisnis.

##  Dataset Overview

Dataset yang digunakan berisi transaksi e-commerce di Brazil (2016-2018) dengan 5 tabel utama:

| Tabel | Jumlah Baris | Deskripsi |
|-------|-------------|-----------|
| `customers` | 99,441 | Data pelanggan (lokasi, ID unik) |
| `orders` | 99,441 | Data pesanan dengan status dan timestamp |
| `order_items` | 112,650 | Detail item per order (harga, produk, penjual) |
| `products` | 32,951 | Data produk dan kategori |
| `sellers` | 3,095 | Data penjual dan lokasi |

##  Arsitektur & Teknologi

```mermaid
graph LR
    A[CSV Files] --> B[Extract]
    B --> C[Transform & Clean]
    C --> D[Load to PostgreSQL]
    D --> E[Docker Container]
    E --> F[Analytics Ready]
    
    style A fill:#0d47a1
    style B fill:#e65100
    style C fill:#880e4f
    style D fill:#1b5e20
    style E fill:#4a148c
    style F fill:#b71c1c

```


## Detailed Architecture Diagram

### System Architecture

```mermaid
graph TB
    subgraph "Host Machine"
        DATA[(" data/<br/>CSV Files")]
        SCRIPT[" run_otomatis.sh<br/>(Automation Script)"]
        QUERIES[(" queries/<br/>SQL Files")]
    end
    
    subgraph "Docker Environment"
        subgraph "ETL Container"
            EXTRACT[" Extract<br/>extract_ecommerce.py"]
            TRANSFORM[" Transform<br/>transform_ecommerce.py"]
            LOAD[" Load<br/>load_ecommerce.py"]
        end
        
        subgraph "PostgreSQL Container"
            DB[(" PostgreSQL 13<br/>database_ecommerce")]
            TABLES[" Tables:<br/>• customers<br/>• orders<br/>• order_items<br/>• products<br/>• sellers"]
        end
    end
    
    subgraph "Output/Analytics"
        ANALYTICS[" Analytics Ready<br/>• SQL Queries<br/>• Business Intelligence<br/>• Reporting"]
    end
    
    DATA -->|"Read CSV"| EXTRACT
    EXTRACT -->|"Raw DataFrames"| TRANSFORM
    TRANSFORM -->|"Cleaned Data"| LOAD
    LOAD -->|"psycopg2<br/>INSERT"| DB
    DB --> TABLES
    QUERIES -->|"Validation<br/>Queries"| DB
    TABLES --> ANALYTICS
    SCRIPT -.->|"Orchestrate"| EXTRACT
    SCRIPT -.->|"Execute"| QUERIES
    
    style DATA fill:#0d47a1,stroke:#90caf9,color:#e3f2fd
    style EXTRACT fill:#e65100,stroke:#ffcc80,color:#fff3e0
    style TRANSFORM fill:#880e4f,stroke:#f48fb1,color:#fce4ec
    style LOAD fill:#1b5e20,stroke:#a5d6a7,color:#e8f5e9
    style DB fill:#4a148c,stroke:#ce93d8,color:#f3e5f5
    style TABLES fill:#b71c1c,stroke:#ef9a9a,color:#ffebee
    style ANALYTICS fill:#1b5e20,stroke:#81c784,color:#e8f5e9
    style SCRIPT fill:#f57f17,stroke:#fff59d,color:#fffde7

```

### ETL Data Flow

```mermaid
flowchart LR
    subgraph INPUT[" Input Data"]
        C1["customers.csv<br/>99,441 rows"]
        O1["orders.csv<br/>99,441 rows"]
        OI1["order_items.csv<br/>112,650 rows"]
        P1["products.csv<br/>32,951 rows"]
        S1["sellers.csv<br/>3,095 rows"]
    end
    
    subgraph EXTRACT["1️ EXTRACT"]
        E["Read CSV<br/>with pandas"]
    end
    
    subgraph TRANSFORM["2️ TRANSFORM"]
        CLEAN["Data Cleaning:<br/>• Remove duplicates<br/>• Convert timestamps<br/>• Handle nulls<br/>• Drop invalid rows"]
        MERGE["Data Merging:<br/>order_items → orders<br/>→ products → customers"]
    end
    
    subgraph LOAD["3️ LOAD"]
        CREATE["Create Tables<br/>in PostgreSQL"]
        INSERT["Bulk Insert<br/>with execute_values"]
    end
    
    subgraph OUTPUT[" Output"]
        T1["customers<br/>99,441 rows"]
        T2["orders<br/>99,441 rows"]
        T3["order_items<br/>112,650 rows"]
        T4["products<br/>32,949 rows"]
        T5["sellers<br/>3,095 rows"]
    end
    
    C1 & O1 & OI1 & P1 & S1 --> E
    E --> CLEAN
    CLEAN --> MERGE
    MERGE --> CREATE
    CREATE --> INSERT
    INSERT --> T1 & T2 & T3 & T4 & T5
    
    style INPUT fill:#0d47a1,color:#e3f2fd
    style EXTRACT fill:#e65100,color:#fff3e0
    style TRANSFORM fill:#880e4f,color:#fce4ec
    style LOAD fill:#1b5e20,color:#e8f5e9
    style OUTPUT fill:#4a148c,color:#f3e5f5

```

### Docker Container Communication

```mermaid
graph LR
    subgraph DC["Docker Compose Orchestration"]
        direction TB
        
        subgraph ETL_C["ETL Container"]
            PY["Python 3.x<br/>+ pandas<br/>+ psycopg2"]
            VOL1["Volume:<br/>/app/data<br/>(bind mount)"]
        end
        
        subgraph DB_C["Database Container"]
            PG["PostgreSQL 13<br/>Port: 5432"]
            VOL2["Volume:<br/>db_data<br/>(persistent)"]
            VOL3["Volume:<br/>/queries<br/>(bind mount)"]
        end
    end
    
    subgraph HOST["Host System"]
        CSV["CSV Files<br/>./data/"]
        SQL["SQL Scripts<br/>./queries/"]
        PORT["Access:<br/>localhost:5434"]
    end
    
    CSV -->|"Mount"| VOL1
    SQL -->|"Mount"| VOL3
    PY -->|"TCP<br/>db:5432"| PG
    PG -->|"Persist"| VOL2
    PG -->|"Expose"| PORT
    
    style ETL_C fill:#0d47a1,stroke:#90caf9
    style DB_C fill:#4a148c,stroke:#ce93d8
    style HOST fill:#f57f17,stroke:#fff59d
    style PY fill:#1565c0
    style PG fill:#6a1b9a

```

### Database Relationship Schema

```mermaid
erDiagram
    CUSTOMERS ||--o{ ORDERS : "places"
    ORDERS ||--|{ ORDER_ITEMS : "contains"
    PRODUCTS ||--o{ ORDER_ITEMS : "included_in"
    SELLERS ||--o{ ORDER_ITEMS : "sells"
    
    CUSTOMERS {
        string customer_id PK
        string customer_unique_id
        int customer_zip_code_prefix
        string customer_city
        string customer_state
    }
    
    ORDERS {
        string order_id PK
        string customer_id FK
        string order_status
        timestamp order_purchase_timestamp
        timestamp order_approved_at
        timestamp order_delivered_carrier_date
        timestamp order_delivered_customer_date
        timestamp order_estimated_delivery_date
    }
    
    ORDER_ITEMS {
        string order_id FK
        int order_item_id
        string product_id FK
        string seller_id FK
        timestamp shipping_limit_date
        float price
        float freight_value
    }
    
    PRODUCTS {
        string product_id PK
        string product_category_name
        int product_name_length
        int product_description_length
        int product_photos_qty
        int product_weight_g
        int product_length_cm
        int product_height_cm
        int product_width_cm
    }
    
    SELLERS {
        string seller_id PK
        int seller_zip_code_prefix
        string seller_city
        string seller_state
    }
```





### Tech Stack
- **Python 3.x** - ETL scripting
- **Pandas** - Data transformation
- **PostgreSQL 13** - Database warehouse
- **Docker & Docker Compose** - Containerization
- **psycopg2** - PostgreSQL connector

##  Struktur Project

```
p1_E-Commerce/
├── data/                           # Dataset CSV (raw data)
│   ├── olist_customers_dataset.csv
│   ├── olist_orders_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_products_dataset.csv
│   └── olist_sellers_dataset.csv
├── etl/                            # ETL scripts
│   ├── extract_ecommerce.py        # Extract: Membaca CSV
│   ├── transform_ecommerce.py      # Transform: Cleaning & merging
│   ├── load_ecommerce.py           # Load: Insert ke PostgreSQL
│   ├── dockerfile                  # Docker image untuk ETL
│   └── requirements.txt            # Python dependencies
├── queries/
│   └── queries.sql                 # SQL queries untuk validasi
├── docker-compose.yaml             # Orchestration config
└── run_otomatis.sh                 # Automated run script
```

##  ETL Flow

### 1️ **Extract**
- Membaca 5 file CSV dari folder `data/`
- Validasi struktur data dan tipe data
- Menampilkan info dataset (shape, null values, data types)

### 2️ **Transform**
**Cleaning per tabel:**
-  **Customers**: Remove duplicates
-  **Orders**: Remove duplicates + convert timestamps to datetime
-  **Order Items**: Remove duplicates + validate price/freight
-  **Products**: Remove duplicates + drop rows with null physical attributes
-  **Sellers**: Remove duplicates

**Merging:**
```
order_items (anchor)
  ↓ JOIN orders (on: order_id)
  ↓ JOIN products (on: product_id)
  ↓ JOIN customers (on: customer_id)
  = Fact Table (112,650 rows × 26 columns)
```

### 3️ **Load**
- Membuat koneksi ke PostgreSQL di Docker
- Create tables dengan schema yang sesuai
- Insert data cleaned ke PostgreSQL
- Validasi dengan sample queries

##  Cara Menjalankan

### Prasyarat
```bash
# Install Docker dan Docker Compose
docker --version
docker-compose --version
```

### Option 1: Automated Run (Recommended)
```bash
# Jalankan seluruh pipeline otomatis
bash run_otomatis.sh
```

Script ini akan:
1. Build Docker images
2. Start PostgreSQL container
3. Jalankan ETL pipeline
4. Validasi data dengan queries
5. Show sample results

### Option 2: Manual Step-by-Step
```bash
# 1. Build images
docker compose build

# 2. Start database container
docker compose up -d db

# 3. Tunggu database ready (check health)
docker compose ps

# 4. Jalankan ETL
docker compose run --rm etl python load_ecommerce.py

# 5. Validasi hasil
docker compose exec -it db psql -U ecommerce -d database_ecommerce -c '\dt'
```

##  Validasi & Testing

### Cek Tabel yang Terload
```bash
docker compose exec -it db psql -U ecommerce -d database_ecommerce -c '\dt'
```

Expected output:
```
 Schema |    Name     | Type  |   Owner   
--------+-------------+-------+-----------
 public | customers   | table | ecommerce
 public | order_items | table | ecommerce
 public | orders      | table | ecommerce
 public | products    | table | ecommerce
 public | sellers     | table | ecommerce
```

### Sample Query
```bash
# Lihat 10 customers pertama
docker compose exec -it db psql -U ecommerce -d database_ecommerce \
  -c 'SELECT * FROM customers LIMIT 10;'

# Jalankan custom queries
docker compose exec -T db psql -U ecommerce -d database_ecommerce \
  -f /queries/queries.sql
```

##  Database Schema

### Customers
```sql
customer_id (PK), customer_unique_id, customer_zip_code_prefix, 
customer_city, customer_state
```

### Orders
```sql
order_id (PK), customer_id (FK), order_status, 
order_purchase_timestamp, order_approved_at, 
order_delivered_carrier_date, order_delivered_customer_date,
order_estimated_delivery_date
```

### Order Items
```sql
order_id (FK), order_item_id, product_id (FK), seller_id (FK),
shipping_limit_date, price, freight_value
```

### Products
```sql
product_id (PK), product_category_name, product_name_length,
product_description_length, product_photos_qty, product_weight_g,
product_length_cm, product_height_cm, product_width_cm
```

### Sellers
```sql
seller_id (PK), seller_zip_code_prefix, seller_city, seller_state
```

##  Use Cases & Analytics

Data hasil ETL dapat digunakan untuk:
-  **Monthly Sales Trend** - Analisis revenue per bulan
-  **Top Products by Revenue** - Produk terlaris berdasarkan kategori
-  **Geographic Analysis** - Distribusi pelanggan dan penjual per region
-  **Delivery Performance** - Analisis ketepatan waktu pengiriman
-  **Customer Segmentation** - Segmentasi based on purchase behavior

## Configuration

### Environment Variables
Database connection di-configure via environment variables di `docker-compose.yaml`:
```yaml
DB_HOST: db
DB_USER: ecommerce
DB_PASSWORD: securepassword
DB_NAME: database_ecommerce
DB_PORT: 5432 (internal) → 5434 (host)
```

### Local Connection (dari host)
```bash
psql -h localhost -p 5434 -U ecommerce -d database_ecommerce
# Password: securepassword
```

## Cleanup

```bash
# Stop containers
docker compose down

# Stop + hapus volumes (reset database)
docker compose down -v
```




**Author**: Hendra  
**Project Type**: Data Engineering Portfolio  
**Tech**: Python | PostgreSQL | Docker | pandas
