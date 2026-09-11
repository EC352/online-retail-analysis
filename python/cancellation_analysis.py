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
product_invoice = online_retail_clean.groupby(["StockCode", "InvoiceNo"], as_index=False).agg(cancelled = ("cancelled", "max"), description = ("Description", "first"), Invoicedate = ("InvoiceDate", "first"))
products_cancelled = product_invoice.groupby("StockCode").agg(cancelled=("cancelled", "sum"), total_transactions=("InvoiceNo", "nunique"), description=("description", "first"))

products_cancelled["cancellation_rate"] = products_cancelled["cancelled"] / products_cancelled["total_transactions"] * 100
products_cancelled["cancellation_share"] = products_cancelled["cancelled"] / products_cancelled["cancelled"].sum() * 100

products_cancelled = products_cancelled.sort_values("cancelled", ascending=False)

print (f"Most frequently cancelled products:\n {products_cancelled [["cancelled", "description", "total_transactions", "cancellation_rate", "cancellation_share"]].head(10)}")

product_invoice["month"] = product_invoice["Invoicedate"].dt.to_period("M")

monthly_product = product_invoice.groupby(["month", "StockCode"], as_index=False).agg(cancelled=("cancelled", "sum"), total_transactions=("InvoiceNo", "nunique"), description=("description", "first"))
monthly_product["cancellation_rate"] = monthly_product["cancelled"] / monthly_product["total_transactions"] * 100

high_cancellation_months = ["2010-09", "2010-12", "2011-01", "2011-11"]

high_month_products = monthly_product[monthly_product["month"].astype(str).isin(high_cancellation_months)].sort_values(["month", "cancelled"], ascending=[True, False]).groupby("month").head(5)

print(high_month_products)

#Cancellation rate (%) per month
month_invoice = online_retail_clean.groupby(["InvoiceNo", online_retail_clean["InvoiceDate"].dt.to_period("M")], as_index=False).agg(cancelled = ("cancelled", "max"))
cancellation_month = month_invoice.groupby("InvoiceDate", as_index=False).agg(cancelled=("cancelled", "sum"), total_transactions=("InvoiceNo", "nunique"))

cancellation_month["cancellation_rate"] = cancellation_month["cancelled"] / cancellation_month ["total_transactions"] * 100

print (f"Cancellation rate/month:\n {cancellation_month.sort_values("cancelled", ascending=False)}")

plt.plot (cancellation_month["InvoiceDate"].astype(str), cancellation_month["cancellation_rate"], color = "black", linewidth = 2.2, marker = "o", markersize = 4)
plt.xlabel ("Month", fontsize = 12)
plt.ylabel ("cancellation rate (%)", fontsize = 12)
plt.title ("cancellation rate per month", fontsize = 15, fontweight = "bold") #pad = 15
plt.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.4)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

#Cancellation rate per country
invoice_level = (online_retail_clean.groupby(["Country", "InvoiceNo"], as_index=False).agg(cancelled=("cancelled", "max")))

cancellation_country = (invoice_level.groupby("Country", as_index=False).agg(cancelled=("cancelled", "sum"), total_invoices=("InvoiceNo", "nunique")))

cancellation_country["cancellation_rate"] = (cancellation_country["cancelled"] / cancellation_country["total_invoices"] * 100)
cancellation_country["cancellation_share"] = cancellation_country["cancelled"] / cancellation_country["cancelled"].sum() * 100

cancellation_country = cancellation_country.sort_values("cancelled", ascending=False)

print (f"Cancellation rate/country:\n {cancellation_country}")

plt.bar (cancellation_country["Country"].astype(str), cancellation_country["cancellation_rate"], width=0.5, color="skyblue")
plt.xlabel ("Country", fontsize = 12)
plt.ylabel ("cancellation rate (%)", fontsize = 12)
plt.title ("cancellation rate per country", fontsize = 15, fontweight = "bold") #pad = 15
plt.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.4)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()