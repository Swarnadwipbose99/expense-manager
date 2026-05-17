# run.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from expense_manager.app import create_app, db

config = os.getenv("FLASK_CONFIG", "expense_manager.config.DevelopmentConfig")
app = create_app(config)

# Auto-create tables (safe to run every startup — CREATE TABLE IF NOT EXISTS)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=app.config["DEBUG"])
