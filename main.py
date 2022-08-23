from src import Load_data

load = Load_data()
data_excel = load.from_excel(
    type="raw", name_file="dummy_data.xlsx", sheet_name="Hoja2"
)
data_csv = load.from_csv(type="processed", name_file="dummy_prosc_data.csv")

query_test = """ 
SELECT * 
FROM `dolphin-prod.bi_visualization.metas_producto`
"""
data_bq = load.from_BigQuery(query=query_test, name_file="credentials_bq.json")

print(data_excel.head())
print(data_csv.head())
print(data_bq.head())
