from flask import redirect, request, Blueprint, render_template, url_for, flash
from app.services.inventory_service import (
    get_all_items, add_item, get_item_by_id, update_item, delete_item, add_bulk_items
)
import csv
import io


inventory = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory.route('/', methods=['GET', 'POST'])
def get_all_inventory():
    success, items = get_all_items()
    if not success:
        flash(f"Error fetching inventory: {items}", 'error')
        items = []
    return render_template('inventory.html', items=items)

@inventory.route('/add', methods=['GET', 'POST'])
def add_inventory():
    if request.method == 'POST':
        name = request.form.get('name')
        stock_quantity = int(request.form.get('stock_quantity', 0))
        price = float(request.form.get('price', 0.0))
        low_stock_threshold = int(request.form.get('low_stock_threshold', 10))
        category = request.form.get('category')
        unit = request.form.get('unit')

        success, message = add_item(name, stock_quantity, price, low_stock_threshold, category, unit)
        if success:
            flash('Item added successfully!', 'success')
            return redirect(url_for('inventory.get_all_inventory'))
        else:
            flash(f"Error adding item: {message}", 'error')

    return render_template('add_item.html')

@inventory.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update_inventory(item_id):
    success, item = get_item_by_id(item_id)
    if not item:
        flash(f"Item with id {item_id} not found", 'error')
        return redirect(url_for('inventory.get_all_inventory'))

    if request.method == 'POST':
        name = request.form.get('name')
        stock_quantity = int(request.form.get('stock_quantity', item['stock_quantity']))
        price = float(request.form.get('price', item['price']))
        low_stock_threshold = int(request.form.get('low_stock_threshold', item['low_stock_threshold']))
        category = request.form.get('category', item['category'])
        unit = request.form.get('unit', item['unit'])

        success, message = update_item(item_id, name=name, stock_quantity=stock_quantity, price=price, low_stock_threshold=low_stock_threshold, category=category, unit=unit)
        if success:
            flash('Item updated successfully!', 'success')
            return redirect(url_for('inventory.get_all_inventory'))
        else:
            flash(f"Error updating item: {message}", 'error')

    return render_template('update_item.html', item=item, units=['pieces', 'boxes', 'packs'])


@inventory.route('/delete/<int:item_id>', methods=['POST'])
def delete_inventory(item_id):
    success, message = delete_item(item_id)
    if success:
        flash("Item deleted successfully", 'success')
    else:
        flash(f"Error deleting item: {message}", 'error')
    return redirect(url_for('inventory.get_all_inventory'))


@inventory.route('/import', methods=['GET','POST'])
def import_inventory():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash("No file uploaded", 'error')
            return redirect(url_for('inventory.get_all_inventory'))

        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.DictReader(stream)
        items = [row for row in reader]


        success, message = add_bulk_items(items)
        if success:
            flash("Inventory imported successfully", 'success')
            return redirect(url_for('inventory.get_all_inventory'))
        else:
            flash(f"Error importing inventory: {message}", 'error')

    return render_template('import_csv.html')