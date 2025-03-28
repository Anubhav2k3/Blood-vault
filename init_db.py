import sqlite3
import random

# Connect to database
conn = sqlite3.connect("blood_bank.db")
c = conn.cursor()

# Create donors table with units column
c.execute('''CREATE TABLE IF NOT EXISTS donors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                blood_type TEXT NOT NULL,
                units INTEGER NOT NULL
            )''')

# Create transactions table
c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hospital TEXT NOT NULL,
                blood_type TEXT NOT NULL,
                units INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                transaction_id TEXT NOT NULL,
                previous_hash TEXT NOT NULL
            )''')

# Clear old donor data before inserting new values
c.execute("DELETE FROM donors")

# Blood types
blood_types = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

# Insert prefilled blood units (random between 60 and 100)
for blood_type in blood_types:
    units = random.randint(60, 100)
    c.execute("INSERT INTO donors (name, age, blood_type, units) VALUES (?, ?, ?, ?)",
              ("Initial Stock", 0, blood_type, units))

# Commit and close
conn.commit()
conn.close()

print("Database initialized successfully with prefilled blood units!")
