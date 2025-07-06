import psycopg2

def connect_db():
    # Connect to your postgres DB
    conn = psycopg2.connect("host=localhost dbname=Linkado user=aplicacao password=senha123")

# Open a cursor to perform database operations
    cur = conn.cursor()

# Execute a query
    cur.execute("SELECT * FROM contas")

# Retrieve query results
    records = cur.fetchall()
    return records
