'''Saves a WikiSql jsonl file of data, after data cleaning, into an sqlite database.
Needs a hard-coded path for the jsonl file.'''
import json
import sqlite3
import re
from sqlite3 import Error
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as err:
        print(err)
    return connection

def create_table(connection, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_sql)
    except Error as err:
        print(err)

def clean_string(string):
    '''Cleans a string that represents a table or column name. Returns cleaned string.'''
    #bad characters for an identifier
    result = string.replace(" ","_").replace(".","_").replace("#","Nr").replace("@","_")
    result = result.replace("&","_").replace("%","_").replace("$","dolars_").replace(")","_")
    result = result.replace("-","_").replace("/","_").replace("?","_").replace(":","_")
    result = result.replace("+","_").replace(";","_").replace("'","_").replace(">","_")
    result = result.replace("\"","_").replace("]","_").replace("[","_").replace("!","")
    result = result.replace("\\","_").replace("~","approx_").replace("^","_").replace("{","_")
    result = result.replace("’","_").replace("}","_").replace("′^","_").replace("=","_")
    result = result.replace(",","_").replace("(","_").replace("*","_")
    reserved_words = {"from" : "source", "group" : "team", "to" : "target",#reserved words
    "order" : "ranking", "index" : "ind", "as" : "A_s", "drop" : "Drops",
    "where" : "location", "table" : "tab", "total" : "tot"}
    if result.lower() in reserved_words:
        return reserved_words[result.lower()]
    if result.isnumeric():
        if int(result)>1500:
            result = "year_"+result #if it looks like a year, we append that
        else:
            result = "points_"+result
    #if it starts with a digit we make it start with an underscore
    if len(result)>0 and result[0].isdigit():
        result = "_"+result
    #we reduce to a size of one, all sequences of underscores after our replacements
    result = re.sub('_+', '_', result)
    return result

def main():
    '''core data cleaning and database generation/filling'''
    conn = create_connection(r"/home/campero/Desktop/wikisql.db")
    data = []
    with open('train.tables.jsonl') as input_file:
        for line in input_file:
            data.append(json.loads(line))
    all_tables = 0
    tables_inserted=set()
    for item in data:
        all_tables+=1
        if "page_title" in item:
            table_name = clean_string(item["page_title"])
            version_number = 1
            temp_str = table_name
            while temp_str in tables_inserted:
                temp_str = table_name+"_"+str(version_number)
                version_number+=1
            if version_number>1:
                table_name+="_"+str(version_number-1)
            tables_inserted.add(table_name)
            sql_create_table = """ CREATE TABLE IF NOT EXISTS """+table_name+""" ( """
            columns = set()
            temp_str = clean_string(item["header"][0])
            columns.add(temp_str.lower())
            sql_create_table+=" "+temp_str+" "+item["types"][0]+" "
            for i in range(len(item["header"])-1):
                temp_str = clean_string(item["header"][i+1])
                if temp_str.lower() in columns:
                    version_number = 1
                    while temp_str.lower()+"_"+str(version_number) in columns:
                        version_number+=1
                    temp_str += "_"+str(version_number)
                columns.add(temp_str.lower())
                sql_create_table+=", "+temp_str+" "+item["types"][i+1]
            sql_create_table+=""+""" ); """
            #print(sql_create_table)
            create_table(conn,sql_create_table)
            conn.commit()
            records = [tuple(row) for row in item["rows"]]
            try:
                temp_str = ",".join(["?" for row in item["header"]])
                conn.executemany("INSERT INTO "+table_name+" VALUES("+temp_str+");",records)
                conn.commit()
                print("{}: Created-{}".format(str(all_tables), table_name))
            except Error as err:
                print(err)
                #print(records)
                #print(item["rows"])
                #print(sql_create_table)
                print("{}: Error-{}".format(str(all_tables),table_name))
        else:
            print("{}: Skipped (no page title/table name)".format(str(all_tables)))
    print("Created {}/{} tables.".format(str(len(tables_inserted)),str(all_tables)))

if __name__ == "__main__":
    main()
