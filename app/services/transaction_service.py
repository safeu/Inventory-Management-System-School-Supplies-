from app.db import get_db
import logging
from app.services.inventory_service import get_item_by_id

logger = logging.getLogger(__name__)

def restock(item_id, quantity, unit_price):
    try:
        db = get_db()
        success, item = get_item_by_id(item_id)
        if not item:
            raise ValueError(f"Item not found with ID {item_id}")

        new_stock = item['stock_quantity'] + quantity
        db.execute("UPDATE items SET stock_quantity = ? WHERE id = ?", (new_stock, item_id))
        total_price = quantity * unit_price
        db.execute("""
            INSERT INTO transactions (item_id, quantity, transaction_type, unit_price, total_price)
            VALUES (?, ?, 'restock', ?, ?)
        """, (item_id, quantity, unit_price, total_price))
        db.commit()
        return True, "Restock successful"

    except Exception as e:
        db.rollback()
        logger.error(f"Error processing restock: {e}")
        return False, str(e)
    
def sale(item_id, quantity, unit_price):
    try:
        db = get_db()
        success, item = get_item_by_id(item_id)
        if not item:
            raise ValueError(f"Item not found with ID {item_id}")
        if item['stock_quantity'] < quantity:
            raise ValueError("Insufficient stock for sale")

        new_stock = item['stock_quantity'] - quantity
        db.execute("UPDATE items SET stock_quantity = ? WHERE id = ?", (new_stock, item_id))
        total_price = quantity * unit_price
        db.execute("""
            INSERT INTO transactions (item_id, quantity, transaction_type, unit_price, total_price)
            VALUES (?, ?, 'sale', ?, ?)
        """, (item_id, quantity, unit_price, total_price))
        db.commit()
        return True, "Sale successful"

    except Exception as e:
        db.rollback()
        logger.error(f"Error processing sale: {e}")
        return False, str(e)
    

def get_all_transactions():
    try:
        db = get_db()
        transactions = db.execute("SELECT * FROM transactions").fetchall()
        return True, transactions
    except Exception as e:
        logger.error(f"Error fetching transactions: {e}")
        return False, str(e)
    
def get_transaction_by_id(transaction_id):
    try:
        db = get_db()
        transaction = db.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,)).fetchone()
        return True, transaction
    except Exception as e:
        logger.error(f"Error fetching transaction by id: {e}")
        return False, str(e)

def get_transactions_by_item(item_id):
    try:
        db = get_db()
        transactions = db.execute("SELECT * FROM transactions WHERE item_id = ?", (item_id,)).fetchall()
        return True, transactions
    except Exception as e:
        logger.error(f"Error fetching transactions by item id: {e}")
        return False, str(e)

def get_recent_transactions(limit=10):
    try:
        db = get_db()
        transactions = db.execute("SELECT * FROM transactions ORDER BY transaction_date DESC LIMIT ?", (limit,)).fetchall()
        return True, transactions
    except Exception as e:
        logger.error(f"Error fetching recent transactions: {e}")
        return False, str(e)
    
def get_transactions_by_type(transaction_type):
    try:
        db = get_db()
        transactions = db.execute("SELECT * FROM transactions WHERE transaction_type = ?", (transaction_type,)).fetchall()
        return True, transactions
    except Exception as e:
        logger.error(f"Error fetching transactions by type: {e}")
        return False, str(e)

def get_transactions_by_date_range(start_date, end_date):
    try:
        db = get_db()
        transactions = db.execute("""
            SELECT * FROM transactions 
            WHERE transaction_date BETWEEN ? AND ?""", (start_date, end_date)).fetchall()
        return True, transactions
    except Exception as e:
        logger.error(f"Error fetching transactions by date range: {e}")
        return False, str(e)