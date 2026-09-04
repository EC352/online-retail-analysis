import pandas as pd
import matplotlib.pyplot as plt
from data_cleaning import clean_data

#Gather clean data, and delete cancellations
online_retail_clean = clean_data ("data/Online-Retail.csv")
online_retail_clean = online_retail_clean[~online_retail_clean["InvoiceNo"].astype(str).str.startswith ("C")] #delete all invoice No starting with C (cancellations)
online_retail_clean = online_retail_clean [ online_retail_clean ["Quantity"] > 0] #Only keep quantites > 0

###Check distributions of quantity, price 
print (f"Description Quantity\n {online_retail_clean["Quantity"].describe()}")

plt.hist(online_retail_clean.loc[online_retail_clean["Quantity"] <= 50, "Quantity"], bins=20)
plt.xlabel ("Quantity")
plt.ylabel ("Number of Invoices")
plt.title ("Distribution of Quantity")
plt.show ()

print (f"Description Price\n {online_retail_clean["UnitPrice"].describe()}")

plt.hist(online_retail_clean.loc[online_retail_clean["UnitPrice"] <= 20, "Quantity"], bins=20)
plt.xlabel ("UnitPrice")
plt.ylabel ("Number of Invoices")
plt.title ("Distribution of Price")
plt.show ()

###Revenue Analysis
"""Answers:
Which products generate the most revenue? 
Are these products also the most frequently purchased products?
Which countries generate the most revenue? 
How has revenue changed over time? """

#Which products generate the most revenue
online_retail_clean["revenue"] = online_retail_clean["Quantity"] * online_retail_clean["UnitPrice"]
revenue_product = online_retail_clean.groupby("StockCode").agg(revenue = ("revenue", "sum"), description = ("Description", "first")).sort_values("revenue", ascending=False)

print (f"Highest revenue products:\n {revenue_product.head(10)}")

#Which products are purchased most frequently
purchases_product = online_retail_clean.groupby("StockCode").agg(purchased = ("InvoiceNo", "sum"), description = ("Description", "first")).sort_values("purchased", ascending=False)

print (f"Most frequently purchased products:\n {purchases_product.head(10)}")

#Which countries generate the most revenue
revenue_country = online_retail_clean.groupby("Country")["revenue"].sum()

print (f"Highest revenue countries:\n {revenue_country.nlargest(10)}")

#How does the revenue change per month
revenue_month = online_retail_clean.groupby(online_retail_clean["InvoiceDate"].dt.to_period("M"), as_index = False)["revenue"].sum()

print (f"Revenue distribution per month:\n {revenue_month}")

plt.plot (revenue_month["InvoiceDate"].astype(str), revenue_month["revenue"], color = "black",linewidth = 2.2, marker = "o", markersize = 4)
plt.xlabel ("Month", fontsize = 12)
plt.ylabel ("revenue (in millions)", fontsize = 12)
plt.title ("revenue per month", fontsize = 15, fontweight = "bold") #pad = 15
plt.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.4)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


