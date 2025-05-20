# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables from .env file as early as possible
load_dotenv()

# Create the Flask application instance
app = Flask(__name__)

# --- Database Configuration ---
DB_USER = os.getenv('user')
DB_PASSWORD = os.getenv('password')
DB_HOST = os.getenv('host')
DB_PORT = os.getenv('port')
DB_NAME = os.getenv('dbname')

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    print("Error: Crucial database environment variables are not fully set.")
    print("Ensure user, password, host, port, and dbname are in your .env file.")
    raise EnvironmentError("Required database connection details missing from environment variables.")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)
# --- End Database Configuration ---

# --- Import and Register Blueprints ---
# Import the Blueprint from routes.py using a relative import
# This is correct when the project is treated as a package (due to __init__.py)
from .routes import main as main_blueprint

# Register the blueprint with the app instance
app.register_blueprint(main_blueprint)
# --- End Import and Register ---


# This block runs when you execute `python app.py` directly (for local development)
if __name__ == '__main__':
    print("Attempting to run Flask app locally...")
    app.run(debug=True)
