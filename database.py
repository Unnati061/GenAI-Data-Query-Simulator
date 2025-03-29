import sqlite3

DB_NAME = "database.db"

def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Table to store executed queries
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_text TEXT NOT NULL
        )
    """)

    # Sales data table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            month TEXT,
            region TEXT,
            product_name TEXT,
            customer_name TEXT,
            amount REAL
        )
    """)

    # Customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            region TEXT
        )
    """)

    conn.commit()
    conn.close()
    
def insert_mock_data():
    """Insert sample data into sales and customers tables for testing."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Insert mock sales data
    cursor.execute("INSERT INTO sales (date, month, region, product_name, customer_name, amount) VALUES ('2025-03-01', 'March', 'North', 'Laptop', 'Alice', 1200.50)")
    cursor.execute("INSERT INTO sales (date, month, region, product_name, customer_name, amount) VALUES ('2025-03-02', 'March', 'South', 'Phone', 'Bob', 800.00)")

    # Insert mock customer data
    cursor.execute("INSERT INTO customers (customer_name, region) VALUES ('Alice', 'North')")
    cursor.execute("INSERT INTO customers (customer_name, region) VALUES ('Bob', 'South')")

    conn.commit()
    conn.close()


insert_mock_data()


def execute_query(query, params=()):
    """Execute a query and return the results."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.commit()
        return result
    except sqlite3.Error as e:
        return {"error": str(e)}
    finally:
        conn.close()

# Initialize the database on import
init_db()
