import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Supabase credentials from .env
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the .env file")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Data for the Game Info sections
game_info_data = [
    {
        "section_title": "About Rainbow Six Siege",
        "content": """
        <p>Tom Clancy's Rainbow Six Siege is a tactical first-person shooter developed by Ubisoft. It focuses on highly destructive environments and unique operator abilities, demanding strategic thinking, teamwork, and precise gunplay. Unlike many traditional shooters, Siege emphasizes objective-based gameplay over simple deathmatch, making every decision and gadget deployment critical.</p>
        <p>Matches are typically 5v5, with one team defending an objective (like a bomb site or hostage) and the other attacking. The game features a vast roster of operators, each with distinct gadgets, weapons, and playstyles, leading to endless strategic possibilities and a steep but rewarding learning curve.</p>
        """
    },
    {
        "section_title": "Important Game Mechanics",
        "content": """
        <ul>
            <li><strong>Destructible Environments:</strong> Walls, floors, and ceilings can be breached, shot through, or reinforced. Understanding destruction is key to creating new angles or denying enemy pushes.</li>
            <li><strong>Operator Abilities & Gadgets:</strong> Each operator has a unique primary gadget and secondary gadgets (like grenades, breach charges, barbed wire). Mastering these is vital for success.</li>
            <li><strong>Preparation Phase (Defenders):</strong> Defenders have 45 seconds to reinforce walls, place gadgets, and set up defenses. Attackers use drones to gather intel.</li>
            <li><strong>Action Phase:</strong> Attackers push the objective, while defenders hold their ground. Communication and coordination are paramount.</li>
            <li><strong>Objective Modes:</strong>
                <ul>
                    <li><strong>Bomb:</strong> Attackers must plant a defuser on one of two bomb sites. Defenders must prevent the plant or defuse it.</li>
                    <li><strong>Secure Area:</strong> Attackers must secure a designated area. Defenders must prevent attackers from securing it.</li>
                    <li><strong>Hostage:</strong> Attackers must extract a hostage. Defenders must prevent the extraction.</li>
                </ul>
            </li>
            <li><strong>Sound:</strong> Footsteps, reloads, gadget deployment – sound cues are incredibly important for intel and anticipating enemy movements.</li>
            <li><strong>One-Shot Headshots:</strong> A headshot with any weapon is an instant kill, regardless of armor, making precision aiming crucial.</li>
        </ul>
        """
    },
    {
        "section_title": "Recommended Content Creators",
        "content": """
        <p>To deepen your understanding and enjoy high-level gameplay, check out these creators:</p>
        <ul>
            <li><strong>Macie Jay:</strong> Known for his high-level gameplay, unique strategies, and calm commentary. Great for learning advanced tactics.
                <a href="https://www.youtube.com/MacieJay" target="_blank">YouTube Channel</a></li>
            <li><strong>Get_Flanked:</strong> Provides excellent guides, operator breakdowns, and meta analysis. Perfect for understanding game changes and operator roles.
                <a href="https://www.youtube.com/GetFlanked" target="_blank">YouTube Channel</a></li>
            <li><strong>VarsityGaming:</strong> Offers educational content, including "Copper to Diamond" series and detailed explanations of game mechanics. Very helpful for improving your rank.
                <a href="https://www.youtube.com/VarsityGaming" target="_blank">YouTube Channel</a></li>
        </ul>
        """
    },
    {
        "section_title": "Easy Operators to Start Playing",
        "content": """
        <p>For new players, focusing on simple, impactful operators can help you learn the ropes without being overwhelmed by complex gadgets:</p>
        <ul>
            <li><strong>Attackers:</strong>
                <ul>
                    <li><strong>Sledge:</strong> Simple and effective soft destruction. Great for learning map layouts and vertical play.</li>
                    <li><strong>Ash:</strong> Fast-paced entry fragger with breaching rounds. Good for aggressive pushes and learning gunfights.</li>
                    <li><strong>Thatcher:</strong> Essential support for hard breachers. Learn to counter defender utility without complex mechanics.</li>
                </ul>
            </li>
            <li><strong>Defenders:</strong>
                <ul>
                    <li><strong>Rook:</strong> Place armor plates at the start of the round. Simple, yet provides huge team utility.</li>
                    <li><strong>Doc:</strong> Heal yourself or teammates with a stim pistol. Great for holding angles and self-sustain.</li>
                    <li><strong>Jäger:</strong> Place ADS gadgets to destroy grenades. Simple anti-utility that benefits the whole team.</li>
                </ul>
            </li>
        </ul>
        """
    },
    {
        "section_title": "General Tips for New Players",
        "content": """
        <ul>
            <li><strong>Drone, Drone, Drone:</strong> Always use your drones to scout ahead, gather intel, and clear rooms before entering.</li>
            <li><strong>Sound is Key:</strong> Wear headphones and pay attention to footsteps, reloads, and gadget sounds. They provide crucial information.</li>
            <li><strong>Think About Secondary Gadgets:</strong> Don't forget your secondary gadgets (e.g., frag grenades, breach charges, barbed wire). They are just as important as your primary ability.</li>
            <li><strong>Communication:</strong> Call out enemy positions, gadget placements, and your plans to your teammates. Even simple calls are better than none.</li>
            <li><strong>Learn Map Layouts:</strong> Familiarize yourself with maps in custom games or Terrorist Hunt. Knowing common angles, breach points, and rotations is vital.</li>
            <li><strong>Reinforce Smartly:</strong> Don't reinforce between bomb sites unless specifically instructed. Reinforce exterior walls and key choke points.</li>
            <li><strong>Don't Be Afraid to Die:</strong> Every death is a learning opportunity. Analyze what went wrong and how you can improve.</li>
        </ul>
        """
    },
    {
        "section_title": "About the Developers & Future",
        "content": """
        <p>Rainbow Six Siege is developed by <strong>Ubisoft Montreal</strong>. It first launched on <strong>December 1, 2015</strong>. Since its release, the game has undergone continuous development, with numerous seasonal updates introducing new operators, maps, and gameplay changes.</p>
        <p>Ubisoft has committed to a long-term future for Siege. While details about "Siege X" are still emerging, it represents the ongoing evolution and expansion of the game, likely bringing new content, features, and possibly a new engine or significant graphical updates to keep the game fresh and competitive for years to come.</p>
        """
    }
]

def populate_game_info_table():
    try:
        print("Attempting to delete existing game info sections...")
        # Delete all existing entries to ensure a clean re-population
        delete_response = supabase.table('game_info').delete().neq('id', 0).execute()
        print(f"Deleted {len(delete_response.data)} existing game info sections.")

        print("Attempting to insert new game info data...")
        insert_response = supabase.table('game_info').insert(game_info_data).execute()
        print(f"Successfully inserted {len(insert_response.data)} game info sections.")
        # print(f"Inserted data: {insert_response.data}") # Uncomment to see the inserted data

    except Exception as e:
        print(f"An error occurred during population: {e}")
        print("Please ensure your 'game_info' table exists in Supabase and has 'section_title' (STRING) and 'content' (TEXT) columns.")

if __name__ == "__main__":
    populate_game_info_table()
