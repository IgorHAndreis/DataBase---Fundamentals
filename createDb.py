import psycopg2



def select_handler(conn:psycopg2.extensions.connection, query, args: list = []):
    cur = conn.cursor()
    cur.execute(query, args)
    records = cur.fetchall()
    cur.close()
    return records

