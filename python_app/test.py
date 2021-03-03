import sqlite3
from db_scripts import *

database = r"D:\DKE\DBSE Project\WikiSQL-master\data\train.db"

    # create a database connection
conn = create_connection(database)
with conn:
    print("Tables:")
    list_tables(conn)