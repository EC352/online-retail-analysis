import pandas as pd

def clean_data (file_path):
    ###This first part is to clean the data (from what was found in the SQL data quality checks), the original data remains in online_retail
    online_retail = pd.read_csv(file_path, sep = ";", encoding = "latin1") #dataset has sterlin sign: latin encoding

    online_retail_clean = online_retail[~online_retail["InvoiceNo"].astype(str).str.startswith ("A")] #delete all invoice No starting with A

    online_retail_clean = online_retail_clean[~online_retail_clean["StockCode"].astype(str).str.match(r"^[A-Za-z]+$")]

    online_retail_clean = online_retail_clean [~online_retail_clean["Description"].isna() & 
                                            ~online_retail_clean["Description"].astype(str).str.contains(r"NaN|\?", case = False, na = False) &
                                            online_retail_clean["Description"].astype(str).str.upper()] #Delte all description that are NaN, ?, or lower case

    online_retail_clean["Quantity"] = pd.to_numeric(online_retail_clean["Quantity"], errors="coerce")
   
    online_retail_clean["InvoiceDate"] = pd.to_datetime(online_retail_clean["InvoiceDate"], format="mixed") #Transform date into proper format

    online_retail_clean["UnitPrice"] = pd.to_numeric(online_retail_clean["UnitPrice"].str.replace(",", ".", regex=False), errors="coerce") 
    online_retail_clean = online_retail_clean[~online_retail_clean["UnitPrice"].isna()] #Remove NaNs of UnitPrice

    online_retail_clean = online_retail_clean[~online_retail_clean["CustomerID"].isna()] #Remove NaNs of CustomerID

    return online_retail_clean

