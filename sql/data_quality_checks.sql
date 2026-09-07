--General information
SELECT COUNT(*) FROM "online_retail";
DESC "online_retail";
SELECT * FROM "online_retail" LIMIT 2;


--InvoiceNo has no letters except c. InvoiceNos A563185, A563186, A563187 is Adjust bad debt 
SELECT DISTINCT * FROM "online_retail"
WHERE regexp_matches ("InvoiceNo", '[A-BD-Za-bd-z]') OR "InvoiceNo" IS NULL;
--InvoiceNumbers contain C (cancellation) and A (bad debt)

--StockCode column has no letters
SELECT * FROM "online_retail"
WHERE regexp_matches ("StockCode", '[^0-9]') OR "StockCode" IS NULL; -- Letters are allowed; descriptions not in all caps are not products

--Descriptions are text (not NaN or ?) I learned that most actual product descriptions are capitalized 
SELECT * FROM "online_retail"
WHERE "Description" <> UPPER("Description") OR "Description" IS NULL OR "Description" LIKE '?%';

--Quantity is an integer > 0
SELECT * FROM "online_retail" 
WHERE "Quantity" <= 0 OR "Quantity" IS NULL;

--Date is between 2010-12-01 and 2011-12-09
SELECT * FROM "online_retail"
WHERE "InvoiceDate" NOT BETWEEN '2010-12-01' AND '2011-12-10'; --All are in between these

