--total per invoice 
SELECT "InvoiceNumber", "Description",
SUM("Quantity" * "UnitPrice") AS "invoice_total" FROM "invoice_items" AS ii
JOIN "products" p ON ii."Code" = p."StockCode"
WHERE "InvoiceNumber" NOT LIKE 'A%' AND "InvoiceNumber" NOT LIKE 'C%'
AND "Quantity" > 0 AND "Quantity" IS NOT NULL
AND "Description" = UPPER("Description") AND "Description" IS NOT NULL AND "Description" NOT LIKE '?%'
GROUP BY "InvoiceNumber", "Description"
ORDER BY SUM("Quantity" * "UnitPrice") DESC
LIMIT 10;

--Customers with most invoices
SELECT "CustomerID", "Country", COUNT ("InvoiceNo") FROM "invoices"
WHERE "InvoiceNo" NOT LIKE 'A%' AND "InvoiceNo" NOT LIKE 'C%'
AND "CustomerID" IS NOT NULL
GROUP BY "CustomerID", "Country"
ORDER BY COUNT ("InvoiceNo") DESC
LIMIT 10;
 
--Customers with highest total invoice
SELECT "CustomerID", "Description", "Country",
SUM("Quantity" * "UnitPrice") AS "invoice_total" FROM "invoice_items" AS ii
JOIN "products" p ON ii."Code" = p."StockCode"
JOIN "invoices" i ON ii."InvoiceNumber" = i."InvoiceNo"
WHERE "InvoiceNumber" NOT LIKE 'A%' AND "InvoiceNumber" NOT LIKE 'C%'
AND "Quantity" > 0 AND "Quantity" IS NOT NULL
AND "Description" = UPPER("Description") AND "Description" IS NOT NULL AND "Description" NOT LIKE '?%'
AND "CustomerID" IS NOT NULL
GROUP BY "CustomerID", "Description", "Country"
ORDER BY SUM("Quantity" * "UnitPrice") DESC
LIMIT 10;

--Most sold products
SELECT "Description", COUNT("InvoiceNumber") FROM "invoice_items" AS ii
JOIN "products" p ON ii."Code" = p."StockCode"
WHERE "InvoiceNumber" NOT LIKE 'A%' AND "InvoiceNumber" NOT LIKE 'C%'
AND "Description" = UPPER("Description") AND "Description" IS NOT NULL AND "Description" NOT LIKE '?%'
GROUP BY "Description"
ORDER BY COUNT("InvoiceNumber") DESC
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
