import streamlit as st
import sqlite3
import hashlib
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import networkx as nx

# Connect to SQLite database
conn = sqlite3.connect("blood_bank.db", check_same_thread=False)
c = conn.cursor()

# Create Tables if not exists
def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS donors (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 age INTEGER NOT NULL,
                 blood_type TEXT NOT NULL,
                 units INTEGER NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 hospital TEXT NOT NULL,
                 blood_type TEXT NOT NULL,
                 units INTEGER NOT NULL,
                 timestamp TEXT NOT NULL,
                 transaction_id TEXT NOT NULL,
                 previous_hash TEXT NOT NULL)''')

    conn.commit()

# Hashing Function
def generate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Register a Donor
def register_donor():
    st.subheader("Register a New Donor")
    
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    blood_type = st.selectbox("Blood Type", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    units = st.number_input("Blood Units Donated", min_value=1, step=1)

    if st.button("Register Donor"):
        if name and blood_type and units > 0:
            c.execute("INSERT INTO donors (name, age, blood_type, units) VALUES (?, ?, ?, ?)", 
                      (name, age, blood_type, units))
            conn.commit()
            st.success(f"Donor {name} registered successfully!")
        else:
            st.error("Please fill in all fields.")

# View Inventory
def view_inventory():
    st.subheader("Blood Bank Inventory")

    c.execute("SELECT blood_type, SUM(units) FROM donors GROUP BY blood_type HAVING SUM(units) > 0")
    data = c.fetchall()

    if data:
        df = pd.DataFrame(data, columns=["Blood Type", "Total Units"])
        st.table(df)
    else:
        st.warning("No blood units available.")

# Process a Blood Transaction
def make_transaction():
    st.subheader("Hospital Blood Request")

    hospital = st.text_input("Hospital Name")
    blood_type = st.selectbox("Blood Type Needed", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    units = st.number_input("Units Required", min_value=1, step=1)

    if st.button("Process Transaction"):
        c.execute("SELECT SUM(units) FROM donors WHERE blood_type = ?", (blood_type,))
        available_units = c.fetchone()[0] or 0

        if available_units >= units:
            timestamp = str(datetime.datetime.now())
            c.execute("SELECT transaction_id FROM transactions ORDER BY id DESC LIMIT 1")
            previous_hash = c.fetchone()
            previous_hash = previous_hash[0] if previous_hash else "0"

            transaction_data = f"{hospital}{blood_type}{units}{timestamp}{previous_hash}"
            transaction_id = generate_hash(transaction_data)

            c.execute("INSERT INTO transactions (hospital, blood_type, units, timestamp, transaction_id, previous_hash) VALUES (?, ?, ?, ?, ?, ?)",
                      (hospital, blood_type, units, timestamp, transaction_id, previous_hash))

            # Reduce units from available donors in order
            remaining_units = units
            while remaining_units > 0:
                c.execute("SELECT id, units FROM donors WHERE blood_type = ? AND units > 0 ORDER BY id LIMIT 1", (blood_type,))
                donor = c.fetchone()
                if not donor:
                    break  # No more donors to deduct from

                donor_id, donor_units = donor
                if donor_units <= remaining_units:
                    c.execute("DELETE FROM donors WHERE id = ?", (donor_id,))
                    remaining_units -= donor_units
                else:
                    c.execute("UPDATE donors SET units = units - ? WHERE id = ?", (remaining_units, donor_id))
                    remaining_units = 0

            conn.commit()
            st.success(f"Transaction successful! Transaction ID: {transaction_id}")
        else:
            st.error("Not enough blood units available.")

# View Transaction History
def transaction_history():
    st.subheader("Transaction History")

    c.execute("SELECT * FROM transactions")
    data = c.fetchall()

    if data:
        df = pd.DataFrame(data, columns=["ID", "Hospital", "Blood Type", "Units", "Timestamp", "Transaction ID", "Previous Hash"])
        st.table(df)

        st.subheader("Blockchain Network Representation")
        plot_blockchain(df)
    else:
        st.warning("No transactions recorded.")

# Plot Blockchain Network
def plot_blockchain(df):
    G = nx.DiGraph()

    for _, row in df.iterrows():
        G.add_edge(row["Previous Hash"], row["Transaction ID"], label=row["Blood Type"])

    plt.figure(figsize=(10, 5))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2000, font_size=8)
    labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    st.pyplot(plt)

# Initialize Database
create_tables()

# Streamlit UI
st.title("🩸 Blockchain-based Blood Bank Inventory Manager")

menu = ["Home", "Register Donor", "Inventory", "Transactions", "Transaction History"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register Donor":
    register_donor()
elif choice == "Inventory":
    view_inventory()
elif choice == "Transactions":
    make_transaction()
elif choice == "Transaction History":
    transaction_history()
else:
    st.subheader("Welcome to the Blockchain-based Blood Bank")
    st.write("Use the sidebar to navigate through the application.")
