# create a class named DataExtractor
# creating methods that help extract data from different data sources CSV files, an API and an S3 bucket.
import pandas as pd
from database_utils import DatabaseConnector
import tabula
import requests
import boto3


class DataExtractor:

    def __init__(self):
        pass

    def read_rds_table(self, db_connector, table_name): # Milestone 2, task 3, Step 5 -> Extract the table name given "legacy user"
        engine = db_connector.init_db_engine()
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)
        return df
    
    # Milestone 2 - Task 4
    def retrieve_pdf_data(self, pdf_path):
        dfs = tabula.read_pdf(pdf_path,stream=False, pages='all')
        # Combine all DataFrames into a single DataFrame
        combined_df = pd.concat(dfs, ignore_index=True)
        return combined_df
    
    # Milestone 2 - Task 5
    def list_number_of_stores(self, endpoint, headers):
        response = requests.get(endpoint, headers=headers)
        total_number_data = response.json()
        number_of_stores = total_number_data['number_stores']
        return number_of_stores
    
    def retrieve_stores_data(self, endpoint, headers, number_of_stores):
        all_stores_data = []
        for store_number in range(0, number_of_stores + 1):
            store_endpoint = endpoint.format(store_number=store_number)
            response = requests.get(store_endpoint, headers=headers)
            
            if response.status_code == 200:
                store_data = response.json()
                all_stores_data.append(store_data)
            else:
                print(f"Failed to retrieve data for store {store_number}: {response.status_code}")
        
        # Convert the list of stores data into a DataFrame
        stores_df = pd.DataFrame(all_stores_data)
        
        # Return the DataFrame
        return stores_df
    
        

    # Milestone 2 task 6
    def extract_from_s3(self, s3_address, local_file_path):
        # Split the s3 address to get the bucket name and the file key
        s3_parts = s3_address.replace("s3://", "").split("/")
        bucket_name = s3_parts[0]
        object_key = "/".join(s3_parts[1:])
        # Create a session and client
        s3 = boto3.client('s3')
        # Download the file from S3
        s3.download_file(bucket_name, object_key, local_file_path)
        # Load the CSV file into a Pandas DataFrame
        df = pd.read_csv(local_file_path)
        return df
   
    # Milestone 2 task 8
    def extract_from_https(self, s3_address_json, local_file_path_json):
        # Send a GET request to download the file
        response = requests.get(s3_address_json)
        
        # Save the content to a local file
        with open(local_file_path_json, mode = 'r') as date_file:
            df = pd.read_json(local_file_path_json)
        
        return df

