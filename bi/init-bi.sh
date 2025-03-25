#!/bin/bash
set -e  # Detener el script si hay un error

echo "Esperando a que PostgreSQL esté listo..."
until PGPASSWORD=$POSTGRES_BI_PASSWORD psql -U postgres -d postgres -c "SELECT 1" &>/dev/null; do
  sleep 2
done

echo "PostgreSQL está listo."

echo "Verificando existencia del archivo de schema..."
if [ ! -f "/docker-entrypoint-initdb.d/schema-bi.sql" ]; then
    echo "ERROR: No se encontró el archivo /schema-bi.sql dentro del contenedor."
    exit 1
fi

echo "Archivo de schema encontrado."

echo "Verificando si el usuario '$POSTGRES_BI_USER' existe..."
USER_EXISTS=$(PGPASSWORD=$POSTGRES_PASSWORD psql -U postgres -d postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$POSTGRES_BI_USER';")

if [ "$USER_EXISTS" != "1" ]; then
  echo "El usuario '$POSTGRES_BI_USER' no existe. Creándolo..."
  PGPASSWORD=$POSTGRES_PASSWORD psql -U postgres -d postgres -c "CREATE ROLE $POSTGRES_BI_USER WITH LOGIN SUPERUSER PASSWORD '$POSTGRES_BI_PASSWORD';"
else
  echo "El usuario '$POSTGRES_BI_USER' ya existe."
fi

echo "Eliminando base de datos anterior si existe..."
PGPASSWORD=$POSTGRES_BI_PASSWORD psql -U "$POSTGRES_BI_USER" -d postgres -c "DROP DATABASE IF EXISTS $POSTGRES_BI_DB;"

echo "Creando nueva base de datos..."
PGPASSWORD=$POSTGRES_BI_PASSWORD psql -U "$POSTGRES_BI_USER" -d postgres -c "CREATE DATABASE $POSTGRES_BI_DB;"

echo "Creando nueva base de datos metabase vacía..."
PGPASSWORD=$POSTGRES_BI_PASSWORD psql -U "$POSTGRES_BI_USER" -d postgres -c "CREATE DATABASE $MB_DB_DBNAME;"

echo "Verificando que la base de datos se haya creado correctamente..."
PGPASSWORD=$POSTGRES_BI_PASSWORD psql -U "$POSTGRES_BI_USER" -d postgres -c "\l"

echo "Creando schema y tablas BI"
PGPASSWORD=$POSTGRES_BI_PASSWORD psql -U "$POSTGRES_BI_USER" -d "$POSTGRES_BI_DB" -f /docker-entrypoint-initdb.d/schema-bi.sql

echo "BI creado"
