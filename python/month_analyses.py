import pandas as pd
import matplotlib.pyplot as plt
from data_cleaning import clean_data

#Gather clean data, and delete cancellations
online_retail_clean = clean_data ("data/Online-Retail.csv")
online_retail_clean = online_retail_clean[~online_retail_clean["InvoiceNo"].astype(str).str.startswith ("C")] #delete all invoice No starting with C (cancellations)
online_retail_clean = online_retail_clean [ online_retail_clean ["Quantity"] > 0] #Only keep quantites > 0

#Month analyses 
"""Answers:
Best and worst months 
Monthly growth; Calculate monthly revenue and compare each month with the previous month. 
Monthly customer activity; unique customers per month; Is revenue increasing because we're getting more customers, or because existing customers are spending more?"""

#Best and worst months
online_retail_clean ["revenue"] = online_retail_clean["Quantity"] * online_retail_clean["UnitPrice"]
revenue_month = online_retail_clean.groupby(online_retail_clean["InvoiceDate"].dt.to_period("M"))["revenue"].sum()

print (f"Best month:\n {revenue_month.idxmax()} with {round(revenue_month.max(),2)}\nWorst month:\n{revenue_month.idxmin()} with {round(revenue_month.min(),2)}")

#Monthly growth (revenue month/revenue previous month)
revenue_month = revenue_month.reset_index()
revenue_month.columns = ["Month", "Revenue"]

revenue_month["monthly growth"] = revenue_month["Revenue"] / revenue_month ["Revenue"].shift(1)

print (f"Monthly growth:\n {revenue_month}")

plt.plot (revenue_month["Month"].astype(str), revenue_month["monthly growth"], color = "black",linewidth = 2.2, marker = "o", markersize = 4)
plt.xlabel ("Month", fontsize = 12)
plt.ylabel ("Monthly growth", fontsize = 12)
plt.title ("Monthly growth", fontsize = 15, fontweight = "bold", pad = 15) 
plt.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.4)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

#Monthly new customers
first_purchase = online_retail_clean.groupby("CustomerID")["InvoiceDate"].min().dt.to_period("M") #Find the first purchase date for each customer
new_customers_per_month = first_purchase.value_counts().sort_index().reset_index() 

new_customers_per_month.columns = ["Month", "NumberNewCustomers"]

print (f"Number of new customers per month:\n {new_customers_per_month}")

plt.bar (new_customers_per_month["Month"].astype(str), new_customers_per_month["NumberNewCustomers"], width = 0.5, color="skyblue")
plt.xlabel ("Month", fontsize = 12)
plt.ylabel ("Number of new customers", fontsize = 12)
plt.title ("New customers per month", fontsize = 15, fontweight = "bold") #pad = 15
plt.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.4)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()