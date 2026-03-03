from flask import render_template, Blueprint
from app.services.inventory_service import get_low_stock_items, out_of_stock_items, get_total_inventory_value
from app.services.transaction_service import get_recent_transactions


dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def index():
    success, low_stock_items = get_low_stock_items()
    success, out_of_stock = out_of_stock_items()
    success, total_value = get_total_inventory_value()
    success, recent_transactions = get_recent_transactions()
    return render_template('dashboard.html', 
                            low_stock_items=low_stock_items, 
                            out_of_stock=out_of_stock, 
                            total_value=total_value,
                            recent_transactions=recent_transactions)