import pymongo
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_data_to_collection(client, database_name, collection_name, data):
    """
    Add data to an existing collection in a MongoDB database.

    Args:
        - data: Dictionary containing the data to be inserted.
        - client: pymongo.MongoClient instance.
        - database_name: Name of the MongoDB database.
        - collection_name: Name of the collection to add data.

    Returns:
        - None
    """
    try:
        # Access the specified database and collection
        database = client[database_name]
        collection = database[collection_name]

        # Insert data into the collection
        collection.insert_one(data)
        logger.info('Data added to MongoDB collection')
        

    except pymongo.errors.ConnectionFailure as e:
        # Handling connection errors
        print(f"Could not connect to MongoDB: {e}")
        raise  # Re-raise the exception to signal the error
    except Exception as ex:
        # Handling other unexpected exceptions
        print(f"An error occurred: {ex}")
        raise  # Re-raise the exception to signal the error
