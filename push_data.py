

import os
import sys
import certifi
import pandas as pd
import pymongo

from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


# Load environment variables
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class NetworkDataExtract:

    def __init__(self):
        try:
            if not MONGO_DB_URL:
                raise ValueError("MONGO_DB_URL is not configured")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Convert CSV into list of dictionaries
    def csv_to_json_converter(self, file_path):

        try:
            logging.info("Reading CSV file")

            data = pd.read_csv(file_path)

            records = data.to_dict(orient="records")

            logging.info(
                f"Successfully converted {len(records)} records"
            )

            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Insert records into MongoDB
    def insert_data_mongodb(self, records, database, collection_name):

        client = None

        try:
            logging.info("Connecting to MongoDB Atlas")

            client = pymongo.MongoClient(
                MONGO_DB_URL,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=5000
            )

            # Verify connection
            client.admin.command("ping")

            logging.info("MongoDB connection successful")

            # Select database
            db = client[database]

            # Select collection
            collection = db[collection_name]

            # Insert records
            result = collection.insert_many(records)

            inserted_count = len(result.inserted_ids)

            logging.info(
                f"Successfully inserted {inserted_count} records"
            )

            return inserted_count

        except Exception as e:
            raise NetworkSecurityException(e, sys)

        finally:
            if client is not None:
                client.close()


if __name__ == "__main__":

    try:
        FILE_PATH = "Network_Data/PhisingData.csv"

       
        DATABASE = "MasumAI"

        COLLECTION = "NetworkData"

        # Create object
        network_obj = NetworkDataExtract()

        # Convert CSV into records
        records = network_obj.csv_to_json_converter(FILE_PATH)

        print("Total records:", len(records))

        # Insert records into MongoDB
        count = network_obj.insert_data_mongodb(
            records,
            DATABASE,
            COLLECTION
        )

        print("Successfully inserted records:", count)

    except Exception as e:
        logging.error(f"Data extraction failed: {e}")
        raise




























# # 1. Load your .env file
# load_dotenv()
# uri = os.getenv("MONGO_URL")

# # Stop immediately if MONGO_URL wasn't loaded from .env
# if not uri:
#     raise ValueError("❌ MONGO_URL not found! Make sure your file is named '.env' (not '.env.txt') and contains MONGO_URL=...")

# # 2. Initialize client with a 5-second timeout so it doesn't hang if blocked
# client = MongoClient(uri, serverSelectionTimeoutMS=5000)

# try:
#     # 3. Force a connection check using 'ping'
#     response = client.admin.command("ping")
#     print("✅ Connected successfully! Ping response:", response)

#     # Optional: List existing databases to confirm permissions
#     print("📂 Databases available:", client.list_database_names())

# except OperationFailure as e:
#     print("❌ Authentication failed (Wrong username, password, or user permissions):", e)
# except ConnectionFailure as e:
#     print("❌ Network error (Check your Atlas IP Whitelist or internet connection):", e)
# except Exception as e:
#     print("❌ Unexpected error:", e)
# finally:
#     client.close()
