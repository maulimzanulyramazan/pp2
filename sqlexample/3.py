import psycopg2
conn = psycopg2.connect(
    host = 'localhost',
    database = 'myfirstdb',
    user = 'postgres',
    password = '550697',
    port = '2008'
)

cur = conn.cursor()
cur.execute("SELECT * FROM contacts ORDER BY id;")
rows = cur.fetchall()
for row in rows:
    print(*row)
cur.close()
conn.close()