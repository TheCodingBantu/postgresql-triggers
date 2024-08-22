import psycopg2
import select
import json

# Connection parameters
conn = psycopg2.connect(
    dbname="scrapper",
    user="phil",
    password="password",  # Add your password here
    host="localhost",     # Use 'localhost' or your DB host
    port="5432"           # Default PostgreSQL port is 5432
)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cur = conn.cursor()
cur.execute("LISTEN table_update;")

print("Waiting for notifications on channel 'table_update'")
while True:
    if select.select([conn], [], [], 5) == ([], [], []):
        pass
    else:
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            # Parse the JSON payload
            payload = json.loads(notify.payload)
            operation = payload.get('operation')
            table = payload.get('table')
            row_data = payload.get('data')
            
            print(f"Operation: {operation}")
            print(f"Table: {table}")
            print("Row data:", row_data)
