from app.db import get_db
import logging

logger = logging.getLogger(__name__)

def get_all_items():
    try:
        db = get_db()
        items = db.execute("SELECT * FROM items").fetchall()
        return True, items
    except Exception as e:
        logger.error(f"Error fetching items: {e}")
        return False, str(e)

def get_item_by_id(item_id):
    try:
        db = get_db()
        item = db.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        return True, item
    except Exception as e:
        logger.error(f"Error fetching item by id: {e}")
        return False, str(e)

def add_item(name, stock_quantity, cost_price, selling_price=None, low_stock_threshold=10, category=None, unit=None):
    try:
        db = get_db()
        if not selling_price:
            selling_price = cost_price * 2
        db.execute("""
            INSERT INTO items (name, stock_quantity, cost_price, selling_price, low_stock_threshold, category, unit)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, stock_quantity, cost_price, selling_price, low_stock_threshold, category, unit))
        db.commit()
        return True, db.execute("SELECT last_insert_rowid()").fetchone()[0]
    except Exception as e:
        logger.error(f"Error adding item: {e}")
        return False, str(e)

def add_bulk_items(items):
    try:
        db = get_db()
        items_data = []
        for item in items:
            selling_price = item.get('selling_price') or float(item['cost_price']) * 2
            items_data.append((
                item['name'],
                item['stock_quantity'],
                item['cost_price'],
                selling_price,
                item.get('low_stock_threshold', 10),
                item.get('category'),
                item.get('unit')))

        db.executemany("""
            INSERT INTO items (name, stock_quantity, cost_price, selling_price, low_stock_threshold, category, unit)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, items_data)
        db.commit()
        return True, len(items_data)
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding bulk items: {e}")
        return False, str(e)

def update_item(item_id, **kwargs):
    try:
        db = get_db()

        success, item = get_item_by_id(item_id)
        if not item:
            raise ValueError(f"Item with id {item_id} not found")

        allowed = {'name', 'stock_quantity', 'cost_price', 'selling_price', 'low_stock_threshold', 'category', 'unit'}
        fields = {k: v for k, v in kwargs.items() if k in allowed}
        if not fields:
            raise ValueError("No valid fields to update")
        
        set_clause = ", ".join([f"{k} = ?" for k in fields.keys()])
        values = list(fields.values()) + [item_id]
        db.execute(f"UPDATE items SET {set_clause} WHERE id = ?", values)
        db.commit()

        success, updated_item = get_item_by_id(item_id)
        return True, updated_item
    except Exception as e:
        logger.error(f"Error updating item: {e}")
        return False, str(e)

def get_low_stock_items():
    try:
        db = get_db()
        items = db.execute("SELECT * FROM items WHERE stock_quantity <= low_stock_threshold").fetchall()
        return True, items
    except Exception as e:
        logger.error(f"Error fetching low stock items: {e}")
        return False, str(e)

def out_of_stock_items():
    try:
        db = get_db()
        items = db.execute("SELECT * FROM items WHERE stock_quantity <= 0").fetchall()
        return True, items
    except Exception as e:
        logger.error(f"Error fetching out of stock items: {e}")
        return False, str(e)

def delete_item(item_id):
    try:
        db = get_db()
        success, item = get_item_by_id(item_id)
        if not item:
            raise ValueError(f"Item with id {item_id} not found")
        db.execute("DELETE FROM items WHERE id = ?", (item_id,))
        db.commit()

        return True, f"Item with id {item_id} deleted"
    except Exception as e:
        logger.error(f"Error deleting item: {e}")
        return False, str(e)

def search_items(query):
    try:
        db = get_db()
        items = db.execute("SELECT * FROM items WHERE name LIKE ?", ('%' + query + '%',)).fetchall()
        return True, items
    except Exception as e:
        logger.error(f"Error searching items: {e}")
        return False, str(e)

def get_items_by_category(category):
    try:
        db = get_db()
        items = db.execute("SELECT * FROM items WHERE category = ?", (category,)).fetchall()
        return True, items
    except Exception as e:
        logger.error(f"Error fetching items by category: {e}")
        return False, str(e)

def get_total_inventory_value():
    try:
        db = get_db()
        total_value = db.execute("SELECT SUM(stock_quantity * selling_price) AS total_value FROM items").fetchone()['total_value']
        return True, total_value if total_value is not None else 0.0
    except Exception as e:
        logger.error(f"Error calculating total inventory value: {e}")
        return False, str(e)

