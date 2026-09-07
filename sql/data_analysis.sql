--Customer summary


--Number of unique customers
SELECT COUNT ("ID") FROM "customers";

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

--Each customer's first purchase
WITH "first_invoice" AS (
    SELECT "InvoiceNo", "InvoiceDate", "CustomerID", 
    ROW_NUMBER () OVER (PARTITION BY "CustomerID" ORDER BY "InvoiceDate", "InvoiceNo") AS "rn"
    FROM "invoices"
    WHERE "InvoiceNo" NOT LIKE 'A%' AND "InvoiceNo" NOT LIKE 'C%' 
    AND "CustomerID" IS NOT NULL
)

SELECT fi."CustomerID", fi."InvoiceNo", fi."InvoiceDate", 
ii."Code", p."Description", ii."Quantity" FROM "first_invoice" AS fi
JOIN "invoice_items" ii ON fi."InvoiceNo" = ii."InvoiceNumber"
JOIN "products" p ON ii."Code" = p."StockCode"
WHERE fi."rn" = 1 
AND "Quantity" > 0 AND "Quantity" IS NOT NULL
AND "Description" = UPPER("Description") AND "Description" IS NOT NULL AND "Description" NOT LIKE '?%'
ORDER BY fi."CustomerID";


--Product summary


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

--The top 10 products within each country (most sold)
SELECT "Country", "Description",
COUNT("InvoiceNo") AS "number_of_invoices" FROM "invoices" AS i
JOIN "invoice_items" ii ON i."InvoiceNo" = ii."InvoiceNumber"
JOIN "products" p ON ii."Code" = p."StockCode"
WHERE "InvoiceNo" NOT LIKE 'A%' AND "InvoiceNumber" NOT LIKE 'C%'
AND "Description" = UPPER("Description") AND "Description" IS NOT NULL AND "Description" NOT LIKE '?%'
AND "Country" IS NOT NULL
GROUP BY "Country", "Description"
ORDER BY COUNT("InvoiceNo") DESC;


--Invoice and monthly summary


--Total per invoice 
SELECT "InvoiceNumber", "Description",
SUM("Quantity" * "UnitPrice") AS "invoice_total_price" FROM "invoice_items" AS ii
JOIN "products" p ON ii."Code" = p."StockCode"
WHERE "InvoiceNumber" NOT LIKE 'A%' AND "InvoiceNumber" NOT LIKE 'C%'
AND "Quantity" > 0 AND "Quantity" IS NOT NULL
AND "Description" = UPPER("Description") AND "Description" IS NOT NULL AND "Description" NOT LIKE '?%'
GROUP BY "InvoiceNumber", "Description"
ORDER BY SUM("Quantity" * "UnitPrice") DESC
LIMIT 10;

--How many transaction occur each month
SELECT YEAR ("InvoiceDate") AS 'year', MONTH ("InvoiceDate") AS 'month', 
COUNT ("InvoiceNo") as 'number_of_invoices' FROM "invoices"
WHERE "InvoiceNo" NOT LIKE 'A%' AND "InvoiceNo" NOT LIKE 'C%'
GROUP BY YEAR ("InvoiceDate"), MONTH ("InvoiceDate");

--Monthly revenue comparison to the previous month
WITH "monthly_revenue" AS (
    SELECT DATE_TRUNC ('month', i."InvoiceDate") AS "month",
    SUM (ii."Quantity" * ii."UnitPrice") AS "revenue"
    FROM "invoices" i
    JOIN "invoice_items" ii ON i."InvoiceNo" = ii."InvoiceNumber"
    WHERE "Quantity" > 0 AND "Quantity" IS NOT NULL
    GROUP BY DATE_TRUNC ('month', i."InvoiceDate")
)

SELECT
    "month",
    "revenue",
    LAG("revenue") OVER (
        ORDER BY "month"
    ) AS "previous_month_revenue",
    "revenue" - LAG("revenue") OVER (
        ORDER BY "month"
    ) AS "revenue_change",
    ROUND(
        100.0 * (
            "revenue" - LAG("revenue") OVER (ORDER BY "month")
        ) / NULLIF(LAG("revenue") OVER (ORDER BY "month"), 0),
        2
    ) AS "revenue_change_percent"
FROM "monthly_revenue"
ORDER BY "month";


--Country summary 
 

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