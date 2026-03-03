from flask import Flask
from .settings import Settings
from . import db
from .models import init_db
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Settings)
    db.init_app(app)

    from .routes.dashboard_routes import dashboard
    from .routes.inventory_routes import inventory
    from .routes.transaction_routes import transaction

    app.register_blueprint(dashboard)
    app.register_blueprint(inventory)
    app.register_blueprint(transaction)

    with app.app_context():
        init_db()

    return app

