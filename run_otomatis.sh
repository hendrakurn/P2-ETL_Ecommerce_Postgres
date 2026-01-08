#!/usr/bin/env bash
set -e

echo "[1] Build images"
docker compose build

echo "[2] Start services (db + etl dependencies)"
docker compose up -d db

echo "[3] Tunggu Postgres ready..."
# opsi 1: pakai healthcheck di compose (sudah kita buat)
# cukup sleep dikit sebagai safety tambahan
sleep 10

echo "[4] Jalankan ETL"
# Jalankan container etl sekali (one-off run)
docker compose run --rm etl python load_ecommerce.py

echo "[5] Jalankan reporting queries"
# Contoh: pakai psql di dalam container db
#docker compose exec -T db psql -U postgres -d sales_db -f /queries/queries.sql
docker compose exec -T db psql -U ecommerce -d database_ecommerce -f /queries/queries.sql

echo "[6] Selesai. Cek hasil:"
docker compose exec -it db psql -U ecommerce -d database_ecommerce -c '\dt'

echo "[7] contoh queries table customers 10 rows:"
docker compose exec -it db psql -U ecommerce -d database_ecommerce -c 'SELECT * FROM customers limit 10;'

echo "[8] Stop services"
docker compose down -v