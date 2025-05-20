from flask import render_template, request, jsonify, Blueprint, url_for
from .app import db
from .models import Operator, Map, GameInfo
import os # Import os to access environment variables for LLM API key
import google.generativeai as genai # Import the Google Gemini library
import textwrap # Useful for formatting LLM prompts
import re # Import regex for robust parsing (optional, but good for parsing LLM output)

main = Blueprint('main', __name__)
LLM_API_KEY = os.getenv('LLM_API_KEY')

if LLM_API_KEY:
    try:
        genai.configure(api_key=LLM_API_KEY)
        print("LLM API configured successfully.")
    except Exception as e:
        print(f"Error configuring LLM API: {e}")
        LLM_API_KEY = None
        print("LLM API configuration failed. LLM suggestions will not work.")
else:
    print("Warning: LLM_API_KEY environment variable not set. LLM suggestions will not work.")

def get_llm_suggestions(prompt):
    """
    Sends a prompt to the Google Gemini and returns a list of suggested operator names.
    Handles basic parsing of the LLM response.
    """
    print(f"\n--- Sending Prompt to LLM ---")
    print(prompt)
    print(f"--- End Prompt ---\n")

    if not LLM_API_KEY:
        print("LLM API key not available. Cannot get suggestions.")
        return [] # empty if LLM API KEY is missing

    suggested_names = []
    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        response = model.generate_content(prompt)

        suggested_names_raw = response.text.strip()
        print(f"LLM Raw Response: '{suggested_names_raw}'")

        # following section for robust parsing of responses

        # splitting by comma first
        potential_names = [name.strip() for name in suggested_names_raw.split(',') if name.strip()]

        # here is the fallback, if comma splitting did not work
        if not potential_names:
             potential_names = [line.strip() for line in suggested_names_raw.split('\n') if line.strip()]

        refined_names = []
        for name in potential_names:
             if re.match(r'^[A-Z][a-zA-Z\s\'-]*$', name):
                  refined_names.append(name)
             else:
                 refined_names.append(name)

        # set for getting rid of duplicates, and back to list
        suggested_names = list(set(refined_names))

        # 3 suggestions only
        final_suggestions = suggested_names[:3]
        print(f"Parsed and limited suggestions: {final_suggestions}")

        return final_suggestions

    except Exception as e:
        print(f"Error during LLM API call: {e}")
        return []

def format_operator_data_for_prompt(operators):
    """Formats a list of Operator objects into a string suitable for an LLM prompt."""
    formatted_data = "Available Operators (Name, Side, Role, Armor, Speed, Ability, Bio, Synergies, Counters, Solo Friendly):\n"
    for op in operators:
        formatted_data += textwrap.dedent(f"""
        - {op.name} ({op.side}): Role: {op.role}, {op.armor} Armor, {op.speed} Speed. Ability: {op.ability}. Bio: {op.short_bio}. Synergies: {op.synergy_examples if op.synergy_examples else 'None'}. Counters: {op.counter_examples if op.counter_examples else 'None'}. Solo Friendly: {'Yes' if op.solo_friendly else 'No'}.
        """)
    return formatted_data.strip()

def format_map_data_for_prompt(map_data):
    """Formats a Map object into a string suitable for an LLM prompt."""
    formatted_data = textwrap.dedent(f"""
    Map Name: {map_data.name}
    Map Description: {map_data.description if map_data.description else 'None'}
    Defender Sites on this map: {map_data.defender_sites if map_data.defender_sites else 'None'}
    Requires Electricity for key walls: {'Yes' if map_data.electricity_needed else 'No'}
    """)
    return formatted_data.strip()


# --- Your existing routes ---
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/operators')
def operators():
    try:
        operators_data = Operator.query.all()
        attackers = [op for op in operators_data if op.side == 'Attacker']
        defenders = [op for op in operators_data if op.side == 'Defender']
        return render_template('operators.html', attackers=attackers, defenders=defenders)
    except Exception as e:
        print(f"Error fetching operators: {e}")
        return render_template('error.html', message="Could not load operators."), 500

@main.route('/operators/<operator_name_slug>')
def operator_detail(operator_name_slug):
    operator_name = operator_name_slug.replace('-', ' ').title()
    try:
        operator_data = Operator.query.filter_by(name=operator_name).first()

        if operator_data:
            operator_data.secondary_gadgets_list = [g.strip() for g in operator_data.secondary_gadgets.split(',')] if operator_data.secondary_gadgets else []
            operator_data.synergy_list = [op.strip() for op in operator_data.synergy_examples.split(',')] if operator_data.synergy_examples else []
            operator_data.counter_list = [op.strip() for op in operator_data.counter_examples.split(',')] if operator_data.counter_examples else []

            return render_template('operator_detail.html', operator=operator_data)
        else:
            return render_template('error.html', message=f"Operator '{operator_name}' not found."), 404
    except Exception as e:
        print(f"Error fetching operator detail for {operator_name}: {e}")
        return render_template('error.html', message="Could not load operator details."), 500

@main.route('/maps')
def maps_list():
    try:
        maps = Map.query.all()
        return render_template('maps.html', maps=maps)
    except Exception as e:
        print(f"Error fetching maps: {e}")
        return render_template('error.html', message="Could not load maps."), 500

@main.route('/maps/<map_name_slug>')
def map_detail(map_name_slug):
    map_name = map_name_slug.replace('-', ' ').title()
    try:
        map_data = Map.query.filter_by(name=map_name).first()

        if map_data:
            if map_data.defender_sites:
                map_data.defender_sites_list = [site.strip() for site in map_data.defender_sites.split(',')]
            else:
                map_data.defender_sites_list = []

            return render_template('map_detail.html', map=map_data)
        else:
            return render_template('error.html', message=f"Map '{map_name}' not found."), 404
    except Exception as e:
        print(f"Error fetching map detail for {map_name}: {e}")
        return render_template('error.html', message="Could not load map details."), 500

@main.route('/game-info')
def game_info():
    try:
        game_info_sections = GameInfo.query.order_by(GameInfo.id).all()
        return render_template('game_info.html', info_sections=game_info_sections)
    except Exception as e:
        print(f"Error fetching game info: {e}")
        return render_template('error.html', message="Could not load game information."), 500


@main.route('/api/search')
def search_operators():
    query = request.args.get('query', '').strip()

    if not query:
        return jsonify([])

    try:
        results = Operator.query.filter(Operator.name.ilike(f'%{query}%')).all()
        return jsonify([op.to_dict() for op in results])
    except Exception as e:
        print(f"Error during search API call: {e}")
        return jsonify({'error': 'Could not perform search'}), 500

# API endpoint for getting sites on some map
@main.route('/api/map-sites/<map_name>')
def get_map_sites(map_name):
    try:
        map_data = Map.query.filter_by(name=map_name).first()

        if map_data and map_data.defender_sites:
            sites_list = [site.strip() for site in map_data.defender_sites.split(',')]
            return jsonify({'sites': sites_list})
        else:
            return jsonify({'sites': []}), 404

    except Exception as e:
        print(f"Error fetching map sites for {map_name}: {e}")
        return jsonify({'error': 'Could not fetch map sites'}), 500

@main.route('/lineup-suggestor', methods=['GET', 'POST'])
def lineup_suggestor():
    maps = []
    error = None
    selected_map_name = None
    selected_site = None
    selected_side = None
    is_solo_queue = False
    situation_description = None
    suggested_operators = []

    try:
        # get maps for dropdown menu
        maps = Map.query.order_by(Map.name).all()

        if request.method == 'POST':
            selected_map_name = request.form.get('map')
            selected_site = request.form.get('site')
            selected_side = request.form.get('side')
            is_solo_queue = request.form.get('solo_queue') == 'yes'
            situation_description = request.form.get('situation')

            print("Form Data Received for LLM Suggestion:")
            print(f"Map: {selected_map_name}")
            print(f"Site: {selected_site}")
            print(f"Side: {selected_side}")
            print(f"Solo Queue: {is_solo_queue}")
            print(f"Situation: {situation_description}")

            # --- LLM Integration Logic ---
            if LLM_API_KEY: # Only proceed if API key is set
                try:
                    # 1. Fetch relevant data from the database
                    selected_map = Map.query.filter_by(name=selected_map_name).first()
                    # Fetch operators for the selected side
                    available_operators = Operator.query.filter_by(side=selected_side).all()

                    # Basic validation
                    if not selected_map_name or not selected_site or not selected_side or situation_description is None:
                         error = "Please fill in all required fields."
                         print("Validation Error:", error)
                    elif not selected_map:
                        error = f"Map '{selected_map_name}' not found in database."
                        print(error)
                    elif not available_operators:
                         error = f"No {selected_side} operators found in the database."
                         print(error)
                    elif not situation_description or not situation_description.strip():
                         error = "Please provide a situation description."
                         print(error)
                    else:
                        # 2. Construct the prompt for the LLM
                        map_data_formatted = format_map_data_for_prompt(selected_map)
                        operator_data_formatted = format_operator_data_for_prompt(available_operators)

                        # Craft the prompt - be very clear about the desired output format
                        prompt = textwrap.dedent(f"""
                        You are an expert Rainbow Six Siege player and tactical analyst.
                        Your task is to suggest a lineup of 3 operators for a specific scenario.
                        Consider the provided map details, the specific defender site, whether the user is playing solo or with a team, and the detailed situation description.
                        Only suggest operators from the list of available operators provided, ensuring they match the user's side ({selected_side}).
                        Prioritize operators whose abilities, role, armor/speed, synergies, counters, and solo-friendliness (if applicable) best fit the map, site, team size, and described situation.
                        Provide ONLY the names of the 3 most suitable suggested operators, separated by commas. Do not include any other text, explanations, rankings, or formatting like bullet points or numbers. Ensure the names exactly match the names in the provided list. If you cannot find 3 suitable operators, provide as many as you can (up to 3).

                        Map Details:
                        {map_data_formatted}

                        Defender Site: {selected_site}

                        Playing as Side: {selected_side}
                        Playing Style: {'Solo Queue (consider operators effective independently)' if is_solo_queue else 'With a Team (consider team synergies)'}

                        Situation Description: {situation_description}

                        {operator_data_formatted}

                        Suggest exactly 3 {selected_side} operators from the list above, comma-separated (e.g., Operator1, Operator2, Operator3):
                        """)

                        # 3. Call the LLM
                        suggested_names = get_llm_suggestions(prompt)
                        print(f"LLM suggested names (parsed): {suggested_names}") # Debugging

                        # 4. Query the database for the suggested operator objects
                        if suggested_names:
                            # Use the 'in_' filter to get multiple operators by name
                            # Filter by side again just to be extra safe
                            suggested_operators_from_db = Operator.query.filter(
                                Operator.name.in_(suggested_names),
                                Operator.side == selected_side
                            ).all()

                            # Order the results based on the LLM's suggestion order if possible
                            # Create a dictionary mapping name to Operator object
                            found_operators_dict = {op.name: op for op in suggested_operators_from_db}
                            # Build the final list in the order of suggested_names, only including found operators
                            suggested_operators = [
                                found_operators_dict[name] for name in suggested_names if name in found_operators_dict
                            ]

                            print(f"Found {len(suggested_operators)} suggested operators in DB.") # Debugging
                            if not suggested_operators:
                                error = "Could not find suggested operators in the database. Check LLM output format."

                        else:
                            print("LLM did not return any valid operator names.") # Debugging
                            error = "Could not get operator suggestions from the AI. Try rephrasing the situation."

                except Exception as llm_e:
                    print(f"An error occurred during LLM processing: {llm_e}")
                    error = "An error occurred while generating suggestions. Please try again."
            else:
                error = "LLM API key not configured. Cannot generate suggestions."
                print(error)

            # Pass the received data back to the template to pre-fill the form
            # and pass the suggested operators list and any error message
            # Continue to render_template below

        # Render the template, passing data needed for the form and potential results
        return render_template(
            'lineup_suggestor.html',
            maps=maps, # Pass maps for the dropdown
            selected_map_name=selected_map_name,
            selected_site=selected_site, # Pass selected site back to JS for initial population
            selected_side=selected_side,
            is_solo_queue=is_solo_queue,
            situation_description=situation_description,
            suggested_operators=suggested_operators, # Pass the results (list of Operator objects)
            error=error # Pass any error message to the template
        )


    except Exception as e:
        print(f"Error in lineup_suggestor route: {e}")
        error = "Could not load data for the lineup suggestor."
        return render_template('error.html', message=error), 500
