FROM metabase/metabase:latest

# Instalar cliente de PostgreSQL en Alpine
RUN apk update && apk add --no-cache postgresql-client bash curl

# Copiar el script de espera
COPY wait-for-etl.sh /wait-for-etl.sh
RUN chmod +x /wait-for-etl.sh

# Establecer el script como entrypoint
ENTRYPOINT ["/wait-for-etl.sh"]

# Dejar el comando original de Metabase como argumento por defecto
CMD ["/app/run_metabase.sh"]
