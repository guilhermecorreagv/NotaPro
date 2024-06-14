import sqlite3 
import config 

def connect_database():
    config.db_connection = sqlite3.connect("database.db")

def setup_database():
    cur = config.db_connection.cursor()

    con = sqlite3.connect("database.db")
    cur = con.cursor()

    # Enable foreign key support
    cur.execute("PRAGMA foreign_keys = ON;")

    # Products table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Products(
            ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Description TEXT, 
            Stock INTEGER DEFAULT 0,
            Price INTEGER
        );
    """)

    # Clients table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Clients(
            ClientID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name VARCHAR(255) NOT NULL,
            ContactInfo TEXT
        );
    """)

    # Sales table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Sales(
            SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
            ProductID INTEGER NOT NULL,
            Quantity INTEGER NOT NULL,
            SaleDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CustomerID INTEGER,
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
            FOREIGN KEY (CustomerID) REFERENCES Clients(ClientID)
        );
    """)

    # Create Indices
    cur.execute("CREATE INDEX IF NOT EXISTS idx_product_name ON Products(Name);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_client_name ON Clients(Name);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sale_product ON Sales(ProductID);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sale_date ON Sales(SaleDate);")

    # Commit and close
    con.commit()



