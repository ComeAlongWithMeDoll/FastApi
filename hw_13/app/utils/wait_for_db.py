import time
import psycopg2
from psycopg2 import OperationalError

def wait_for_postgres(host, port, db, user, password):
    for attempt in range(30):  # было 10
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=db,
                user=user,
                password=password
            )
            conn.close()
            print("[wait-for-db] PostgreSQL is ready!")
            return
        except Exception as e:
            print(f"[wait-for-db] PostgreSQL not ready yet (attempt {attempt+1}/30) — retrying...")
            time.sleep(2)  # было 1
    raise Exception("PostgreSQL did not become ready in time.")
