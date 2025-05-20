# r6_fan_app/__init__.py

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
LLM_API_KEY = os.getenv('LLM_API_KEY')  # Also load LLM API Key here

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, LLM_API_KEY]):
    print("Error: Crucial environment variables are not fully set.")
    print("Ensure user, password, host, port, dbname, and LLM_API_KEY are in your .env file.")
    raise EnvironmentError("Required environment variables missing from .env or environment.")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)
# --- End Database Configuration ---

# --- Import and Register Blueprints ---
# Import the Blueprint from routes.py using a relative import
# This is correct because __init__.py and routes.py are now in the same package
from .routes import main as main_blueprint

# Register the blueprint with the app instance
app.register_blueprint(main_blueprint)
# --- End Import and Register ---

# No __name__ == '__main__': block here, as run.py handles execution.
