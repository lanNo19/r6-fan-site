import os
from dotenv import load_dotenv
from supabase import create_client, Client
from flask import Flask, render_template, request, jsonify, redirect, url_for

# Fix the relative import: change to absolute import
from routes import main as main_blueprint # <-- CHANGED THIS LINE
from models import Operator, Map, GameInfo # Assuming these are in models.py

# Load environment variables
load_dotenv()

# Supabase credentials
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(main_blueprint)

# Add a simple route for the root URL
@app.route('/')
def index():
    # You might want to fetch some data for the homepage here if needed
    return render_template('index.html')

# This is a placeholder for your actual API endpoint for map sites
# It should ideally fetch from your database based on the map name
@app.route('/api/map-sites/<map_name>')
def get_map_sites(map_name):
    # In a real application, you'd fetch this from your database
    # For now, a mock data structure
    mock_map_data = {
        "Bank": ["Vault", "Open Area - Teller", "Archives - Server", "CEO Office"],
        "Oregon": ["Kitchen - Dining", "Dorm Main Hall - Kids", "Tower - Meeting", "Bunker - Laundry"],
        "Chalet": ["Kitchen - Dining", "Wine Cellar - Storage", "Master Bedroom - Bathroom", "Gaming Room - Bar"],
        "Consulate": ["Garage - Cafe", "Consul Office - Meeting Room", "Archives - Tellers", "Visa Office - Consulate Room"],
        "Border": ["Customs Inspection - Supply Room", "Ventilation Room - Armory", "Workshop - Bathroom", "Teller's Office - Server Room"],
        # Add more maps and their sites as needed
    }
    sites = mock_map_data.get(map_name, [])
    return jsonify(sites=sites)

if __name__ == '__main__':
    app.run(debug=True)

