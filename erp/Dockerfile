FROM postgres:latest

# Copiamos script y dump de la base de datos
COPY init-erp.sh /docker-entrypoint-initdb.d/init-erp.sh
COPY backup.dump /docker-entrypoint-initdb.d/backup.dump

# Damos permisos de ejecución al script
RUN chmod +x /docker-entrypoint-initdb.d/init-erp.sh
