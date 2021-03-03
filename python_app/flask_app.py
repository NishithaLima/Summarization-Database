import flask
from flask import request
from flask_cors import CORS, cross_origin
import json

from db_scripts import *

app = flask.Flask("flask_server")
app.config["DEBUG"] = True
CORS(app)

database = r"wikisql.db"
conn = create_connection(database)

@app.route("/" , methods=["GET"])
def home():
    return "Running Flask server"

@app.route("/tables", methods=["GET"])
@cross_origin(origin='*')
def get_tables():
    conn = create_connection(database)
    
    with conn:
        
        tbl = list_tables(conn)
        print("Total Tables:", len(tbl))
        return json.dumps({"tables":tbl})



@app.route("/table_min_row", methods=["GET"])
@cross_origin(origin='*')
def get_table_rowcount():

    min_r = request.args.get('min')
    min_r = 100 if min_r == None else int(min_r)
    conn = create_connection(database)

    
    
    with conn:
        
        tbl = list_tables(conn)

        lst = row_count(conn, tbl, min_r)
        
        return json.dumps({"tables":[t['table_name'] for t in lst]})


@app.route("/table_row_col_count", methods=["GET"])
@cross_origin(origin='*')
def get_table_row_col_count():
    tbl = request.args.get('tbl')
    conn = create_connection(database)

    
    with conn:
        
        tbl = get_row_column_count(conn, tbl)
        
        return json.dumps(tbl)


@app.route("/tablesData", methods=["GET"])
@cross_origin(origin='*')
def get_tabledata():
    tbl = request.args.get('tbl')
    conn = create_connection(database)
    
    with conn:
        
        tbl = get_table_data(conn, tbl)
        return json.dumps({"tables":tbl})



app.run()