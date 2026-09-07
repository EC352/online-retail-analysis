--I changed the big table in smaller analytic tables, nothing is repeated in different tables to reduce insertion/updating errors
--customers: CustomerID : customers can be added without needing an invoice etc. 
--invoices: InvoiceNo | InvoiceDate | CustomerID | Country
--products: StockCode | Description : can add products without needing invoices
--invoice_items: InvoiceNo | StockCode | Quantity | | UnitPrice

DROP TABLE IF EXISTS "invoice_items";
DROP TABLE IF EXISTS "invoices";
DROP TABLE IF EXISTS "products";
DROP TABLE IF EXISTS "customers";

CREATE TABLE IF NOT EXISTS "customers" (
    "ID" INTEGER PRIMARY KEY);

INSERT INTO "customers"
SELECT DISTINCT "CustomerID" FROM "online_retail"
WHERE "CustomerID" IS NOT NULL;

CREATE TABLE IF NOT EXISTS "invoices" (
    "InvoiceNo" VARCHAR (8) PRIMARY KEY,
    "InvoiceDate" DATETIME,
    "CustomerID" INTEGER,
    "Country" VARCHAR (64) ,
    FOREIGN KEY ("CustomerID") REFERENCES "customers"("ID")
);

INSERT INTO "invoices"
SELECT "InvoiceNo",
MAX (strptime("InvoiceDate", '%d/%m/%Y %H:%M')),
MAX ("CustomerID"),
MAX ("Country") FROM "online_retail"
WHERE "InvoiceNo" IS NOT NULL
GROUP BY "InvoiceNo";

CREATE TABLE IF NOT EXISTS "products" (
    "StockCode" VARCHAR (7) PRIMARY KEY,
    "Description" TEXT
);

INSERT INTO "products"
SELECT DISTINCT "StockCode", 
MAX ("Description")
FROM "online_retail"
WHERE "StockCode" IS NOT NULL
GROUP BY "StockCode";

CREATE TABLE IF NOT EXISTS "invoice_items" (
    "InvoiceItemID" INTEGER PRIMARY KEY,
    "InvoiceNumber" VARCHAR (8),
    "Code" VARCHAR (7),
    "Quantity" INTEGER,
    "UnitPrice" DECIMAL (10,2),
    FOREIGN KEY ("InvoiceNumber") REFERENCES "invoices"("InvoiceNo"),
    FOREIGN KEY ("Code") REFERENCES "products"("StockCode")
);

INSERT INTO "invoice_items" 
SELECT ROW_NUMBER () OVER () AS "InvoiceItemID", 
"InvoiceNo", "StockCode", "Quantity", 
CAST(REPLACE("UnitPrice", ',', '.') AS DECIMAL(10,2)) FROM "online_retail";




