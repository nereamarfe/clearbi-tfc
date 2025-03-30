# Sistema de Analítica de Datos para Business Intelligence

Este proyecto forma parte del Trabajo Fin de Ciclo de Desarrollo de Aplicaciones Multiplataforma. Implementa un sistema completo de integración, almacenamiento y análisis de datos para una empresa ficticia dedicada a la venta de bicicletas y accesorios.

---

## 📊 Descripción

El sistema automatiza la extracción, transformación y carga (ETL) de datos provenientes de un ERP, almacena los datos en un **Data Warehouse** en modelo estrella y facilita su análisis mediante la herramienta de visualización **Metabase**.

---

## 🛠️ Arquitectura

- **ERP (PostgreSQL):** Base de datos operativa con datos normalizados.
- **Data Warehouse (PostgreSQL):** Base de datos desnormalizada para análisis.
- **ETL (Python):** Proceso automatizado de carga de datos.
- **Metabase:** Plataforma para consultas y visualización de datos.

Los servicios están orquestados mediante **Docker Compose** y organizados en redes internas para mayor seguridad.

---

## 📝 Estructura del Proyecto

```
.
├── erp/
│   ├── Dockerfile
│   ├── init-erp.sh
│   └── backup.dump
├── bi/
│   ├── Dockerfile
│   ├── init-bi.sh
│   └── schema-bi.sql
├── etl/
│   ├── Dockerfile
│   ├── etl.py
│   ├── schema-bi.sql
│   └── requirements.txt
├── metabase/
│   └── Dockerfile
├── docker-compose.yml
├── .env
└── Makefile
```

---

## 📚 Requisitos

- Docker & Docker Compose
- Make (opcional, recomendado)
- Python 3.12+ (solo para desarrollo local)

---

## 🔧 Configuración

1. Copiar el archivo `.env.example` a `.env` y configurar las variables.
2. Asegurarse de que los puertos **3000**, **3003** y **3004** estén disponibles.

---

## 🚀 Despliegue Rápido

Levanta todo el entorno con un solo comando:

```bash
make up
```

Para detener y eliminar los contenedores:

```bash
make down
```

---

## 💡 Comandos Makefile últiles

| Comando          | Descripción                                      |
|---------------|--------------------------------------------------|
| make up      | Levanta todos los servicios                      |
| make down    | Detiene y elimina los servicios                  |
| make logs    | Muestra los logs de los contenedores             |
| make etl     | Ejecuta el proceso ETL                           |
| make reset-bi| Reinicia la base de datos DWH                    |
| make clear-etl| Limpia la tabla de estado `etl_ready`            |

---

## 📈 Proceso ETL

El proceso ETL realiza las siguientes acciones:

1. Espera que las bases de datos estén disponibles.
2. Elimina y recrea la base de datos **bi**.
3. Carga el esquema estrella desde `schema-bi.sql`.
4. Extrae, transforma y carga datos desde el ERP al DWH.
5. Crea la tabla de control `etl_ready`.

Los logs del proceso se encuentran en `etl/etl.log`.

---

## 🌐 Acceso a Metabase

Una vez iniciado el sistema, puedes acceder a la herramienta de visualización:

- URL: [http://localhost:3000](http://localhost:3000)
- Usuario y contraseña: configurados en el archivo `.env`

La conexión al DWH está preconfigurada para facilitar la creación de dashboards y consultas.

---

## 📚 Licencia

Proyecto desarrollado exclusivamente con fines educativos para el Trabajo Fin de Ciclo.

