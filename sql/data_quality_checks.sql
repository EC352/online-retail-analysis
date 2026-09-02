--InvoiceNo has no letters except c. InvoiceNos A563185, A563186, A563187 is Adjust bad debt 
SELECT DISTINCT * FROM "invoice_items"
WHERE regexp_matches ("InvoiceNumber", '[A-BD-Za-bd-z]') OR "InvoiceNumber" IS NULL;
--InvoiceNumbers contain C (cancellation) and A (bad debt)

--StockCode column has no letters
SELECT * FROM "products"
WHERE regexp_matches ("StockCode", '[^0-9]') OR "StockCode" IS NULL; -- Letters are allowed; descriptions not in all caps are not products

--Descriptions are text (not NaN or ?) I learned that most actual product descriptions are capitalized 
SELECT * FROM "products"
WHERE "Description" <> UPPER("Description") OR "Description" IS NULL OR "Description" LIKE '?%';

--Quantity is an integer > 0
SELECT * FROM "invoice_items" 
WHERE "Quantity" <= 0 OR "Quantity" IS NULL;

--Date is between 2010-12-01 and 2011-12-09
SELECT * FROM "invoices"
WHERE "InvoiceDate" NOT BETWEEN '2010-12-01' AND '2011-12-10'; --All are in between these

