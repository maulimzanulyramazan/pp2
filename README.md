📌 Description

This project is a simple PhoneBook application built with Python and PostgreSQL.
It allows users to store, manage, and search contacts in a database.

⚙️ Features
Create a contacts table in PostgreSQL
Insert contacts from a CSV file
Add new contacts from console input
Update contact name or phone number
Search contacts:
by name (case-insensitive)
by phone prefix
Delete contacts:
by name
by phone number
🛠️ Technologies Used
Python
PostgreSQL
psycopg2
CSV module
📂 Project Structure
Practice7/
│── phonebook.py
│── connect.py
│── config.py
│── contacts.csv
🚀 How to Run
Install dependencies:
pip install psycopg2-binary
Configure database connection in config.py:
host = "localhost"
database = "your_database"
user = "postgres"
password = "your_password"
port = "your_port"
Run the program:
python phonebook.py
📄 CSV Format

Example contacts.csv:

name,phone
Roma,87771234567
Timur,87011234567
Aruzhan,87471234567
💡 Notes
Phone numbers must be unique (UNIQUE constraint)
Phone numbers are stored as BIGINT
The program uses parameterized queries to prevent SQL injection
📌 Conclusion

This project demonstrates basic CRUD operations (Create, Read, Update, Delete) with PostgreSQL using Python.
It is a simple but practical example of working with databases.