import pandas as pd

df = pd.read_csv('data/olist_customers_dataset.csv')

kolom = df.columns.tolist()

tipe_kolom = df.dtypes

jumlah_data = df.shape

baris, colum = df.shape

print(df.head(10))

print(kolom)

print(tipe_kolom)

print(df.info())


print(jumlah_data)