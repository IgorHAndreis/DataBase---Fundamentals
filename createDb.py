import psycopg2

def connect_db():
    # Connect to your postgres DB
    conn = psycopg2.connect("host=localhost dbname=Linkado user=aplicacao password=senha123")
    return conn

def select_handler(conn:psycopg2.extensions.connection, query, args: list = []):
    cur = conn.cursor()
    cur.execute(query, args)
    records = cur.fetchall()
    return records

