import pandas as pd
import matplotlib.pyplot as plt
from data_cleaning import clean_data

#Gather clean data, and delete cancellations
online_retail_clean = clean_data ("data/Online-Retail.csv")
online_retail_clean = online_retail_clean[~online_retail_clean["InvoiceNo"].astype(str).str.startswith ("C")] #delete all invoice No starting with C (cancellations)
online_retail_clean = online_retail_clean [ online_retail_clean ["Quantity"] > 0] #Only keep quantites > 0

#Transaction analysis
"""Answers:
What are the largest transactions?  
How many transactions occur each month?  
When do most transactions occur?"""

#What are the largest transcations? What products?
online_retail_clean ["revenue"] = online_retail_clean["Quantity"] * online_retail_clean["UnitPrice"]
online_retail_clean_revsorted = online_retail_clean.sort_values("revenue", ascending=False)

print (f"largest revenue transactions:\n {online_retail_clean_revsorted.head(10)}")

online_retail_clean_quansorted = online_retail_clean.sort_values("Quantity", ascending=False)

print (f"transactions with the most products:\n {online_retail_clean_quansorted.head(10)}")

#What days do most transactions occur?
transactions_day= online_retail_clean.groupby(online_retail_clean["InvoiceDate"].dt.to_period("D"))["InvoiceNo"].nunique()

print(f"Days with most transactions:\n {transactions_day.nlargest(10)}")

#How many transactions occur each month
transactions_month = online_retail_clean.groupby(online_retail_clean["InvoiceDate"].dt.to_period("M"))["InvoiceNo"].nunique()

transactions_month = transactions_month.reset_index()
transactions_month.columns = ["Month", "Transactions"]

print(f"Transactions per month:\n {transactions_month}")

plt.bar (transactions_month["Month"].astype(str), transactions_month["Transactions"], width = 0.5, color="skyblue")
plt.xlabel ("Month", fontsize = 12)
plt.ylabel ("Number of transactions", fontsize = 12)
plt.title ("Transactions per month", fontsize = 15, fontweight = "bold") #pad = 15
plt.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.4)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


