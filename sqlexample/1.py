import psycopg2

conn = psycopg2.connect(
    host = 'localhost',
    database = 'myfirstdb',
    user = 'postgres',
    password = '550697',
    port = '2008'    
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(25),
    phone INT
);
""")

conn.commit()
print("Table created")
cur.close()
conn.close()