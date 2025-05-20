# app.py

from flask import Flask, jsonify
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
# Import the Blueprint from routes.py
# This import should be absolute from the project root perspective when Gunicorn runs 'app:app'
from routes import main as main_blueprint

# Register the blueprint with the app instance
app.register_blueprint(main_blueprint)
# --- End Import and Register ---


# --- API Endpoint for Map Sites (Moved from routes.py for simplicity, can be in blueprint) ---
# This is a placeholder for your actual API endpoint for map sites
# It should ideally fetch from your database based on the map name
@app.route('/api/map-sites/<map_name>')
def get_map_sites(map_name):
    # In a real application, you'd fetch this from your database
    # For now, a mock data structure
    mock_map_data = {
        "Bank": ["Vault", "Open Area - Teller", "Archives - Server", "CEO Office"],
        "Oregon": ["Kitchen", "Kids Bedroom", "Basement"], # Simplified for example
        "Coastline": ["Hookah Lounge / Billiards Room", "Blue Bar / Sunrise Bar", "Penthouse / Theater"],
        "Kafe Dostoyevsky": ["Reading Room / Fireplace Hall", "Mining Room / Dining Room", "Kitchen / Bake Shop"],
        "Kanal": ["Secure Containers / Boats", "Server Room / Kayak", "Coast Guard Office / Lounge"],
        "Villa": ["Living Room / Bar", "Dining Room / Kitchen", "Classic Room / Games Room", "Statuary Room / Vault"],
        # Add more maps and their sites as needed
    }
    sites = mock_map_data.get(map_name, [])
    return jsonify(sites=sites)


# This block runs when you execute `python app.py` directly (for local development)
if __name__ == '__main__':
    print("Attempting to run Flask app...")
    app.run(debug=True)
