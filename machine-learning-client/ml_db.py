"""
This file contains the code to connect to the database and database helper functions.
"""
import pymongo

from ml_defaults import (
    MONGO_HOST,
    MONGO_PORT,
    MONGO_USERNAME,
    MONGO_PASSWORD,
    MONGO_DB_NAME,
)

# make a connection to the database server
if MONGO_USERNAME and MONGO_PASSWORD:
    connection = pymongo.MongoClient(
        MONGO_HOST,
        MONGO_PORT,
        username=MONGO_USERNAME,
        password=MONGO_PASSWORD,
        authSource=MONGO_DB_NAME,
    )
else:
    connection = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)

db = connection[MONGO_DB_NAME]
