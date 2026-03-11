from .db import get_db

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        stock_quantity INTEGER NOT NULL DEFAULT 0,
        cost_price REAL NOT NULL DEFAULT 0.0,
        selling_price REAL NOT NULL DEFAULT 0.0,
        low_stock_threshold INTEGER NOT NULL DEFAULT 10,
        category TEXT,
        unit TEXT CHECK(unit IN ('pieces', 'boxes', 'packs')),
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    db.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        transaction_type TEXT CHECK(transaction_type IN ('sale', 'restock')) NOT NULL,
        unit_price REAL NOT NULL,
        total_price REAL NOT NULL,
        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE
    )""")


    db.commit()





