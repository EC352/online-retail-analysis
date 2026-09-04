import pandas as pd
import matplotlib.pyplot as plt
from data_cleaning import clean_data

###Gather clean data
online_retail_clean = clean_data ("data/Online-Retail.csv")

###Cancellation analysis
"""Answers:
What proportion of invoices are cancellations?
Cancellation rate per month
Total revenue cancelled
Products cancelled most often 
Cancellation rate per country
"""
#Cancellation rate (in %)
cancellation_rate = online_retail_clean["InvoiceNo"].astype(str).str.startswith ("C").sum() / len (online_retail_clean) * 100

print (f"Overall cancellation rate: {round(cancellation_rate, 2)} %")

#Total revenue cancelled
online_retail_clean["revenue"] = online_retail_clean["Quantity"] * online_retail_clean["UnitPrice"]  
online_retail_clean["cancelled"] = online_retail_clean["InvoiceNo"].astype(str).str.startswith("C")

revenue_cancelled = online_retail_clean.loc[online_retail_clean["cancelled"], "revenue"].sum()

print (f"Total revenue cancelled: {revenue_cancelled}")

#Most often cancelled products
products_cancelled = online_retail_clean.groupby("StockCode").agg(cancelled = ("cancelled", "sum"), description = ("Description", "first")).sort_values("cancelled", ascending=False)

print (f"Most frequently cancelled products:\n {products_cancelled.head(10)}")

#Cancellation rate (%) per month
cancellation_month = online_retail_clean.groupby(online_retail_clean["InvoiceDate"].dt.to_period("M"), as_index = False).agg(cancelled = ("cancelled", sum), total_invoices = ("InvoiceNo", "nunique"))

cancellation_month["cancellation_rate"] = cancellation_month["cancelled"] / cancellation_month ["total_invoices"] * 100

print (f"Cancellation rate/month:\n {cancellation_month}")

plt.plot (cancellation_month["InvoiceDate"].astype(str), cancellation_month["cancellation_rate"], color = "black", linewidth = 2.2, marker = "o", markersize = 4)
plt.xlabel ("Month", fontsize = 12)
plt.ylabel ("cancellation rate (%)", fontsize = 12)
plt.title ("cancellation rate per month", fontsize = 15, fontweight = "bold") #pad = 15
plt.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.4)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

#Cancellation rate per country
cancellation_country = online_retail_clean.groupby(online_retail_clean["Country"], as_index = False).agg(cancelled = ("cancelled", sum), total_invoices = ("InvoiceNo", "nunique"))

cancellation_country["cancellation_rate"] = cancellation_country["cancelled"] / cancellation_country ["total_invoices"] * 100

print (f"Cancellation rate/country:\n {cancellation_country}")

plt.bar (cancellation_country["Country"].astype(str), cancellation_country["cancellation_rate"], width=0.5, color="skyblue")
plt.xlabel ("Country", fontsize = 12)
plt.ylabel ("cancellation rate (%)", fontsize = 12)
plt.title ("cancellation rate per country", fontsize = 15, fontweight = "bold") #pad = 15
plt.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.4)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()