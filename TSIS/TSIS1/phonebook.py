# ============================================
# PHONEBOOK APPLICATION - MAIN FILE
# Extended contact management system
# ============================================

import psycopg2          # PostgreSQL adapter
import json              # JSON file handling
import csv               # CSV file handling
from datetime import datetime  # Date handling
from connect import connect    # Database connection module

# ============================================
# DATABASE CONNECTION HELPER
# ============================================

def get_conn():
    """Get database connection"""
    return connect()

def execute_sql(sql, params=None, fetch=False):
    """Execute SQL query with optional parameters"""
    conn = get_conn()
    cur = conn.cursor()
    try:
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        if fetch:
            result = cur.fetchall()
            conn.commit()
            return result
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        raise
    finally:
        cur.close()
        conn.close()

# ============================================
# TABLE CREATION
# ============================================

def create_tables():
    """Create all tables (contacts, groups, phones)"""
    try:
        with open('schema.sql', 'r') as f:      # Read schema file
            sql = f.read()                      # Get SQL content
            execute_sql(sql)                    # Execute schema
        print("Tables created successfully")
    except FileNotFoundError:
        print("schema.sql file not found")

# ============================================
# BASIC CRUD OPERATIONS
# ============================================

def insert_contact():
    """Add new contact with email, birthday, and group"""
    name = input("Enter name: ")                         # Get name
    email = input("Enter email (optional): ") or None    # Get email
    birthday = input("Enter birthday (YYYY-MM-DD): ") or None  # Get birthday
    phone = input("Enter phone: ")                       # Get phone
    group_name = input("Enter group (Family/Work/Friend/Other): ") or None  # Get group
    
    conn = get_conn()
    cur = conn.cursor()
    try:
        # Insert contact with group
        if group_name:
            cur.execute("""
                INSERT INTO contacts (name, email, birthday, group_id)
                VALUES (%s, %s, %s, (SELECT id FROM groups WHERE name = %s))
                RETURNING id
            """, (name, email, birthday, group_name))
        else:
            cur.execute("""
                INSERT INTO contacts (name, email, birthday)
                VALUES (%s, %s, %s) RETURNING id
            """, (name, email, birthday))
        
        contact_id = cur.fetchone()[0]          # Get new contact ID
        # Insert main phone
        cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                   (contact_id, phone, 'mobile'))
        conn.commit()
        print(f"Contact '{name}' added successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

def show_all_contacts():
    """Display contacts with sequential numbers"""
    conn = get_conn()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT 
            c.name, 
            c.email, 
            c.birthday, 
            COALESCE(g.name, 'No group') as group_name,
            STRING_AGG(DISTINCT p.phone || '(' || p.type || ')', ', ') as phones,
            ROW_NUMBER() OVER (ORDER BY c.id) as num
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
        ORDER BY c.id
    """)
    rows = cur.fetchall()
    
    if not rows:
        print("No contacts found")
    else:
        for row in rows:
            print(f"\n{row[5]}. {row[0]}")  # 1. Ramazan
            print(f"   Email: {row[1] or 'No email'}")
            print(f"   Birthday: {row[2] or 'Not set'}")
            print(f"   Group: {row[3]}")
            print(f"   Phones: {row[4] or 'No phones'}")
            print("-" * 30)
    
    cur.close()
    conn.close()

# ============================================
# SEARCH & FILTER FUNCTIONS
# ============================================

def filter_by_group():
    """Show contacts only from selected group"""
    group_name = input("Enter group name (Family/Work/Friend/Other): ")
    conn = get_conn()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT 
            c.id, 
            c.name, 
            c.email, 
            STRING_AGG(p.phone || '(' || p.type || ')', ', ') as phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE g.name = %s
        GROUP BY c.id, c.name, c.email
        ORDER BY c.name
    """, (group_name,))
    rows = cur.fetchall()
    
    if not rows:
        print(f"No contacts in group '{group_name}'")
    else:
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2] or 'N/A'}")
            print(f"Phones: {row[3] or 'No phones'}")
            print("-" * 20)
    
    cur.close()
    conn.close()

def search_by_email():
    """Search contacts by email (partial match)"""
    pattern = input("Enter email pattern (e.g., 'gmail'): ")
    conn = get_conn()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, name, email, birthday 
        FROM contacts
        WHERE email ILIKE %s
        ORDER BY name
    """, (f'%{pattern}%',))
    rows = cur.fetchall()
    
    if not rows:
        print("No contacts found")
    else:
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Birthday: {row[3] or 'N/A'}")
    
    cur.close()
    conn.close()

def advanced_search():
    """Search all fields - working version"""
    pattern = input("Enter search pattern: ")
    conn = get_conn()
    cur = conn.cursor()
    
    # Direct SQL query - no function needed
    cur.execute("""
        SELECT 
            c.id,
            c.name,
            COALESCE(c.email, 'No email') as email,
            c.birthday,
            COALESCE(g.name, 'No group') as group_name,
            STRING_AGG(DISTINCT p.phone || '(' || p.type || ')', ', ') as phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE c.name ILIKE %s
           OR c.email ILIKE %s
           OR p.phone ILIKE %s
           OR g.name ILIKE %s
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
        ORDER BY c.id
    """, (f'%{pattern}%', f'%{pattern}%', f'%{pattern}%', f'%{pattern}%'))
    
    rows = cur.fetchall()
    
    if not rows:
        print("No contacts found")
    else:
        print(f"\nFound {len(rows)} contact(s):")
        for row in rows:
            print(f"\nID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Email: {row[2]}")
            print(f"Birthday: {row[3] or 'Not set'}")
            print(f"Group: {row[4]}")
            print(f"Phones: {row[5] or 'No phones'}")
            print("-" * 30)
    
    cur.close()
    conn.close()

# ============================================
# SORTING FUNCTIONS
# ============================================

def sorted_contacts():
    """Display contacts sorted by name, birthday, or creation date"""
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by date added")
    choice = input("Choose: ")
    
    # Define sort column based on user choice
    if choice == "1":
        order_by = "c.name"
    elif choice == "2":
        order_by = "c.birthday NULLS LAST"
    elif choice == "3":
        order_by = "c.created_at"
    else:
        order_by = "c.name"
    
    conn = get_conn()
    cur = conn.cursor()
    # Dynamic ORDER BY
    cur.execute(f"""
        SELECT c.id, c.name, c.birthday, c.created_at, c.email,
               STRING_AGG(p.phone || '(' || p.type || ')', ', ') as phones
        FROM contacts c
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, c.name, c.birthday, c.created_at, c.email
        ORDER BY {order_by}
    """)
    rows = cur.fetchall()
    for row in rows:
        print(f"Name: {row[1]}, Birthday: {row[2] or 'N/A'}, Added: {row[3]}, Phones: {row[5] or 'N/A'}")
    cur.close()
    conn.close()

# ============================================
# PAGINATED NAVIGATION
# ============================================

def paginated_navigation():
    """Interactive page navigation using database pagination"""
    limit = int(input("Enter records per page: "))  # Items per page
    page = 0  # Start from page 0
    
    while True:
        offset = page * limit  # Calculate offset
        conn = get_conn()
        cur = conn.cursor()
        # Get paginated results
        cur.execute("""
            SELECT c.id, c.name, c.email, STRING_AGG(p.phone || '(' || p.type || ')', ', ') as phones
            FROM contacts c
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, c.name, c.email
            ORDER BY c.id
            LIMIT %s OFFSET %s
        """, (limit, offset))
        rows = cur.fetchall()
        
        if not rows and page > 0:
            print("End of records")
            break
        elif not rows:
            print("No contacts")
            break
        
        print(f"\n--- Page {page + 1} ---")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2] or 'N/A'}, Phones: {row[3] or 'N/A'}")
        
        cur.close()
        conn.close()
        
        # Navigation menu
        print("\nCommands: next, prev, quit")
        cmd = input("Enter command: ").lower()
        if cmd == 'next':
            page += 1
        elif cmd == 'prev' and page > 0:
            page -= 1
        elif cmd == 'quit':
            break
        else:
            print("Invalid command")

# ============================================
# PHONE AND GROUP MANAGEMENT
# ============================================

def add_phone():
    """Add new phone to existing contact - FIXED"""
    name = input("Enter contact name: ")
    phone = input("Enter phone number: ")
    p_type = input("Enter type (home/work/mobile): ").lower()
    
    if p_type not in ['home', 'work', 'mobile']:
        p_type = 'mobile'
    
    conn = get_conn()
    cur = conn.cursor()
    try:
        # Check if contact exists
        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        contact = cur.fetchone()
        if not contact:
            print(f"✗ Contact '{name}' not found!")
            return
        
        # Add phone
        cur.execute("""
            INSERT INTO phones (contact_id, phone, type)
            VALUES (%s, %s, %s)
        """, (contact[0], phone, p_type))
        
        conn.commit()
        print(f"✓ Phone '{phone}' added to '{name}'")
    except Exception as e:
        conn.rollback()
        print(f"✗ Error: {e}")
    finally:
        cur.close()
        conn.close()
def move_to_group():
    """Move contact to group - FIXED"""
    name = input("Enter contact name: ")
    group_name = input("Enter group name: ")
    
    conn = get_conn()
    cur = conn.cursor()
    try:
        # Check contact exists
        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        contact = cur.fetchone()
        if not contact:
            print(f"✗ Contact '{name}' not found!")
            return
        
        # Get or create group
        cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
        group = cur.fetchone()
        if not group:
            cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (group_name,))
            group_id = cur.fetchone()[0]
            print(f"✓ Group '{group_name}' created")
        else:
            group_id = group[0]
        
        # Update contact
        cur.execute("UPDATE contacts SET group_id = %s WHERE id = %s", (group_id, contact[0]))
        conn.commit()
        print(f"✓ Contact '{name}' moved to group '{group_name}'")
    except Exception as e:
        conn.rollback()
        print(f"✗ Error: {e}")
    finally:
        cur.close()
        conn.close()

# ============================================
# IMPORT/EXPORT FUNCTIONS
# ============================================

def export_json():
    """Export all contacts to JSON file"""
    filename = input("Enter filename (e.g., contacts.json): ")
    if not filename.endswith('.json'):
        filename += '.json'
    
    conn = get_conn()
    cur = conn.cursor()
    # Get all data including phones as JSON
    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name as group_name,
               COALESCE(json_agg(json_build_object('phone', p.phone, 'type', p.type)) 
               FILTER (WHERE p.id IS NOT NULL), '[]'::json) as phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
        ORDER BY c.id
    """)
    rows = cur.fetchall()
    
    # Convert to list of dictionaries
    contacts = []
    for row in rows:
        contact = {
            "id": row[0], "name": row[1], "email": row[2],
            "birthday": str(row[3]) if row[3] else None,
            "group": row[4], "phones": row[5]
        }
        contacts.append(contact)
    
    # Write to JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)
    
    print(f"Exported {len(contacts)} contacts to {filename}")
    cur.close()
    conn.close()

def import_json():
    """Import contacts from JSON with duplicate handling"""
    filename = input("Enter JSON filename: ")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            contacts = json.load(f)
    except FileNotFoundError:
        print("File not found")
        return
    
    conn = get_conn()
    cur = conn.cursor()
    
    for contact in contacts:
        # Check if contact exists
        cur.execute("SELECT id FROM contacts WHERE name = %s", (contact['name'],))
        existing = cur.fetchone()
        
        if existing:
            print(f"Contact '{contact['name']}' exists")
            choice = input("Skip (s) or Overwrite (o)? ").lower()
            if choice == 's':
                continue
        
        try:
            if existing and choice == 'o':
                # Delete existing (cascade deletes phones)
                cur.execute("DELETE FROM contacts WHERE id = %s", (existing[0],))
            
            # Insert contact
            cur.execute("""
                INSERT INTO contacts (name, email, birthday, group_id)
                VALUES (%s, %s, %s, (SELECT id FROM groups WHERE name = %s))
                RETURNING id
            """, (contact['name'], contact.get('email'), contact.get('birthday'), 
                  contact.get('group', 'Other')))
            
            contact_id = cur.fetchone()[0]
            
            # Insert phones
            for phone_data in contact.get('phones', []):
                cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                           (contact_id, phone_data['phone'], phone_data['type']))
            
            conn.commit()
            print(f"Imported: {contact['name']}")
        except Exception as e:
            conn.rollback()
            print(f"Error: {e}")
    
    cur.close()
    conn.close()
    print("Import completed")

def import_csv_extended():
    """CSV import with new fields (email, birthday, group)"""
    filename = input("Enter CSV filename: ")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            contacts = list(reader)
    except FileNotFoundError:
        print("File not found")
        return
    
    conn = get_conn()
    cur = conn.cursor()
    
    for contact in contacts:
        try:
            # Get values (case insensitive)
            name = contact.get('name', contact.get('Name', ''))
            phone = contact.get('phone', contact.get('Phone', ''))
            email = contact.get('email', contact.get('Email', None)) or None
            birthday = contact.get('birthday', contact.get('Birthday', None)) or None
            group_name = contact.get('group_name', contact.get('Group_name', 'Other'))
            phone_type = contact.get('phone_type', contact.get('Phone_type', 'mobile')).lower()
            
            # Insert contact
            cur.execute("""
                INSERT INTO contacts (name, email, birthday, group_id)
                VALUES (%s, %s, %s, (SELECT id FROM groups WHERE name = %s))
                RETURNING id
            """, (name, email, birthday, group_name))
            
            contact_id = cur.fetchone()[0]
            
            # Insert phone
            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                       (contact_id, phone, phone_type))
            
            conn.commit()
            print(f"Imported: {name}")
        except Exception as e:
            conn.rollback()
            print(f"Error: {e}")
    
    cur.close()
    conn.close()
    print("CSV import completed")

# ============================================
# PRACTICE 8 FUNCTIONS (Kept for compatibility)
# ============================================

def call_pattern_search():
    """Search by pattern using existing function"""
    pattern = input("Enter pattern: ")
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def call_upsert():
    """Insert or update contact"""
    name = input("Enter name: ")
    phone = int(input("Enter phone: "))
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("Done")

def call_bulk_insert():
    """Insert multiple contacts"""
    names = ["Ali", "Aruzhan", "Ulan"]
    phones = ["87771234567", "87011234567", "87013601031"]
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CALL insert_many_users(%s, %s)", (names, phones))
    conn.commit()
    cur.close()
    conn.close()
    print("Batch insert done")

def call_pagination_old():
    """Original pagination function"""
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def call_delete():
    """Delete contact by name or phone"""
    value = input("Enter name or phone to delete: ")
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()
    cur.close()
    conn.close()
    print("Deleted")

# ============================================
# MAIN MENU
# ============================================

def menu():
    """Main interactive menu"""
    while True:
        print("\n" + "="*40)
        print("PHONEBOOK MENU")
        print("="*40)
        print("1. Create tables")
        print("2. Add new contact")
        print("3. Show all contacts")
        print("4. Filter by group")
        print("5. Search by email")
        print("6. Advanced search (all fields)")
        print("7. Sort contacts")
        print("8. Paginated navigation")
        print("9. Add phone to contact")
        print("10. Move contact to group")
        print("11. Export to JSON")
        print("12. Import from JSON")
        print("13. Import from CSV")
        print("14. Pattern search")
        print("15. Upsert contact")
        print("16. Bulk insert")
        print("17. Old pagination")
        print("18. Delete contact")
        print("0. Exit")
        
        choice = input("Choose: ")
        
        if choice == "1":
            create_tables()
        elif choice == "2":
            insert_contact()
        elif choice == "3":
            show_all_contacts()
        elif choice == "4":
            filter_by_group()
        elif choice == "5":
            search_by_email()
        elif choice == "6":
            advanced_search()
        elif choice == "7":
            sorted_contacts()
        elif choice == "8":
            paginated_navigation()
        elif choice == "9":
            add_phone()
        elif choice == "10":
            move_to_group()
        elif choice == "11":
            export_json()
        elif choice == "12":
            import_json()
        elif choice == "13":
            import_csv_extended()
        elif choice == "14":
            call_pattern_search()
        elif choice == "15":
            call_upsert()
        elif choice == "16":
            call_bulk_insert()
        elif choice == "17":
            call_pagination_old()
        elif choice == "18":
            call_delete()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()