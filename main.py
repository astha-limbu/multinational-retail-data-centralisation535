# main.py

from data_extraction import DataExtractor
from database_utils import DatabaseConnector
from data_cleaning import DataCleaning

# Initialize classes
db_connector = DatabaseConnector()
data_extractor = DataExtractor()
data_cleaning = DataCleaning()
local_db_connector = DatabaseConnector()

# List tables
tables = db_connector.list_db_tables()
print("Available tables:", tables)

# Extract user data
user_data_df = data_extractor.read_rds_table(db_connector, 'legacy_users')
print("Extracted user data from AWS RDS database: legacy_users")

# Clean user data
cleaned_user_data_df = data_cleaning.clean_user_data(user_data_df)
print("Cleaned user data")

# Upload cleaned data to the local database
local_db_creds = local_db_connector.read_local_db_creds()
local_db_connector.upload_to_db(cleaned_user_data_df, 'dim_users', creds = local_db_creds)
print("Uploaded cleaned data to dim_users table in sales_data")


# Milestone 2 TASK 4
# Extract data from PDF
pdf_path = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
card_data_df = data_extractor.retrieve_pdf_data(pdf_path)
print(f"Extracted data from PDF: {pdf_path}")

# Clean the card data
cleaned_card_data_df = data_cleaning.clean_card_data(card_data_df)
print("Cleaned card data")

# Upload the cleaned data to the database
db_connector.upload_to_db(cleaned_card_data_df, 'dim_card_details', creds = local_db_creds)
print("Uploaded cleaned data to dim_card_details table in sales_data")


# Milestone 2 - task 5
# API details 
api_key = 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'
headers = {'x-api-key': api_key}
retrieve_a_store_endpoint =  'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}'
number_of_stores_endpoint =  'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'

# Step 1: Get the Number of Stores
number_of_stores = data_extractor.list_number_of_stores(number_of_stores_endpoint, headers)
print(f"Number of stores to retrieve: {number_of_stores}")

# Step 2 & 3: Retrieve store data
stores_data_df = data_extractor.retrieve_stores_data(retrieve_a_store_endpoint, headers, number_of_stores)
print("Extracted store data")

# Step 4: Clean the store data
cleaned_store_data_df = data_cleaning.clean_store_data(stores_data_df)
print("Cleaned store data")

# Step 5: Upload cleaned data to the database
db_connector.upload_to_db(cleaned_store_data_df, 'dim_store_details', creds = local_db_creds)
print("Uploaded cleaned data to dim_store_details table")


# Milstone 2 - task 6
s3_address_csv = 's3://data-handling-public/products.csv'
local_file_path_csv = '/Users/astha/Downloads/products.csv'
products_df = data_extractor.extract_from_s3(s3_address_csv, local_file_path_csv)
print("Data extracted from S3 csv file")

# Step 2: cleaning - Convert product weights
products_df = data_cleaning.convert_product_weights(products_df)
print("Product weights converted")

# Step 3: Clean the products data
cleaned_products_df = data_cleaning.clean_products_data(products_df)
print("Cleaned Product data")

# Step 4: Upload cleaned data to the database
db_connector.upload_to_db(cleaned_products_df, 'dim_products', creds=local_db_creds)
print("Product data uploaded to dim_products table")


# Milstone 2 - task 7
# List tables
tables = db_connector.list_db_tables()
print("Available tables:", tables)

# Extract orders data
orders_data_df = data_extractor.read_rds_table(db_connector, 'orders_table')
print("Extracted user data from AWS RDS database: orders_table")

# Clean orders data
cleaned_orders_data_df = data_cleaning.clean_orders_data(orders_data_df)
print("Cleaned orders data")

# Upload cleaned data to the local database
local_db_connector.upload_to_db(cleaned_orders_data_df, 'orders_table', creds = local_db_creds)
print("Uploaded cleaned data to orders_table table in sales_data")


# Milstone 2 - task 8
s3_address_json = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'
local_file_path_json = '/Users/astha/Downloads/date_details.json'

# extract date and times detail
date_details_df = data_extractor.extract_from_https(s3_address_json, local_file_path_json)
print("Data extracted from S3 JSON file")

# Step 2: Clean the dates and time data
cleaned_date_details_df = data_cleaning.clean_date_times_data(date_details_df)
print("Cleaned date details")

# Upload cleaned data to the local database
local_db_connector.upload_to_db(cleaned_date_details_df, 'dim_date_times', creds = local_db_creds)
print("Uploaded cleaned data to dim_date_times table in sales_data")


