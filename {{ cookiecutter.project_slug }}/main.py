# Simplifies the execution of one or more of the src scripts
# For instace, here we are reading different types of source data

from utils import Load_data

load = Load_data()

# Read excel in raw folder within data folder
data_excel = Load_data().from_excel(type='raw', name_file='dummy_data.xlsx')

# Read csv in raw folder within data folder
data_csv = load.from_csv(type="processed", name_file="dummy_processed.csv")

# Read data from GCP BigQuery service
query_test = """ 
SELECT * 
FROM `dolphin-prod.bi_visualization.metas_producto`
"""
data_bq = load.from_BigQuery(query=query_test, name_file="credentials_bq.json")

print('\n'+'-'*10+' Data from excel '+'-'*10)
print(data_excel.head())
print('\n'+'-'*10+' Data from csv '+'-'*10)
print(data_csv.head())
print('\n'+'-'*10+' Data from BigQuery '+'-'*10)
print(data_bq.head())