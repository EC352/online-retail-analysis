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

#I found that there is an increase of 683% between Oct 2010 & Dec 2010
october = online_retail_clean[(online_retail_clean["InvoiceDate"].dt.year == 2010) & 
                              (online_retail_clean["InvoiceDate"].dt.month == 10)]
december = online_retail_clean[(online_retail_clean["InvoiceDate"].dt.year == 2010) & 
                              (online_retail_clean["InvoiceDate"].dt.month == 12)]

october_orders = october.groupby("InvoiceNo")["revenue"].sum().sort_values(ascending=False)
december_orders = december.groupby("InvoiceNo")["revenue"].sum().sort_values(ascending=False)

print (f"Highest revenue orders in october:\n {october_orders.head(10)}")
print (f"Highest revenue orders in december:\n {december_orders.head(10)}")

largest_order_oct = october_orders.iloc[0]
largest_order_oct_share = (largest_order_oct / october["revenue"].sum()) * 100

largest_order_dec = december_orders.iloc[0]
largest_order_dec_share = (largest_order_dec / december["revenue"].sum()) * 100

print (f"October largest order share: {largest_order_oct_share}%\n vs December: {largest_order_dec_share}%")

print (f"October:\n Orders: {len(october_orders)}\n Revenue: {october_orders.sum()}\n Average_order: {october_orders.mean()}\n Median_order: {october_orders.median()}")
print (f"December:\n Orders: {len(december_orders)}\n Revenue: {december_orders.sum()}\n Average_order: {december_orders.mean()}\n Median_order: {december_orders.median()}")

#Examining the september 2011 peak:
august = online_retail_clean[(online_retail_clean["InvoiceDate"].dt.year == 2011) & 
                              (online_retail_clean["InvoiceDate"].dt.month == 8)]
september = online_retail_clean[(online_retail_clean["InvoiceDate"].dt.year == 2011) & 
                              (online_retail_clean["InvoiceDate"].dt.month == 9)]

august_orders = august.groupby("InvoiceNo")["revenue"].sum().sort_values(ascending=False)
september_orders = september.groupby("InvoiceNo")["revenue"].sum().sort_values(ascending=False)

print (f"Highest revenue orders in august 2011:\n {august_orders.head(10)}")
print (f"Highest revenue orders in september 2011:\n {september_orders.head(10)}")

largest_order_aug = august_orders.iloc[0]
largest_order_aug_share = (largest_order_aug / august["revenue"].sum()) * 100

largest_order_sep = september_orders.iloc[0]
largest_order_sep_share = (largest_order_sep / september["revenue"].sum()) * 100

print (f"August largest order share: {largest_order_aug_share}%\n vs September: {largest_order_sep_share}%")

print (f"August:\n Orders: {len(august_orders)}\n Revenue: {august_orders.sum()}\n Average_order: {august_orders.mean()}\n Median_order: {august_orders.median()}")
print (f"September:\n Orders: {len(september_orders)}\n Revenue: {september_orders.sum()}\n Average_order: {september_orders.mean()}\n Median_order: {september_orders.median()}")

largest_sep_invoice = september_orders.index[0]
large_order_sep = september[september["InvoiceNo"] == largest_sep_invoice]

print (large_order_sep[["InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice", "Country", "revenue"]])

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

october["FirstPurchaseMonth"] = october["CustomerID"].map(first_purchase)
october["CustomerType"] = october["InvoiceDate"].dt.to_period("M") == october["FirstPurchaseMonth"]

oct_orders = october["InvoiceNo"].nunique()
oct_revenue = october["revenue"].sum()
october_new_orders = october[october["CustomerType"] == True]["InvoiceNo"].nunique()
october_new_revenue = october[october["CustomerType"] == True]["revenue"].sum()

print (f"October new orders share: {october_new_orders / oct_orders * 100}")
print (f"October new revenue share: {october_new_revenue / oct_revenue * 100}")

december["FirstPurchaseMonth"] = december["CustomerID"].map(first_purchase)
december["CustomerType"] = december["InvoiceDate"].dt.to_period("M") == december["FirstPurchaseMonth"]

dec_orders = december["InvoiceNo"].nunique()
dec_revenue = december["revenue"].sum()
december_new_orders = december[december["CustomerType"] == True]["InvoiceNo"].nunique()
december_new_revenue = december[december["CustomerType"] == True]["revenue"].sum()

print (f"December new orders share: {december_new_orders / dec_orders * 100}")
print (f"December new revenue share: {december_new_revenue / dec_revenue * 100}")




