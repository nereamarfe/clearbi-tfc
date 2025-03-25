#!/bin/bash

echo "Esperando a que el ETL termine..."

until PGPASSWORD=$POSTGRES_BI_PASSWORD psql -h bi -U $POSTGRES_BI_USER -d $POSTGRES_BI_DB -c "SELECT * FROM etl_ready LIMIT 1;" > /dev/null 2>&1; do
  echo "Datos no cargados aún... esperando 20s"
  sleep 20
done

echo "Datos cargados. Iniciando Metabase..."
exec "$@"
