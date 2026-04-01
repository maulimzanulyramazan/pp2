from connect import connect


def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone BIGINT UNIQUE
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table created successfully")


def call_search_function():
    pattern = input("Enter pattern: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def call_insert_or_update():
    name = input("Enter name: ")
    phone = int(input("Enter phone: "))

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))
    conn.commit()

    cur.close()
    conn.close()
    print("Insert/update done")


def call_insert_many():
    names = ["Ali", "Aruzhan", "Ulan"]
    phones = ["87771234567", "87011234567", "87013601031"]

    conn = connect()
    cur = conn.cursor()
    
    cur.execute("CALL insert_many_users(%s, %s)", (names, phones))
    conn.commit()

    cur.close()
    conn.close()
    print("Batch insert finished")


def call_pagination():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def call_delete():
    value = input("Enter username or phone to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()

    cur.close()
    conn.close()
    print("Delete done")


def show_all():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts ORDER BY id")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Search by pattern")
        print("3. Insert or update one user")
        print("4. Insert many users")
        print("5. Show contacts with pagination")
        print("6. Delete by name or phone")
        print("7. Show all contacts")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            call_search_function()
        elif choice == "3":
            call_insert_or_update()
        elif choice == "4":
            call_insert_many()
        elif choice == "5":
            call_pagination()
        elif choice == "6":
            call_delete()
        elif choice == "7":
            show_all()
        elif choice == "0":
            print("Goodbye")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()