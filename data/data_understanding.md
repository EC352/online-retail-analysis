# Number Rows
541909

# Variables, meaning, unit (data dictionary)
1. **InvoiceNo**: a 6-digit integral number uniquely assigned to each transaction. If this code starts with letter 'c', it indicates a cancellation, varchar
2. **StockCode**: a 5-digit integral number uniquely assigned to each distinct product, varchar
3. **Description**: product name, varchar
4. **Quantity**: quantity of each item per transaction, int64
5. **InvoiceDate**: the day and time when each transaction was generated, varchar
6. **UnitPrice**: product price per unit, in sterling, varchar
7. **CustomerID**: a 5-digit integral number uniquely assigned to each customer, int64
8. **Country**: the name of the country where each customer resides, varchar

# What constitutes a transaction?  
An InvoiceNo without a c

# What constitutes a product?  
When description is not NULL

# What constitutes a customer?  
When CustomerID is not NULL

# What does a cancellation look like?  
An InvoiceNo starting with a c

# What are the time boundaries?  
DD/MM/YYYY HH:MM; between 01/12/2010 and 09/12/2011

# How many countries are represented? 
38

# Missing values?
The website said None, but I find quite some weird values and NaNs in pandas

I went through the columns very carefully
1. InvoiceNo columns should have 6 digits. When it starts with C --> cancellation (remove). I found some starting with A as well (Adjust bad debt) (remove)
2. StockCode should be integers, has letters too:
    [] P: POST - Postage - delete
    [] D: DOT - Dotcom postage - delete
    [] M: M - Manual - delete
    [] C: C2 - Carriage - delete
    [] S: S - Samples - delete
    [] B: Bank charges - bank charges - delete
    [] A: Amazon fee - Amazon fee - delete
    [] g: giftcode - gift voucher - keep
    [] m: m - Manual - delete
3. Description: keep all
    Found a few NaN and ? when going through Quantity
    Deleted everything containing NaN or ?
4. Quantity: delete all negatives (impossible)
    Huge max (80995) --> they are normal products (except one, but customer ID = NaN)
5. InvoiceDate should be between 01/12/2010 and 09/12/2011 -- Removed all outside that date
6. Unitprice is a float and nothing else
7. CustomerID should not be NaN

# Distributions quantity, price, transactions/customer, transactions/day  
Quantity: strong right skew (mean (13.14) > median (6), max of 80995)
UnitPrice: strong right skew (mean (2.86) > median (1.85), max of 649.5)
Transactions/customer: right skew again (mean: 4.10, median: 2), max of 185 (customer 14911)
Transactions/day: normal distribution (mean: 1.07, median: 1), max of 4 (at 26-05-2011)



