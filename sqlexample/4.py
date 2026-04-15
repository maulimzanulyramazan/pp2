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
UPDATE contacts
SET phone = '87474897545'
WHERE name = 'Roma';
""")
conn.commit()
print("updated")
cur.close()
conn.close()