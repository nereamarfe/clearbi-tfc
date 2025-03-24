import os
import time
import psycopg2
from psycopg2.extras import execute_values
import logging

# Configuración de logging
logging.basicConfig(
    filename="etl.log", 
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

DB_ERP = {
    "dbname": os.getenv("POSTGRES_ERP_DB"),
    "user": os.getenv("POSTGRES_ERP_USER"),
    "password": os.getenv("POSTGRES_ERP_PASSWORD"),
    "host": os.getenv("ERP_HOST")
}

DB_DWH = {
    "dbname": os.getenv("POSTGRES_BI_DB"),
    "user": os.getenv("POSTGRES_BI_USER"),
    "password": os.getenv("POSTGRES_BI_PASSWORD"),
    "host": os.getenv("BI_HOST")
}

def wait_for_postgres(config):
    print(f"Esperando a que la base de datos '{config["dbname"]}' esté lista...")
    while True:
        try:
            conn = psycopg2.connect(host=config["host"], dbname=config["dbname"], user=config["user"], password=config["password"])
            conn.close()
            logging.info(f"Conexión a la base de datos '{config['dbname']}' exitosa.")
            break
        except Exception as e:
            logging.error(f"La base de datos '{config['dbname']}' no está lista todavía...: {e}")
            time.sleep(5)



# Función para conectar a una base de datos
def connect_db(config):
    try:
        logging.info("Intentando conectar a la base de datos...")
        return psycopg2.connect(
        dbname=config["dbname"],
        user=config["user"],
        password=config["password"],
        host=config["host"])
    except Exception as e:
        logging.error(f"Error al conectar a la base de datos: {e}")
        return None
    

# Extraer y cargar datos en DimCustomer
def extract_load_customers():
    logging.info("Iniciando carga de DimCustomer...")
    try:
        conn_erp = connect_db(DB_ERP)
        cursor_erp = conn_erp.cursor()
        cursor_erp.execute("""
            SELECT DISTINCT c.CustomerID, c.CustomerID AS CustomerBK, p.FirstName, p.LastName,
                   p.FirstName || ' ' || p.LastName AS FullName, pe.EmailAddress, ph.PhoneNumber,
                   c.ModifiedDate, CURRENT_TIMESTAMP AS CreatedDate
            FROM Sales.Customer c
            LEFT JOIN Person.Person p ON c.PersonID = p.BusinessEntityID
            LEFT JOIN Person.EmailAddress pe ON p.BusinessEntityID = pe.BusinessEntityID
            LEFT JOIN Person.PersonPhone ph ON p.BusinessEntityID = ph.BusinessEntityID
            WHERE p.FirstName IS NOT NULL
        """)
        data = cursor_erp.fetchall()
        cursor_erp.close()
        conn_erp.close()

        if not data:
            logging.warning("No se encontraron datos para DimCustomer.")

        conn_dwh = connect_db(DB_DWH)
        cursor_dwh = conn_dwh.cursor()
        insert_query = """
            INSERT INTO adventure_dwh.DimCustomer (CustomerID, CustomerBK, FirstName, LastName, FullName,
                                                   EmailAddress, Phone, ModifiedDate, CreatedDate)
            VALUES %s
        """
        execute_values(cursor_dwh, insert_query, data)
        conn_dwh.commit()
        cursor_dwh.close()
        conn_dwh.close()
        logging.info("DimCustomer cargado con éxito.")
    except Exception as e:
        logging.error(f"Error en extract_load_customers: {e}")

# Extraer y cargar datos en DimProduct con logging
def extract_load_products():
    logging.info("Iniciando carga de DimProduct...")
    try:
        conn_erp = connect_db(DB_ERP)
        cursor_erp = conn_erp.cursor()
        cursor_erp.execute("""
            SELECT p.ProductID AS ProductBK, p.ProductID, p.Name, p.ProductNumber, p.Color,
                   p.StandardCost, p.ListPrice, p.Size, p.Weight, pc.Name AS ProductCategory,
                   psc.Name AS ProductSubcategory, p.ModifiedDate, CURRENT_TIMESTAMP AS CreatedDate
            FROM Production.Product p
            LEFT JOIN Production.ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
            LEFT JOIN Production.ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
        """)
        data = cursor_erp.fetchall()
        cursor_erp.close()
        conn_erp.close()

        if not data:
            logging.warning("No se encontraron datos para DimProduct.")

        conn_dwh = connect_db(DB_DWH)
        cursor_dwh = conn_dwh.cursor()
        insert_query = """
            INSERT INTO adventure_dwh.DimProduct (ProductBK, ProductID, Name, ProductNumber, Color, StandardCost, ListPrice,
                                                  Size, Weight, ProductCategory, ProductSubcategory, ModifiedDate, CreatedDate)
            VALUES %s
        """
        execute_values(cursor_dwh, insert_query, data)
        conn_dwh.commit()
        cursor_dwh.close()
        conn_dwh.close()
        logging.info("DimProduct cargado con éxito.")
    except Exception as e:
        logging.error(f"Error en extract_load_products: {e}")

# Extraer y cargar datos en DimSalesTerritory con logging
def extract_load_sales_territory():
    logging.info("Iniciando carga de DimSalesTerritory...")
    try:
        conn_erp = connect_db(DB_ERP)
        cursor_erp = conn_erp.cursor()
        cursor_erp.execute("""
            SELECT st.TerritoryID AS SalesTerritoryBK, st.TerritoryID, st.Name, st.CountryRegionCode,
                   st.Group AS RegionGroup, st.ModifiedDate, CURRENT_TIMESTAMP AS CreatedDate
            FROM Sales.SalesTerritory st
        """)
        data = cursor_erp.fetchall()
        cursor_erp.close()
        conn_erp.close()

        if not data:
            logging.warning("No se encontraron datos para DimSalesTerritory.")

        conn_dwh = connect_db(DB_DWH)
        cursor_dwh = conn_dwh.cursor()
        insert_query = """
            INSERT INTO adventure_dwh.DimSalesTerritory (SalesTerritoryBK, SalesTerritoryID, Name, CountryRegionCode,
                                                         RegionGroup, ModifiedDate, CreatedDate)
            VALUES %s
        """
        execute_values(cursor_dwh, insert_query, data)
        conn_dwh.commit()
        cursor_dwh.close()
        conn_dwh.close()
        logging.info("DimSalesTerritory cargado con éxito.")
    except Exception as e:
        logging.error(f"Error en extract_load_sales_territory: {e}")

# Extraer y cargar datos en DimShipMethod con logging
def extract_load_ship_methods():
    logging.info("Iniciando carga de DimShipMethod...")
    try:
        conn_erp = connect_db(DB_ERP)
        cursor_erp = conn_erp.cursor()
        cursor_erp.execute("""
            SELECT ShipMethodID AS ShipMethodBK, ShipMethodID, Name, ShipBase, ShipRate,
                   ModifiedDate, CURRENT_TIMESTAMP AS CreatedDate
            FROM Purchasing.ShipMethod
        """)
        data = cursor_erp.fetchall()
        cursor_erp.close()
        conn_erp.close()

        if not data:
            logging.warning("No se encontraron datos para DimShipMethod.")

        conn_dwh = connect_db(DB_DWH)
        cursor_dwh = conn_dwh.cursor()
        insert_query = """
            INSERT INTO adventure_dwh.DimShipMethod (ShipMethodBK, ShipMethodID, Name, ShipBase, ShipRate, ModifiedDate, CreatedDate)
            VALUES %s
        """
        execute_values(cursor_dwh, insert_query, data)
        conn_dwh.commit()
        cursor_dwh.close()
        conn_dwh.close()
        logging.info("DimShipMethod cargado con éxito.")
    except Exception as e:
        logging.error(f"Error en extract_load_ship_methods: {e}")


# Extraer y cargar datos en FactSales con logging
def extract_load_fact_sales():
    logging.info("Iniciando carga de FactSales...")
    try:
        conn_erp = connect_db(DB_ERP)
        cursor_erp = conn_erp.cursor()
        cursor_erp.execute("""
            SELECT soh.SalesOrderID, sod.SalesOrderDetailID,
                   soh.SalesOrderID || '|' || sod.SalesOrderDetailID AS SalesBK,
                   soh.CustomerID, soh.TerritoryID, sod.ProductID, soh.ShipMethodID,
                   TO_CHAR(soh.OrderDate, 'YYYYMMDD')::INTEGER AS OrderDateKey,
                   sod.OrderQty*sod.UnitPrice AS SalesAmount, sod.OrderQty AS Quantity,
                   sod.UnitPriceDiscount AS Discount, sod.UnitPrice,
                   sod.OrderQty * (sod.UnitPrice - sod.UnitPriceDiscount) AS TotalSale,
                   soh.ModifiedDate, CURRENT_TIMESTAMP AS CreatedDate
            FROM Sales.SalesOrderHeader soh
            LEFT JOIN Sales.SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID
        """)
        
        data_erp = cursor_erp.fetchall()
        cursor_erp.close()
        conn_erp.close()

        if not data_erp:
            logging.warning("No se encontraron datos para FactSales.")

        conn_dwh = connect_db(DB_DWH)
        cursor_dwh = conn_dwh.cursor()

        for row in data_erp:
            sales_order_id, sales_order_detail_id, sales_bk, customer_id, territory_id, product_id, ship_method_id, \
            order_date_key, sales_amount, quantity, discount, unit_price, total_sale, modified_date, created_date = row

            cursor_dwh.execute("""
                INSERT INTO adventure_dwh.FactSales (SalesOrderID, SalesOrderDetailID, SalesBK, CustomerKey, ProductKey,
                                                     ShipMethodKey, OrderDateKey, SalesTerritoryKey, SalesAmount, Quantity,
                                                     Discount, UnitPrice, TotalSale, ModifiedDate, CreatedDate)
                SELECT %s, %s, %s,
                       dc.CustomerKey, dp.ProductKey, dsm.ShipMethodKey,
                       %s, dst.SalesTerritoryKey, %s, %s, %s, %s, %s, %s, %s
                FROM adventure_dwh.DimCustomer dc
                LEFT JOIN adventure_dwh.DimSalesTerritory dst ON dst.SalesTerritoryID = %s
                LEFT JOIN adventure_dwh.DimProduct dp ON dp.ProductID = %s
                LEFT JOIN adventure_dwh.DimShipMethod dsm ON dsm.ShipMethodID = %s
                WHERE dc.CustomerID = %s
            """, (sales_order_id, sales_order_detail_id, sales_bk, order_date_key,
                  sales_amount, quantity, discount, unit_price, total_sale, modified_date, created_date,
                  territory_id, product_id, ship_method_id, customer_id))

        conn_dwh.commit()
        cursor_dwh.close()
        conn_dwh.close()
        logging.info("FactSales cargada con éxito.")
    except Exception as e:
        logging.error(f"Error en extract_load_fact_sales: {e}")

# Extraer y cargar datos en DimEmployee con logging
def extract_load_employees():
    logging.info("Iniciando carga de DimEmployee...")
    try:
        conn_erp = connect_db(DB_ERP)
        cursor_erp = conn_erp.cursor()
        cursor_erp.execute("""
            SELECT e.BusinessEntityID AS EmployeeID, p.FirstName, p.LastName,
                   CONCAT(p.FirstName, ' ', p.LastName) AS FullName, e.JobTitle,
                   e.HireDate, e.BirthDate, pe.EmailAddress, ph.PhoneNumber,
                   e.ModifiedDate, CURRENT_TIMESTAMP AS CreatedDate
            FROM HumanResources.Employee e
            LEFT JOIN Person.Person p ON e.BusinessEntityID = p.BusinessEntityID
            LEFT JOIN Person.EmailAddress pe ON p.BusinessEntityID = pe.BusinessEntityID
            LEFT JOIN Person.PersonPhone ph ON p.BusinessEntityID = ph.BusinessEntityID
        """)
        data = cursor_erp.fetchall()
        cursor_erp.close()
        conn_erp.close()

        if not data:
            logging.warning("No se encontraron datos para DimEmployee.")

        conn_dwh = connect_db(DB_DWH)
        cursor_dwh = conn_dwh.cursor()
        insert_query = """
            INSERT INTO adventure_dwh.DimEmployee (EmployeeID, FirstName, LastName, FullName, JobTitle, HireDate, BirthDate,
                                                   EmailAddress, Phone, ModifiedDate, CreatedDate)
            VALUES %s
        """
        execute_values(cursor_dwh, insert_query, data)
        conn_dwh.commit()
        cursor_dwh.close()
        conn_dwh.close()
        logging.info("DimEmployee cargado con éxito.")
    except Exception as e:
        logging.error(f"Error en extract_load_employees: {e}")

# Extraer y cargar datos en DimVendor con logging
def extract_load_vendors():
    logging.info("Iniciando carga de DimVendor...")
    try:
        conn_erp = connect_db(DB_ERP)
        cursor_erp = conn_erp.cursor()
        cursor_erp.execute("""
            SELECT v.BusinessEntityID AS VendorBK, v.BusinessEntityID AS VendorID, v.Name,
                   v.AccountNumber, ph.PhoneNumber, pe.EmailAddress, v.ModifiedDate,
                   CURRENT_TIMESTAMP AS CreatedDate
            FROM Purchasing.Vendor v
            LEFT JOIN Person.Person p ON v.BusinessEntityID = p.BusinessEntityID
            LEFT JOIN Person.EmailAddress pe ON p.BusinessEntityID = pe.BusinessEntityID
            LEFT JOIN Person.PersonPhone ph ON p.BusinessEntityID = ph.BusinessEntityID
        """)
        data = cursor_erp.fetchall()
        cursor_erp.close()
        conn_erp.close()

        if not data:
            logging.warning("No se encontraron datos para DimVendor.")

        conn_dwh = connect_db(DB_DWH)
        cursor_dwh = conn_dwh.cursor()
        insert_query = """
            INSERT INTO adventure_dwh.DimVendor (VendorBK, VendorID, Name, AccountNumber, Phone, EmailAddress,
                                                 ModifiedDate, CreatedDate)
            VALUES %s
        """
        execute_values(cursor_dwh, insert_query, data)
        conn_dwh.commit()
        cursor_dwh.close()
        conn_dwh.close()
        logging.info("DimVendor cargado con éxito.")
    except Exception as e:
        logging.error(f"Error en extract_load_vendors: {e}")


# Extraer y cargar datos en DimLocation con logging
def extract_load_locations():
    logging.info("Iniciando carga de DimLocation...")
    try:
        conn_erp = connect_db(DB_ERP)
        cursor_erp = conn_erp.cursor()
        cursor_erp.execute("""
            SELECT LocationID, LocationID AS LocationBK, Name, CostRate, Availability, ModifiedDate,
                   CURRENT_TIMESTAMP AS CreatedDate
            FROM Production.Location
        """)
        data = cursor_erp.fetchall()
        cursor_erp.close()
        conn_erp.close()

        if not data:
            logging.warning("No se encontraron datos para DimLocation.")

        conn_dwh = connect_db(DB_DWH)
        cursor_dwh = conn_dwh.cursor()
        insert_query = """
            INSERT INTO adventure_dwh.DimLocation (LocationID, LocationBK, Name, CostRate, Availability, ModifiedDate, CreatedDate)
            VALUES %s
        """
        execute_values(cursor_dwh, insert_query, data)
        conn_dwh.commit()
        cursor_dwh.close()
        conn_dwh.close()
        logging.info("DimLocation cargado con éxito.")
    except Exception as e:
        logging.error(f"Error en extract_load_locations: {e}")

# Extraer y cargar datos en DimDate con logging
def extract_load_dates():
    logging.info("Iniciando carga de DimDate...")
    try:
        conn_dwh = connect_db(DB_DWH)
        cursor_dwh = conn_dwh.cursor()
        cursor_dwh.execute("""
            INSERT INTO adventure_dwh.DimDate (DateKey, FullDate, Year, Quarter, Month, Day, WeekdayName, IsWeekend)
            SELECT TO_CHAR(d, 'YYYYMMDD')::INTEGER, d, EXTRACT(YEAR FROM d), EXTRACT(QUARTER FROM d),
                   EXTRACT(MONTH FROM d), EXTRACT(DAY FROM d), TO_CHAR(d, 'Day'),
                   CASE WHEN EXTRACT(ISODOW FROM d) IN (6,7) THEN TRUE ELSE FALSE END
            FROM GENERATE_SERIES('2010-01-01'::DATE, '2015-01-01'::DATE, '1 day'::INTERVAL) d
        """)
        conn_dwh.commit()
        cursor_dwh.close()
        conn_dwh.close()
        logging.info("DimDate cargado con éxito.")
    except Exception as e:
        logging.error(f"Error en extract_load_dates: {e}")

# Extraer y cargar datos en FactPurchases con logging
def extract_load_fact_purchases():
    logging.info("Iniciando carga de FactPurchases...")
    try:
        conn_erp = connect_db(DB_ERP)
        cursor_erp = conn_erp.cursor()
        cursor_erp.execute("""
            SELECT poh.PurchaseOrderID, pod.PurchaseOrderDetailID, 
                   poh.PurchaseOrderID || '|' || pod.PurchaseOrderDetailID AS PurchaseBK,
                   poh.VendorID, pod.ProductID, poh.EmployeeID, poh.ShipMethodID,
                   TO_CHAR(poh.OrderDate, 'YYYYMMDD')::INTEGER AS PurchaseDateKey,
                   pod.OrderQty, pod.UnitPrice, (pod.OrderQty * pod.UnitPrice) AS TotalCost,
                   poh.ModifiedDate, CURRENT_TIMESTAMP AS CreatedDate
            FROM Purchasing.PurchaseOrderHeader poh
            LEFT JOIN Purchasing.PurchaseOrderDetail pod ON poh.PurchaseOrderID = pod.PurchaseOrderID
        """)
        
        data_erp = cursor_erp.fetchall()
        cursor_erp.close()
        conn_erp.close()

        if not data_erp:
            logging.warning("No se encontraron datos para FactPurchases.")

        conn_dwh = connect_db(DB_DWH)
        cursor_dwh = conn_dwh.cursor()

        for row in data_erp:
            purchase_order_id, purchase_order_detail_id, purchase_bk, vendor_id, product_id, employee_id, ship_method_id, \
            purchase_date_key, quantity, unit_cost, total_cost, modified_date, created_date = row

            cursor_dwh.execute("""
                INSERT INTO adventure_dwh.FactPurchases (PurchaseOrderID, PurchaseOrderDetailID, PurchaseBK, VendorKey, ProductKey,
                                                         EmployeeKey, ShipMethodKey, PurchaseDateKey, Quantity, UnitCost, 
                                                         TotalCost, ModifiedDate, CreatedDate)
                SELECT %s, %s, %s,
                       dv.VendorKey, dp.ProductKey, de.EmployeeKey, dsm.ShipMethodKey,
                       %s, %s, %s, %s, %s, %s
                FROM adventure_dwh.DimVendor dv
                LEFT JOIN adventure_dwh.DimProduct dp ON dp.ProductID = %s
                LEFT JOIN adventure_dwh.DimEmployee de ON de.EmployeeID = %s
                LEFT JOIN adventure_dwh.DimShipMethod dsm ON dsm.ShipMethodID = %s
                WHERE dv.VendorID = %s
            """, (purchase_order_id, purchase_order_detail_id, purchase_bk, 
                  purchase_date_key, quantity, unit_cost, total_cost, modified_date, created_date,
                  product_id, employee_id, ship_method_id, vendor_id))

        conn_dwh.commit()
        cursor_dwh.close()
        conn_dwh.close()
        logging.info("FactPurchases cargada con éxito.")
    except Exception as e:
        logging.error(f"Error en extract_load_fact_purchases: {e}")


# Extraer y cargar datos en FactInventory con logging
def extract_load_fact_inventory():
    logging.info("Iniciando carga de FactInventory...")
    try:
        # Conectar a la base de datos de origen (ERP)
        conn_erp = connect_db(DB_ERP)
        cursor_erp = conn_erp.cursor()

        # Extraer datos de Production.ProductInventory en adventure_erp sin JOIN con adventure_dwh
        cursor_erp.execute("""
            SELECT pi.LocationID, pi.ProductID,
                   pi.LocationID || '|' || pi.ProductID AS InventoryBK,
                   pi.Quantity AS StockLevel,
                   TO_CHAR(DATE '2013-01-01', 'YYYYMMDD')::INTEGER AS LastUpdatedDateKey,
                   pi.ModifiedDate, CURRENT_TIMESTAMP AS CreatedDate
            FROM Production.ProductInventory pi
        """)
        
        data_erp = cursor_erp.fetchall()
        cursor_erp.close()
        conn_erp.close()

        if not data_erp:
            logging.warning("No se encontraron datos para FactInventory.")

        # Conectar a la base de datos de destino (DWH)
        conn_dwh = connect_db(DB_DWH)
        cursor_dwh = conn_dwh.cursor()

        # Insertar datos en FactInventory con LEFT JOIN en adventure_dwh
        for row in data_erp:
            location_id, product_id, inventory_bk, stock_level, last_updated_date_key, \
            modified_date, created_date = row

            cursor_dwh.execute("""
                INSERT INTO adventure_dwh.FactInventory (InventoryBK, LocationKey, ProductKey, Warehouse, StockLevel, 
                                                         UnitCost, TotalValue, LastUpdatedDateKey, ModifiedDate, CreatedDate)
                SELECT %s, l.LocationKey, p.ProductKey, l.Name, %s, p.StandardCost, p.StandardCost*%s ,%s, %s, %s
                FROM adventure_dwh.DimLocation l
                LEFT JOIN adventure_dwh.DimProduct p ON p.ProductID = %s
                WHERE l.LocationID = %s
            """, (inventory_bk, stock_level, stock_level, last_updated_date_key, modified_date, created_date,
                  product_id, location_id))

        conn_dwh.commit()
        cursor_dwh.close()
        conn_dwh.close()
        logging.info("FactInventory cargada con éxito.")
    except Exception as e:
        logging.error(f"Error en extract_load_fact_inventory: {e}")

def check_bi_loaded():
    conn_dwh = connect_db(DB_DWH)
    with conn_dwh.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS etl_ready (ok BOOLEAN);")
        cur.execute("INSERT INTO etl_ready VALUES (TRUE);")
    conn_dwh.commit()
    conn_dwh.close()
    logging.info("BI cargado con éxito.")


def main():
    logging.info("--------------INICIANDO PROCESO ETL...--------------")
    wait_for_postgres(DB_ERP)
    wait_for_postgres(DB_DWH)
    extract_load_customers()
    extract_load_products()
    extract_load_sales_territory()
    extract_load_ship_methods()
    extract_load_dates()
    extract_load_fact_sales()
    extract_load_employees()
    extract_load_vendors()
    extract_load_locations()
    extract_load_fact_purchases()
    extract_load_fact_inventory()
    logging.info("--------------PROCESO ETL FINALIZADO.--------------")
    check_bi_loaded()

if __name__ == "__main__":
   main()