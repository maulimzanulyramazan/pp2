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
ALTER TABLE contacts
ALTER COLUMN phone TYPE VARCHAR(25);
""")
conn.commit()
print("CHANGED")
cur.close()
conn.close()