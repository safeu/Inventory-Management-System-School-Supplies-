# School Supplies Inventory Management 

A full-stack web application built with Python, Flask, and SQLite to manage school supplies inventory — inspired by the inefficiencies of manually tracking stock through Excel spreadsheets.

## Features 

- 📦 **Inventory Management** — Add, update, and delete inventory items with stock tracking
- 📊 **Dashboard** — Real-time overview of inventory value, low stock alerts, and recent transactions
- 🔄 **Transaction Tracking** — Record sales and restocks with full transaction history
- ⚠️ **Low Stock Alerts** — Automatic detection of items below configurable stock thresholds
- 📁 **Bulk CSV Import** — Import multiple inventory items at once via CSV file upload

## Tech Stack

- **Backend** — Python, Flask
- **Database** — SQLite3
- **Frontend** — HTML, Bootstrap 5
- **Architecture** — MVC pattern with service layer separation

## Project Structure
```
app/
├── routes/
│   ├── dashboard_routes.py
│   ├── inventory_routes.py
│   └── transaction_routes.py
├── services/
│   ├── inventory_service.py
│   └── transaction_service.py
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── inventory.html
│   ├── add_item.html
│   ├── update_item.html
│   ├── transactions.html
│   ├── restock.html
│   ├── sale.html
│   └── import_csv.html
├── __init__.py
├── db.py
├── models.py
└── settings.py
run.py
requirements.txt
```

## Getting Started

### Prerequisites
- Python 3.11+
- pip

### Installation

1. Clone the repository
```bash
git clone 
cd inventory-management
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python run.py
```

4. Open your browser and go to
```
http://localhost:5000
```

## CSV Import Format

To bulk import inventory items, upload a CSV file with the following headers:
```
name, stock_quantity, price, low_stock_threshold, category, unit
Pencils, 100, 0.50, 10, Stationery, pieces
Notebooks, 50, 2.00, 5, Paper, packs
```
## Motivation

 Previously managed inventory for family school supplies retail business using Excel spreadsheets - a process that was tedious and very prone to human error. This project was built to replace that workflow with a proper structured system featuring automated alerts and a clean dashboard interface.