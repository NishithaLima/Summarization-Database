import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def list_tables(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    
    rows = cur.fetchall()
    
    return [row[0] for row in rows]


def row_count(conn, tables, min_count = None):
    curr = conn.cursor()
    lst = []
    for t in tables:
        curr.execute("SELECT COUNT(1) FROM " + t )

        r = curr.fetchall()[0][0]
        lst.append({
            "table_name" : t,
            "rows" : r
        })

    print(lst[0])
    if min_count:
        lst = [x for x in lst if x["rows"] > min_count]

    return lst


def get_row_column_count(conn, table):
    curr = conn.cursor()
    curr.execute("SELECT COUNT(1) FROM " + table )
    r = curr.fetchall()[0][0]
    

    curr.execute("pragma table_info(ABC_Amsterdam)")
    c = curr.fetchall()

    return {
        "rows" : r,
        "cols" : len(c)
    }


def get_table_data(conn, table):
    curr = conn.cursor()
    curr.execute("SELECT * from " + table )

    rows = curr.fetchall()
    names =  [d[0] for d in curr.description]

    return {
        "rowsData" :rows,
        "columnNames": names
    }

