import pandas as pd
import os
from dotenv import load_dotenv
from snowflake.connector import connect 
from snowflake.connector.pandas_tools import write_pandas  
from pathlib import Path

#Load environment variables from .env file
env_path = Path(r"E:\de_project_v1\.env")
load_dotenv(env_path, override=True)
required = ["SNOW_USER","SNOW_PASSWORD","SNOW_ACCOUNT","SNOW_WAREHOUSE","SNOW_DATABASE","SNOW_SCHEMA"]
missing = [k for k in required if not os.getenv(k)]
if missing:
    raise ValueError(f"Missing env vars: {missing}")


#Establish connection to Snowflake using SQL connector 
conn = connect(
    user=os.getenv("SNOW_USER"),
    password=os.getenv("SNOW_PASSWORD"),
    account=os.getenv("SNOW_ACCOUNT"),
    warehouse=os.getenv("SNOW_WAREHOUSE")
)
#That block is setting the session context for your Snowflake connection. 
#Think of it like telling Snowflake: “From now on, assume I’m working in this warehouse, 
#this database, and this schema unless I say otherwise.”
with conn.cursor() as cur:
    # Select compute
    cur.execute(f"USE WAREHOUSE {os.getenv('SNOW_WAREHOUSE')}")

    # Create database if it does not already exist
    cur.execute(
        f"CREATE DATABASE IF NOT EXISTS {os.getenv('SNOW_DATABASE')}"
    )

    # Create schema if it does not already exist
    cur.execute(
        f"CREATE SCHEMA IF NOT EXISTS "
        f"{os.getenv('SNOW_DATABASE')}.{os.getenv('SNOW_SCHEMA')}"
    )

    # Set current database and schema for this session
    cur.execute(f"USE DATABASE {os.getenv('SNOW_DATABASE')}")
    cur.execute(f"USE SCHEMA {os.getenv('SNOW_SCHEMA')}")

#Path to Dataset folder and CSV file
folder_path = 'E:/de_project_v1/dataset'

# Loop through each CSV file, load it into a DataFrame, then upload it to Snowflake
for filename in os.listdir(folder_path): #os.listdir(folder_path) returns a list of names (strings) for everything inside that folder: files + subfolders.
    if filename.endswith('.csv'):
        # Create a clean table name: olist_orders_dataset.csv -> OLIST_ORDERS
        table_name = filename.replace("_dataset.csv", "").replace(".csv", "").upper()
        file_path = os.path.join(folder_path, filename) 
        #Builds the full path to the file. 
        #Example:folder_path = "E:/AE_first_Project/dataset" . 
        #filename = "olist_orders_dataset.csv" file_path becomes: "E:/AE_first_Project/dataset/olist_orders_dataset.csv". 
        #This is important because pd.read_csv() needs a full path (or it must be run from the correct directory).
        #Load the CSV file into a DataFrame
        print(f"📦 Loading {filename}...")
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.upper()
#Push the DataFrame to Snowflake
        success, nchunks, nrows, _ = write_pandas(
            conn=conn, 
            df=df, 
            table_name= table_name,
            auto_create_table=True, #Create table if already not exist in snowflake
            overwrite=True #Overwrite the table if it already exists in Snowflake
            )
        if success:
            print(f"Successfully ingested {nrows} rows into Snowflake.")
        else:
            print("Failed to ingest data into Snowflake.") 
conn.close()