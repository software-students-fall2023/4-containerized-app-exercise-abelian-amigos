"""
This file contains the code to connect to the database and database helper functions.
"""
import pymongo

from src.web_app_defaults import (
    MONGO_DB_HOST,
    MONGO_DB_PORT,
    MONGO_DB_USERNAME,
    MONGO_DB_PASSWORD,
    DATABASE_NAME,
)

# make a connection to the database server
if MONGO_DB_USERNAME and MONGO_DB_PASSWORD:
    connection = pymongo.MongoClient(
        MONGO_DB_HOST,
        MONGO_DB_PORT,
        username=MONGO_DB_USERNAME,
        password=MONGO_DB_PASSWORD,
    )
else:
    connection = pymongo.MongoClient(MONGO_DB_HOST, MONGO_DB_PORT)

db = connection[DATABASE_NAME]
