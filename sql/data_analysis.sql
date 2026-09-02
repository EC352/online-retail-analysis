--total per invoice 
SELECT "InvoiceNumber", "Description",
SUM("Quantity" * "UnitPrice") AS "invoice_total_price" FROM "invoice_items" AS ii
JOIN "products" p ON ii."Code" = p."StockCode"
WHERE "InvoiceNumber" NOT LIKE 'A%' AND "InvoiceNumber" NOT LIKE 'C%'
AND "Quantity" > 0 AND "Quantity" IS NOT NULL
AND "Description" = UPPER("Description") AND "Description" IS NOT NULL AND "Description" NOT LIKE '?%'
GROUP BY "InvoiceNumber", "Description"
ORDER BY SUM("Quantity" * "UnitPrice") DESC
LIMIT 10;

--Customers with most invoices
SELECT "CustomerID", "Country", COUNT ("InvoiceNo") AS 'number_of_invoices' FROM "invoices"
WHERE "InvoiceNo" NOT LIKE 'A%' AND "InvoiceNo" NOT LIKE 'C%'
AND "CustomerID" IS NOT NULL
GROUP BY "CustomerID", "Country"
ORDER BY COUNT ("InvoiceNo") DESC
LIMIT 10;
 
--Customers with highest total invoice
SELECT "CustomerID",
SUM("Quantity" * "UnitPrice") AS "invoice_total_price" FROM "invoice_items" AS ii
JOIN "products" p ON ii."Code" = p."StockCode"
JOIN "invoices" i ON ii."InvoiceNumber" = i."InvoiceNo"
WHERE "InvoiceNumber" NOT LIKE 'A%' AND "InvoiceNumber" NOT LIKE 'C%'
AND "Quantity" > 0 AND "Quantity" IS NOT NULL
AND "Description" = UPPER("Description") AND "Description" IS NOT NULL AND "Description" NOT LIKE '?%'
AND "CustomerID" IS NOT NULL
GROUP BY "CustomerID"
ORDER BY SUM("Quantity" * "UnitPrice") DESC
LIMIT 10;

--Most sold products
SELECT "Description", SUM("Quantity") AS 'number_times_sold' FROM "invoice_items" AS ii
JOIN "products" p ON ii."Code" = p."StockCode"
WHERE "Quantity" > 0 AND "Quantity" IS NOT NULL
AND "Description" = UPPER("Description") AND "Description" IS NOT NULL AND "Description" NOT LIKE '?%'
GROUP BY "Description"
ORDER BY SUM("Quantity") DESC
LIMIT 10;

--Products with highest revenue
SELECT "Description",
SUM("Quantity" * "UnitPrice") AS "product_revenue_total" FROM "invoice_items" AS ii
JOIN "products" p ON ii."Code" = p."StockCode"
WHERE "InvoiceNumber" NOT LIKE 'A%' AND "InvoiceNumber" NOT LIKE 'C%'
AND "Quantity" > 0 AND "Quantity" IS NOT NULL
AND "Description" = UPPER("Description") AND "Description" IS NOT NULL AND "Description" NOT LIKE '?%'
GROUP BY "Description"
ORDER BY SUM("Quantity" * "UnitPrice") DESC
LIMIT 10;

--Countries with the highest revenue
SELECT "Country",
SUM("Quantity" * "UnitPrice") AS "country_revenue_total" FROM "invoice_items" AS ii
JOIN "products" p ON ii."Code" = p."StockCode"
JOIN "invoices" i ON ii."InvoiceNumber" = i."InvoiceNo"
WHERE "InvoiceNumber" NOT LIKE 'A%' AND "InvoiceNumber" NOT LIKE 'C%'
AND "Quantity" > 0 AND "Quantity" IS NOT NULL
AND "Description" = UPPER("Description") AND "Description" IS NOT NULL AND "Description" NOT LIKE '?%'
AND "Country" IS NOT NULL
GROUP BY "Country"
ORDER BY SUM("Quantity" * "UnitPrice") DESC
LIMIT 10;

--How many transaction occur each month
SELECT YEAR ("InvoiceDate") AS 'year', MONTH ("InvoiceDate") AS 'month', 
COUNT ("InvoiceNo") as 'number_of_invoices' FROM "invoices"
WHERE "InvoiceNo" NOT LIKE 'A%' AND "InvoiceNo" NOT LIKE 'C%'
GROUP BY YEAR ("InvoiceDate"), MONTH ("InvoiceDate");

--I changed the big table in smaller analytic tables, nothing is repeated in different tables to reduce insertion/updating errors
--customers: CustomerID : customers can be added without needing an invoice etc. 
--invoices: InvoiceNo | InvoiceDate | CustomerID | Country
--products: StockCode | Description | UnitPrice : can add products without needing invoices
--invoice_items: InvoiceNo | StockCode | Quantity 
 
