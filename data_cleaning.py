#  methods to clean data from each of the data sources.
import pandas as pd
import re
from datetime import datetime
import numpy as np

class DataCleaning:

    def __init__(self):
        pass
    
    def correct_nonstandard_date(date_str):
            # date_str = str(date_str).strip()
            formats = [
                "%B %Y %d", # e.g., October 2012 08
                "%b %Y %d", # e.g., Oct 2012 08
                "%Y-%m-%d", # e.g., 2006-01-13
                "%Y/%m/%d", # e.g., 2012/10/08
                "%Y %b %d", # e.g., 2020 Oct 01
                "%Y %B %d" # e.g., 2020 October 01
            ]
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt).date()
                except ValueError:
                    continue
        
            return None 
        

    def clean_user_data(self, df):
        
        df['date_of_birth'] = df['date_of_birth'].apply(DataCleaning.correct_nonstandard_date)
        df.dropna(subset=['date_of_birth'], inplace=True)
        return df
    

    # milestone 2 task 4
    def clean_card_data(self, df):

        # Step 1: Convert empty string, "NULL" or 'NaN' in string format and other non-numeric strings to NaN
        df['card_number'] = df['card_number'].replace(['NULL','NaN', ''], np.nan)

        # Step 2: Remove all non-numeric characters
        df['card_number'] = df['card_number'].astype(str).str.replace(r'\D', '', regex=True)

        df.dropna(subset=['card_number'], inplace=True) 
        df.drop_duplicates(inplace=True) # removes  duplicates

        df['date_payment_confirmed'] = df['date_payment_confirmed'].apply(DataCleaning.correct_nonstandard_date)
        df.dropna(subset=['date_payment_confirmed'], inplace=True) 
        
        return df
    

   # milestone 2 task 5
    def clean_store_data(self, df):
        
        # Apply the custom parsing function to the opening_date column
        df['opening_date'] = df['opening_date'].apply(DataCleaning.correct_nonstandard_date)
        df.dropna(subset=['opening_date'], inplace=True)
        
        def extract_numeric(value):
            return ''.join(filter(str.isdigit, str(value)))

        # Apply the function to the 'staff_numbers' column
        df['staff_numbers'] = df['staff_numbers'].apply(extract_numeric)

        return df
        
    

    # Milestone 2 task 6

    def clean_products_data(self, df):
        df = df.dropna(subset=['weight'])
        return df
    
    #  take the products DataFrame as an argument and return the products DataFrame.
    def convert_product_weights(self, df):
        # Function to convert different weight units to kilograms
        
        def convert_to_kg(weight):
            weight = str(weight).lower().replace(' ', '')
            
            # Handle expressions like "40 x 100g"
            if 'x' in weight and 'g' in weight:
                match = re.match(r"(\d+)\s*x\s*(\d+)\s*g", weight)
                if match:
                    multiplier = int(match.group(1))
                    unit_in_grams = int(match.group(2))
                    total_grams = multiplier * unit_in_grams
                    return total_grams / 1000  # Convert to kg
            
            # Handle kg directly
            if 'kg' in weight:
                no_unit = weight.replace('kg', '')
                try:
                    return float(no_unit)
                except ValueError:
                    return None
                
            # Handle grams
            elif 'g' in weight:
                no_unit = weight.replace('g', '')
                try:
                    return float(no_unit)/1000
                except ValueError:
                    return None
            
            # Handle milliliters
            elif 'ml' in weight:
                no_unit = weight.replace('ml', '')
                try:
                    return float(no_unit)/1000
                except ValueError:
                    return None
            
            # Handle liters
            elif 'l' in weight:
                no_unit = weight.replace('l', '')
                try:
                    return float(no_unit)
                except ValueError:
                    return None
                
            # Handle oz
            elif 'oz' in weight:
                no_unit = weight.replace('oz', '')
                try:
                    return float(no_unit)/35.274
                except ValueError:
                    return None
                
            else:
                return None

        # Apply the conversion function to the weight column
        df['weight'] = df['weight'].apply(convert_to_kg)
        return df


    #Milestone 2 - Step 7
    def clean_orders_data(self, df):
        # Remove the columns: 'first_name', 'last_name', and '1'
        df = df.drop(columns=['first_name', 'last_name', '1'], errors='ignore')
        return df
    

    #Milestone 2 - Step 8
    def clean_date_times_data(self, df):
        df.drop_duplicates(inplace=True) # removes  duplicates

        df['month'] = pd.to_numeric(df['month'], errors='coerce')
        df = df[(df['month'] >= 1) & (df['month'] <= 12)]
        df = df.dropna(subset=['month'])
        return df
