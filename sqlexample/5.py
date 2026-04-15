import psycopg2
conn = psycopg2.connect(
    host = 'localhost',
    database = 'myfirstdb',
    user = 'postgres',
    password = '550697',
    port = '2008' 
)
cur = conn.cursor()
cur.execute('''
DELETE FROM contacts
WHERE name = 'Aruzhan'            
''')
conn.commit()
print("DELETED")
cur.close()
conn.close()