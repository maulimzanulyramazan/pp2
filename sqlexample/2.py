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
INSERT INTO contacts(name, phone)
VALUES
    ('Roma', '87076079108'),
    ('Tima', '87775784751'),
    ('Aruzhan', '87715478965');
""")
conn.commit()
print("ADDED")
cur.close()
conn.close()