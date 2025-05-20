import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the .env file")

# Initialize Supabase client (using supabase-py for population is fine)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Data for the 20 original R6 Siege operators with expanded attributes
operators_data = [
    # Attackers (10)
    {
        "name": "Sledge", "side": "Attacker", "ability": "Tactical Breaching Hammer",
        "secondary_gadgets": "Frag Grenades, Stun Grenades", "armor": 2, "speed": 2,
        "role": "Soft Breacher, Entry Support",
        "short_bio": "Sledge excels at quick, quiet destruction of soft surfaces, opening new lines of sight or pathways. His hammer is reusable and effective against barricades and unreinforced walls.",
        "synergy_examples": "Thatcher, Thermite", "counter_examples": "Castle", "solo_friendly": True
    },
    {
        "name": "Thatcher", "side": "Attacker", "ability": "EMP Grenades",
        "secondary_gadgets": "Claymore, Breach Charges", "armor": 2, "speed": 2,
        "role": "Support, Anti-Gadget",
        "short_bio": "Thatcher's EMPs disable all electronic gadgets in their radius, clearing the way for hard breachers and entry fraggers. He is essential for dealing with electrified walls and defender utility.",
        "synergy_examples": "Thermite, Hibana", "counter_examples": "Mute, Bandit, Jäger", "solo_friendly": False
    },
    {
        "name": "Ash", "side": "Attacker", "ability": "Breaching Rounds",
        "secondary_gadgets": "Breach Charges, Stun Grenades", "armor": 1, "speed": 3,
        "role": "Entry Fragger, Soft Breacher",
        "short_bio": "Ash is a fast-paced operator designed for aggressive entry and rapid wall destruction. Her breaching rounds can destroy barricades, unreinforced walls, and deployable shields from a distance.",
        "synergy_examples": "Zofia, Nomad", "counter_examples": "Jäger, Wamai", "solo_friendly": True
    },
    {
        "name": "Thermite", "side": "Attacker", "ability": "Exothermic Charge",
        "secondary_gadgets": "Claymore, Smoke Grenades", "armor": 2, "speed": 2,
        "role": "Hard Breacher, Support",
        "short_bio": "Thermite is the quintessential hard breacher, capable of destroying reinforced walls and hatches. His charges are loud and require a clear path, often needing Thatcher's support to be effective.",
        "synergy_examples": "Thatcher, Maverick", "counter_examples": "Bandit, Kaid, Mute", "solo_friendly": False
    },
    {
        "name": "Twitch", "side": "Attacker", "ability": "Shock Drone",
        "secondary_gadgets": "Breach Charges, Smoke Grenades", "armor": 2, "speed": 2,
        "role": "Utility Clear, Intel",
        "short_bio": "Twitch uses specialized drones that can disable or destroy electronic gadgets with tasers, or annoy defenders. She starts with two drones, one for prep phase and one for action phase.",
        "synergy_examples": "Any hard breacher", "counter_examples": "Mute, Jäger", "solo_friendly": True
    },
    {
        "name": "Montagne", "side": "Attacker", "ability": "Extendable Shield",
        "secondary_gadgets": "Smoke Grenades, Hard Breach Charge", "armor": 3, "speed": 1,
        "role": "Front-line Support, Intel, Plant Denial",
        "short_bio": "Montagne is a powerful shield operator who can extend his shield to provide full body protection, blocking enemy fire and intel. He is excellent for blocking lines of sight and covering teammates for plants.",
        "synergy_examples": "Fuze, Smoke", "counter_examples": "Oryx, Smoke, Ela", "solo_friendly": False
    },
    {
        "name": "Glaz", "side": "Attacker", "ability": "Flip Sight",
        "secondary_gadgets": "Smoke Grenades, Claymore", "armor": 2, "speed": 2,
        "role": "Overwatch, Support, Plant Denial",
        "short_bio": "Glaz is a marksman whose unique thermal scope highlights enemies through smoke and poor visibility. He excels at holding long angles and providing cover fire, especially during plants or pushes through smoke.",
        "synergy_examples": "Smoke, Montagne", "counter_examples": "Wamai, Jäger", "solo_friendly": True
    },
    {
        "name": "Fuze", "side": "Attacker", "ability": "Cluster Charge",
        "secondary_gadgets": "Smoke Grenades, Breach Charges", "armor": 3, "speed": 1,
        "role": "Area Denial, Utility Clear, Crowd Control",
        "short_bio": "Fuze can deploy a cluster charge on destructible surfaces, shooting grenades into the room on the other side. This is highly effective for clearing defender gadgets or flushing out enemies, but carries a risk to teammates.",
        "synergy_examples": "Montagne, Blitz", "counter_examples": "Jäger, Wamai, Mute", "solo_friendly": False
    },
    {
        "name": "Blitz", "side": "Attacker", "ability": "Flash Shield",
        "secondary_gadgets": "Smoke Grenades, Breach Charges", "armor": 3, "speed": 1, # Blitz was 3A/1S at launch
        "role": "Entry Fragger, Crowd Control",
        "short_bio": "Blitz is a shield operator focused on aggressive pushes, capable of blinding enemies with a powerful flash mounted on his shield. He is excellent for close-quarters combat and disrupting defender positions.",
        "synergy_examples": "Montagne, Fuze", "counter_examples": "Oryx, Smoke, Lesion", "solo_friendly": True
    },
    {
        "name": "IQ", "side": "Attacker", "ability": "Electronics Detector",
        "secondary_gadgets": "Breach Charges, Frag Grenades", "armor": 1, "speed": 3, # IQ was 1A/3S at launch
        "role": "Intel, Utility Clear",
        "short_bio": "IQ uses a wrist-mounted device to detect all electronic gadgets through walls, providing crucial intel for her team to clear defender utility or track enemies.",
        "synergy_examples": "Thatcher, Thermite, Kali", "counter_examples": "Mute", "solo_friendly": True
    },
    # Defenders (10)
    {
        "name": "Smoke", "side": "Defender", "ability": "Remote Gas Grenade",
        "secondary_gadgets": "Barbed Wire, Deployable Shield", "armor": 2, "speed": 2,
        "role": "Area Denial, Plant Denial, Anchor",
        "short_bio": "Smoke can deploy toxic gas grenades that damage and disorient enemies, making him excellent for blocking entryways, denying plants, or flushing out attackers in the final seconds of a round.",
        "synergy_examples": "Jäger, Maestro", "counter_examples": "IQ, Thatcher", "solo_friendly": True
    },
    {
        "name": "Mute", "side": "Defender", "ability": "Signal Disruptor",
        "secondary_gadgets": "Nitro Cell, Barbed Wire", "armor": 2, "speed": 2,
        "role": "Anti-Breach, Intel Denial, Anchor",
        "short_bio": "Mute's jammers block drones, breach charges, and other electronic gadgets in their radius, essential for fortifying sites against hard breachers and denying intel.",
        "synergy_examples": "Bandit, Kaid, Castle", "counter_examples": "Thatcher, Twitch, IQ", "solo_friendly": True
    },
    {
        "name": "Castle", "side": "Defender", "ability": "Armored Panels",
        "secondary_gadgets": "Deployable Shield, Impact Grenades", "armor": 2, "speed": 2,
        "role": "Roaming Denier, Entry Denier",
        "short_bio": "Castle deploys impenetrable armored panels over doors and windows, creating strong barriers that force attackers to use breach charges or Sledge's hammer, slowing down their push.",
        "synergy_examples": "Mute, Pulse", "counter_examples": "Sledge, Ash, Zofia, Maverick", "solo_friendly": False
    },
    {
        "name": "Pulse", "side": "Defender", "ability": "Heartbeat Sensor",
        "secondary_gadgets": "Nitro Cell, Barbed Wire", "armor": 2, "speed": 2,
        "role": "Intel, Roamer, Flanker",
        "short_bio": "Pulse uses a heartbeat sensor to detect enemies through walls, providing invaluable real-time intel on their positions. He is excellent for anticipating pushes, flanking, or playing vertical angles.",
        "synergy_examples": "Valkyrie, Mute", "counter_examples": "IQ, Thatcher", "solo_friendly": True
    },
    {
        "name": "Doc", "side": "Defender", "ability": "Stim Pistol",
        "secondary_gadgets": "Barbed Wire, Deployable Shield", "armor": 3, "speed": 1,
        "role": "Healer, Anchor, Self-Sustain",
        "short_bio": "Doc can revive downed teammates from a distance or heal himself and allies, increasing their survivability. He is a strong anchor who can hold angles and sustain himself through engagements.",
        "synergy_examples": "Rook", "counter_examples": "Zofia", "solo_friendly": True
    },
    {
        "name": "Rook", "side": "Defender", "ability": "Armor Pack",
        "secondary_gadgets": "Impact Grenades, Deployable Shield", "armor": 3, "speed": 1,
        "role": "Support, Anchor, Durability",
        "short_bio": "Rook provides his team with deployable armor packs that increase their damage resistance and guarantee a downed state instead of instant death, significantly boosting team survivability.",
        "synergy_examples": "Doc", "counter_examples": "Ash, Zofia", "solo_friendly": True
    },
    {
        "name": "Kapkan", "side": "Defender", "ability": "Entry Denial Device (EDD)",
        "secondary_gadgets": "Impact Grenades, Nitro Cell", "armor": 3, "speed": 1, # Kapkan was 3A/1S at launch
        "role": "Trap, Entry Denier",
        "short_bio": "Kapkan sets invisible booby traps on doorways and windows, which explode when triggered by an attacker. His traps are highly effective at inflicting damage and denying entry.",
        "synergy_examples": "Lesion, Frost", "counter_examples": "Thatcher, Twitch, IQ", "solo_friendly": True
    },
    {
        "name": "Tachanka", "side": "Defender", "ability": "Mounted LMG", # Original launch gadget
        "secondary_gadgets": "Barbed Wire, Deployable Shield", "armor": 3, "speed": 1,
        "role": "Anchor, Area Denial (limited)",
        "short_bio": "Tachanka's original gadget was a deployable heavy machine gun, offering immense firepower but making him a stationary target. He was typically used to hold tight angles or suppress entry points.",
        "synergy_examples": "Maestro, Montagne", "counter_examples": "Glaz, Ash, Thermite", "solo_friendly": False
    },
    {
        "name": "Jäger", "side": "Defender", "ability": "Active Defense System (ADS)",
        "secondary_gadgets": "Barbed Wire, Deployable Shield", "armor": 1, "speed": 3, # Jäger was 1A/3S at launch
        "role": "Anti-Grenade, Roamer Support",
        "short_bio": "Jäger's ADS gadgets intercept and destroy incoming projectiles like grenades, flashes, and smokes, protecting important areas or teammates. He is crucial for denying attacker utility.",
        "synergy_examples": "Wamai", "counter_examples": "Thatcher, IQ", "solo_friendly": True
    },
    {
        "name": "Bandit", "side": "Defender", "ability": "Shock Wire",
        "secondary_gadgets": "Nitro Cell, Barbed Wire", "armor": 1, "speed": 3, # Bandit was 1A/3S at launch
        "role": "Anti-Hard Breach, Roamer",
        "short_bio": "Bandit places electrically charged barbed wire or reinforced walls that destroy attacker gadgets attempting to breach them. He is essential for denying hard-breach attempts on critical walls.",
        "synergy_examples": "Mute, Kaid", "counter_examples": "Thatcher, Twitch, IQ", "solo_friendly": True
    },
]

def populate_operators_table():
    try:
        print("Attempting to insert new operator data...")
        insert_response = supabase.table('operators').insert(operators_data).execute()
        print(f"Successfully inserted {len(insert_response.data)} operators.")

    except Exception as e:
        print(f"An error occurred during population: {e}")
        print("Please ensure your 'operators' table exists in Supabase and has ALL the required columns.")

if __name__ == "__main__":
    populate_operators_table()
