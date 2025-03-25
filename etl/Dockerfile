FROM python:3.12-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar requisitos e instalar dependencias
COPY requirements.txt .
COPY schema-bi.sql .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el script ETL
COPY etl.py .

# Comando por defecto al lanzar el contenedor
CMD ["python", "etl.py"]