Blockchain-Based Blood Bank Inventory Manager
Introduction
The Blockchain-Based Blood Bank Inventory Manager is a secure, transparent, and efficient solution for managing blood donations and transactions. By integrating blockchain technology with a streamlined inventory system, this application enhances trust, traceability, and accessibility in blood bank operations.

Features
🩸 Secure Donor Registration – Stores donor details and donation records securely.

🔗 Blockchain-Enabled Transactions – Ensures tamper-proof, verifiable transaction history.

📊 Real-Time Inventory Management – Tracks blood availability with automatic updates.

🏥 Hospital Blood Requests – Facilitates instant and verified blood transfers.

🔍 Transaction History & Traceability – Displays a transparent record of all transactions.

🖥️ User-Friendly Interface – Developed with Streamlit for easy navigation.

Technology Stack
Python – Backend logic

Streamlit – UI framework

SQLite – Database for storing blood bank data

Blockchain (SHA-256) – Ensuring secure transactions

Pandas & Matplotlib – Data visualization

Installation & Setup
Prerequisites
Ensure you have Python 3.10+ installed. Then, install the required dependencies:

sh
Copy
Edit
pip install -r requirements.txt
Initialize the Database
Run the following command to create and populate the database:

sh
Copy
Edit
python init_db.py
Run the Application
Start the Streamlit app with:

sh
Copy
Edit
streamlit run app.py
Usage
Register Donors – Add donor details and update blood inventory.

View Inventory – Check available blood stock in real-time.

Process Transactions – Hospitals can request blood units securely.

View Transaction History – Blockchain-based records for transparency.

Project Structure
bash
Copy
Edit
📂 Blockchain-BloodBank
│── 📄 app.py               # Main application
│── 📄 init_db.py           # Database initialization
│── 📄 requirements.txt     # Required dependencies
│── 📄 README.md            # Project documentation
│── 📂 database/            # SQLite database files
│── 📂 assets/              # UI and visualization resources
Security & Blockchain Implementation
Each transaction generates a unique hash (SHA-256) to maintain integrity.

Transactions are linked via previous hashes, forming a blockchain.

Prevents fraud, double spending, and unauthorized modifications.

Contributing
Contributions are welcome! Follow these steps:

Fork the repository.

Create a branch (git checkout -b feature-name).

Commit changes (git commit -m "Description").

Push to branch (git push origin feature-name).

Create a Pull Request.

License
This project is open-source under the MIT License.

Contact
For queries, feel free to reach out or open an issue! 🚀
