-- Crear esquema si no existe
CREATE SCHEMA IF NOT EXISTS adventure_dwh;

-- DimCustomer
CREATE TABLE IF NOT EXISTS adventure_dwh.DimCustomer (
    CustomerKey SERIAL PRIMARY KEY,
    CustomerID INT,
    CustomerBK INT,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    FullName VARCHAR(100),
    EmailAddress VARCHAR(100),
    Phone VARCHAR(25),
    ModifiedDate DATE,
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DimProduct
CREATE TABLE IF NOT EXISTS adventure_dwh.DimProduct (
    ProductKey SERIAL PRIMARY KEY,
    ProductBK INT NOT NULL,
    ProductID INT NOT NULL,
    Name VARCHAR(100),
    ProductNumber VARCHAR(50),
    Color VARCHAR(20),
    StandardCost DECIMAL(18,2),
    ListPrice DECIMAL(18,2),
    Size VARCHAR(10),
    Weight DECIMAL(10,2),
    ProductCategory VARCHAR(50),
    ProductSubcategory VARCHAR(50),
    ModifiedDate DATE,
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DimSalesTerritory
CREATE TABLE IF NOT EXISTS adventure_dwh.DimSalesTerritory (
    SalesTerritoryKey SERIAL PRIMARY KEY,
    SalesTerritoryBK INT,
    SalesTerritoryID INT,
    Name VARCHAR(50),
    CountryRegionCode VARCHAR(5),
    RegionGroup VARCHAR(20),
    ModifiedDate DATE,
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DimEmployee
CREATE TABLE IF NOT EXISTS adventure_dwh.DimEmployee (
    EmployeeKey SERIAL PRIMARY KEY,
    EmployeeID INT NOT NULL,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    FullName VARCHAR(100),
    JobTitle VARCHAR(50),
    HireDate DATE,
    BirthDate DATE,
    EmailAddress VARCHAR(100),
    Phone VARCHAR(25),
    ModifiedDate DATE,
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DimVendor
CREATE TABLE IF NOT EXISTS adventure_dwh.DimVendor (
    VendorKey SERIAL PRIMARY KEY,
    VendorBK INT NOT NULL,
    VendorID INT NOT NULL,
    Name VARCHAR(100),
    AccountNumber VARCHAR(50),
    Phone VARCHAR(25),
    EmailAddress VARCHAR(100),
    ModifiedDate DATE,
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DimShipMethod
CREATE TABLE IF NOT EXISTS adventure_dwh.DimShipMethod (
    ShipMethodKey SERIAL PRIMARY KEY,
    ShipMethodBK INT,
    ShipMethodID INT NOT NULL,
    Name VARCHAR(50),
    ShipBase DECIMAL(10,2),
    ShipRate DECIMAL(10,2),
    ModifiedDate DATE,
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DimLocation
CREATE TABLE IF NOT EXISTS adventure_dwh.DimLocation (
    LocationKey SERIAL PRIMARY KEY,
    LocationID INT,
    LocationBK INT,
    Name VARCHAR(100),
    CostRate DECIMAL(10,2),
    Availability DECIMAL(10,2),
    ModifiedDate DATE,
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DimDate
CREATE TABLE IF NOT EXISTS adventure_dwh.DimDate (
    DateKey INT PRIMARY KEY,
    FullDate DATE,
    Year INT,
    Quarter INT,
    Month INT,
    Day INT,
    WeekdayName VARCHAR(20),
    IsWeekend BOOLEAN
);

-- FactSales
CREATE TABLE IF NOT EXISTS adventure_dwh.FactSales (
    SalesKey SERIAL PRIMARY KEY,
    SalesOrderID INT,
    SalesOrderDetailID INT,
    SalesBK VARCHAR(50),
    CustomerKey INT REFERENCES adventure_dwh.DimCustomer(CustomerKey),
    ProductKey INT REFERENCES adventure_dwh.DimProduct(ProductKey),
    ShipMethodKey INT REFERENCES adventure_dwh.DimShipMethod(ShipMethodKey),
    OrderDateKey INT REFERENCES adventure_dwh.DimDate(DateKey),
    SalesTerritoryKey INT REFERENCES adventure_dwh.DimSalesTerritory(SalesTerritoryKey),
    SalesAmount DECIMAL(18,2),
    Quantity INT,
    Discount DECIMAL(18,2),
    UnitPrice DECIMAL(18,2),
    TotalSale DECIMAL(18,2),
    ModifiedDate DATE,
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- FactPurchases
CREATE TABLE IF NOT EXISTS adventure_dwh.FactPurchases (
    PurchaseKey SERIAL PRIMARY KEY,
    PurchaseOrderID INT,
    PurchaseOrderDetailID INT,
    PurchaseBK VARCHAR(50),
    VendorKey INT REFERENCES adventure_dwh.DimVendor(VendorKey),
    ProductKey INT REFERENCES adventure_dwh.DimProduct(ProductKey),
    EmployeeKey INT REFERENCES adventure_dwh.DimEmployee(EmployeeKey),
    ShipMethodKey INT REFERENCES adventure_dwh.DimShipMethod(ShipMethodKey),
    PurchaseDateKey INT REFERENCES adventure_dwh.DimDate(DateKey),
    Quantity INT,
    UnitCost DECIMAL(18,2),
    TotalCost DECIMAL(18,2),
    ModifiedDate DATE,
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- FactInventory
CREATE TABLE IF NOT EXISTS adventure_dwh.FactInventory (
    InventoryKey SERIAL PRIMARY KEY,
    InventoryBK VARCHAR(50),
    LocationKey INT REFERENCES adventure_dwh.DimLocation(LocationKey),
    ProductKey INT REFERENCES adventure_dwh.DimProduct(ProductKey),
    Warehouse VARCHAR(50),
    StockLevel INT,
    UnitCost DECIMAL(18,2),
    TotalValue DECIMAL(18,2),
    LastUpdatedDateKey INT REFERENCES adventure_dwh.DimDate(DateKey),
    ModifiedDate DATE,
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
