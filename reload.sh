#!/bin/bash

PROJECT_DIR="/home/nerea/disco-roto/servicios-clearbi"
cd "$PROJECT_DIR" || {
  echo "ERROR: No se pudo acceder a $PROJECT_DIR"
  exit 1
}
echo "Borrando volúmenes temporales..."
docker volume prune -f

echo "Deteniendo todos los contenedores..."
docker compose stop

echo "Eliminando contenedor 'erp'..."
docker rm erp

echo "Levantando contenedor 'erp'..."
docker compose up -d erp

echo "Esperando 5 segundos a que 'erp' esté listo..."
sleep 5

echo "Arrancando servicios restantes..."
docker compose start

echo "Ejecutando proceso ETL..."
docker compose run --rm etl



echo "Proceso diario completado."
