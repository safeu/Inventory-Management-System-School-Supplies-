from flask import redirect, request, Blueprint, render_template, url_for, flash
from app.services.transaction_service import (
    restock, sale, get_all_transactions, get_recent_transactions)

transaction = Blueprint('transaction', __name__, url_prefix='/transactions')

@transaction.route('/', methods=['GET'])
def get_transactions():
    success, transactions = get_all_transactions()
    if success:
        return render_template('transactions.html', transactions=transactions)
    else:
        flash(f"Error fetching transactions: {transactions}", 'error')
        return render_template('transactions.html', transactions=[])

@transaction.route('/restock', methods=['GET','POST'])
def restock_item():
    if request.method == 'POST':
        item_id = int(request.form.get('item_id'))
        quantity = int(request.form.get('quantity'))
        unit_price = float(request.form.get('unit_price'))
        success, message = restock(item_id, quantity, unit_price)
        if success:
            flash('Restock successful!', 'success')
            return redirect(url_for('transaction.get_transactions'))
        else:
            flash(f"Error processing restock: {message}", 'error')
    return render_template('restock.html')

@transaction.route('/sale', methods=['GET','POST'])
def sale_item():
    if request.method == 'POST':
        item_id = int(request.form.get('item_id'))
        quantity = int(request.form.get('quantity'))
        unit_price = float(request.form.get('unit_price'))
        success, message = sale(item_id, quantity, unit_price)
        if success:
            flash('Sale successful!', 'success')
            return redirect(url_for('transaction.get_transactions'))
        else:
            flash(f"Error processing sale: {message}", 'error')
    return render_template('sale.html')
