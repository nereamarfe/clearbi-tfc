#!/bin/bash
set -e  # Detener el script si hay un error

echo "Esperando a que PostgreSQL esté listo..."
until PGPASSWORD=$POSTGRES_ERP_PASSWORD psql -U postgres -d postgres -c "SELECT 1" &>/dev/null; do
  sleep 2
done

echo "PostgreSQL está listo."

echo "Verificando existencia del archivo de backup..."
if [ ! -f "/docker-entrypoint-initdb.d/backup.dump" ]; then
    echo "ERROR: No se encontró el archivo /backup.dump dentro del contenedor."
    exit 1
fi

echo "Archivo de backup encontrado."

echo "Verificando si el usuario '$POSTGRES_ERP_USER' existe..."
USER_EXISTS=$(PGPASSWORD=$POSTGRES_PASSWORD psql -U postgres -d postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$POSTGRES_ERP_USER';")

if [ "$USER_EXISTS" != "1" ]; then
  echo "El usuario '$POSTGRES_ERP_USER' no existe. Creándolo..."
  PGPASSWORD=$POSTGRES_PASSWORD psql -U postgres -d postgres -c "CREATE ROLE $POSTGRES_ERP_USER WITH LOGIN SUPERUSER PASSWORD '$POSTGRES_ERP_PASSWORD';"
else
  echo "El usuario '$POSTGRES_ERP_USER' ya existe."
fi

echo "Eliminando base de datos anterior si existe..."
PGPASSWORD=$POSTGRES_ERP_PASSWORD psql -U "$POSTGRES_ERP_USER" -d postgres -c "DROP DATABASE IF EXISTS $POSTGRES_ERP_DB;"

echo "Creando nueva base de datos..."
PGPASSWORD=$POSTGRES_ERP_PASSWORD psql -U "$POSTGRES_ERP_USER" -d postgres -c "CREATE DATABASE $POSTGRES_ERP_DB;"

echo "Verificando que la base de datos se haya creado correctamente..."
PGPASSWORD=$POSTGRES_ERP_PASSWORD psql -U "$POSTGRES_ERP_USER" -d postgres -c "\l"

echo "Restaurando backup en $POSTGRES_ERP_DB..."
PGPASSWORD=$POSTGRES_ERP_PASSWORD pg_restore -U "$POSTGRES_ERP_USER" -d $POSTGRES_ERP_DB --no-owner --exit-on-error /docker-entrypoint-initdb.d/backup.dump

echo "Verificando que la restauración fue exitosa..."
PGPASSWORD=$POSTGRES_ERP_PASSWORD psql -U "$POSTGRES_ERP_USER" -d $POSTGRES_ERP_DB -c "\dn"

echo "Restauración completada."