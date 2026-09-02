import pandas as pd
import matplotlib.pyplot as plt

online_retail = pd.read_csv("data/Online-Retail.csv", sep = ";", encoding = "latin1") #dataset has sterlin sign: latin encoding

###This first part is to clean the data (from what was found in the SQL data quality checks), the original data remains in online_retail
online_retail_clean = online_retail[~online_retail["InvoiceNo"].astype(str).str.startswith ("C")] #delete all invoice No starting with C
online_retail_clean = online_retail_clean[~online_retail_clean["InvoiceNo"].astype(str).str.startswith ("A")] #delete all invoice No starting with A

online_retail_clean = online_retail_clean [~online_retail_clean["Description"].isna() & 
                                           ~online_retail_clean["Description"].astype(str).str.contains(r"NaN|\?", case = False, na = False) &
                                           online_retail_clean["Description"].astype(str).str.upper()] #Delte all description that are NaN, ?, or lower case

online_retail_clean["Quantity"] = pd.to_numeric(online_retail_clean["Quantity"], errors="coerce")
online_retail_clean = online_retail_clean [ online_retail_clean ["Quantity"] > 0] #Only keep quantites > 0

online_retail_clean["InvoiceDate"] = pd.to_datetime(online_retail_clean["InvoiceDate"], format="mixed") #Transform date into proper format

online_retail_clean["UnitPrice"] = pd.to_numeric(online_retail_clean["UnitPrice"].str.replace(",", ".", regex=False), errors="coerce") 
online_retail_clean = online_retail_clean[~online_retail_clean["UnitPrice"].isna()] #Remove NaNs of UnitPrice

online_retail_clean = online_retail_clean[~online_retail_clean["CustomerID"].isna()] #Remove NaNs of CustomerID


###Check distributions quantity, price, transactions/customer, transactions/day  
print (f"Description Quantity\n {online_retail_clean["Quantity"].describe()}")
print (f"Description Price\n {online_retail_clean["UnitPrice"].describe()}")

transactions_customer = online_retail_clean.groupby("CustomerID")["InvoiceNo"].nunique()
print (f"Description transactions/customer\n {transactions_customer.describe()}")
print(f"Customers with most transactions\n {transactions_customer.nlargest(10)}")

transactions_day= online_retail_clean.groupby("InvoiceDate")["InvoiceNo"].nunique()
print (f"Description transactions per day\n {transactions_day.describe()}")
print(f"Days with most transactions\n {transactions_day.nlargest(10)}")

plt.hist(online_retail_clean.loc[online_retail_clean["Quantity"] <= 50, "Quantity"], bins=20)
plt.xlabel ("Quantity")
plt.ylabel ("Number of Invoices")
plt.title ("Distribution of Quantity")
plt.show ()

plt.hist(online_retail_clean.loc[online_retail_clean["UnitPrice"] <= 20, "Quantity"], bins=20)
plt.xlabel ("UnitPrice")
plt.ylabel ("Number of Invoices")
plt.title ("Distribution of Price")
plt.show ()

plt.hist(transactions_customer, bins = 10)
plt.xlabel ("Transactions/Customer")
plt.ylabel ("Frequency")
plt.title ("Distribution of Transactions/Customer")
plt.show ()

plt.hist(transactions_day, bins = 10)
plt.xlabel ("Transactions/Day")
plt.ylabel ("Frequency")
plt.title ("Distribution of Transactions/Day")
plt.show ()
