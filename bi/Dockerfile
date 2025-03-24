FROM postgres:latest

# Copiamos script y dump de la base de datos
COPY init-bi.sh /docker-entrypoint-initdb.d/init-bi.sh
COPY schema-bi.sql /docker-entrypoint-initdb.d/schema-bi.sql

# Damos permisos de ejecución al script
RUN chmod +x /docker-entrypoint-initdb.d/init-bi.sh