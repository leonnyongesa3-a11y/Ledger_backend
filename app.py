from flask import Flask, jsonify
from config import Config
from extensions import db, migrate, jwt, cors

# Import blueprints 
from routes.auth import auth_bp
from routes.transactions import transactions_bp
from routes.categories import categories_bp
from routes.budgets import budgets_bp
from routes.savings import savings_bp
from routes.dashboard import dashboard_bp


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Enable CORS for your React frontend
    cors.init_app(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:5173"
                ]
            }
        }
    )

    # Home route
    @app.route("/")
    def home():
        return jsonify({
            "message": "Ledger Finance API",
            "status": "Running"
        }), 200

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(transactions_bp, url_prefix="/api/transactions")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(budgets_bp, url_prefix="/api/budgets")
    app.register_blueprint(savings_bp, url_prefix="/api/savings")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
