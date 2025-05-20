import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 5 R6 Siege maps into DB
maps_data = [
    {
        "name": "Oregon",
        "image_url": "/static/images/maps/oregon.jpg",
        "defender_sites": "Kitchen, Kids Bedroom, Basement",
        "electricity_needed": True,
        "description": "A classic, compact map with distinct verticality, often featuring tense basement defenses. Known for its strong choke points and destructible floors."
    },
    {
        "name": "Coastline",
        "image_url": "/static/images/maps/coastline.jpg",
        "defender_sites": "Hookah Lounge / Billiards Room, Blue Bar / Sunrise Bar, Penthouse / Theater",
        "electricity_needed": False, # More soft walls than hard walls
        "description": "A vibrant, luxurious club in Ibiza, characterized by its soft-breachable walls, open design, and numerous entry points. Favors aggressive play."
    },
    {
        "name": "Kafe Dostoyevsky",
        "image_url": "/static/images/maps/kafe_dostoyevsky.jpg",
        "defender_sites": "Reading Room / Fireplace Hall, Mining Room / Dining Room, Kitchen / Bake Shop",
        "electricity_needed": True,
        "description": "A grand, multi-floor cafe in Moscow, demanding strong vertical play and solid site defenses. Features many hard-breachable walls and tight corridors."
    },
    {
        "name": "Kanal",
        "image_url": "/static/images/maps/kanal.jpg",
        "defender_sites": "Secure Containers / Boats, Server Room / Kayak, Coast Guard Office / Lounge",
        "electricity_needed": False, # More about denying lines of sight and rushes
        "description": "Divided by a canal, requiring unique rotation strategies and often a strong outside presence. Features a mix of hard and soft walls, with bridges connecting the two buildings."
    },
    {
        "name": "Villa",
        "image_url": "/static/images/maps/villa.jpg",
        "defender_sites": "Living Room / Bar, Dining Room / Kitchen, Classic Room / Games Room, Statuary Room / Vault",
        "electricity_needed": True, # Many exterior walls often crucial
        "description": "A lavish Italian villa known for its complex layouts and multiple entry points. Requires coordinated defense to cover its numerous angles and breach points."
    },
]

def populate_maps_table():
    try:
        response = supabase.table('maps').insert(maps_data).execute()
        print(f"Successfully inserted {len(response.data)} maps.")
        print(f"Inserted data: {response.data}")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure your 'maps' table exists in Supabase and has the correct columns.")

if __name__ == "__main__":
    populate_maps_table()