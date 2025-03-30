# Makefile para automatización del proceso ETL y actualización diaria

PROJECT_DIR := /home/user/servicios-clearbi

.PHONY: all clean stop remove_erp start_erp start_services run_etl reload

all: reload

# Limpia volúmenes temporales
clean:
	docker volume prune -f

# Detiene todos los contenedores
stop:
	cd $(PROJECT_DIR) && docker compose stop

# Elimina contenedor 'erp'
remove_erp:
	cd $(PROJECT_DIR) && docker rm erp || true

# Levanta contenedor 'erp'
start_erp:
	cd $(PROJECT_DIR) && docker compose up -d erp
	sleep 5

# Arranca los servicios restantes
start_services:
	cd $(PROJECT_DIR) && docker compose start

# Ejecuta el proceso ETL
run_etl:
	cd $(PROJECT_DIR) && docker compose run --rm etl

# Pipeline completo
reload: clean stop remove_erp start_erp start_services run_etl
	@echo "Proceso diario completado."
