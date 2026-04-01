# 📱 PhoneBook Application (PostgreSQL + Python)

## 📌 Description

This project is a simple PhoneBook application using **Python** and **PostgreSQL**.
It allows the user to store and manage contacts in a database.

The program uses:

* Python → user interface
* PostgreSQL → data storage and logic
* Functions and Procedures → advanced database operations

---

## ⚙️ Features

The application supports:

1. Create contacts table
2. Search contacts by name or phone (pattern search)
3. Insert or update one user
4. Insert multiple users (with validation)
5. Show contacts with pagination (LIMIT & OFFSET)
6. Delete contact by name or phone
7. Show all contacts

---

## 🗄️ Database Structure

Table: `contacts`

* `id` – unique identifier (SERIAL PRIMARY KEY)
* `name` – contact name (VARCHAR)
* `phone` – phone number (VARCHAR)

---

## 🧠 Functions

### 1. search_contacts(pattern_text)

Searches contacts using part of name or phone.

Uses:

* `ILIKE` for case-insensitive search
* `%pattern%` for partial matching

---

### 2. get_contacts_paginated(limit, offset)

Returns contacts in parts using:

* `LIMIT` → number of rows
* `OFFSET` → starting position

---

## ⚡ Procedures

### 1. insert_or_update_user(name, phone)

* Inserts new contact
* Updates phone if contact already exists

---

### 2. insert_many_users(names[], phones[])

* Inserts multiple users
* Uses loop and validation
* Skips incorrect phone numbers

---

### 3. delete_contact(value)

Deletes contact by:

* name
  or
* phone

---

## 🔄 How It Works

1. User selects option from menu
2. Python sends request to PostgreSQL
3. Function or procedure executes
4. Result is returned and printed

---

## 🚀 How to Run

1. Make sure PostgreSQL is running
2. Create database (e.g. `myfirstdb`)
3. Run SQL files:

   * `functions.sql`
   * `procedures.sql`
4. Run Python program:

```bash
py phonebook.py
```

---

## 📁 Project Structure

```
Practice_8/
│
├── phonebook.py
├── connect.py
├── config.py
├── functions.sql
└── procedures.sql
```

---

## 💡 Notes

* Functions return data using `SELECT`
* Procedures perform actions using `CALL`
* Phone numbers are stored as text (VARCHAR)
* ID is auto-generated using SERIAL

---

## 🎯 Conclusion

This project demonstrates how to combine Python and PostgreSQL.
It shows how to use functions, procedures, loops, and conditions in a real application.

---
