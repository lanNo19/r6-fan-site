# r6_fan_app/routes.py

from flask import render_template, request, jsonify, Blueprint, url_for
import requests
import os  # Needed to access environment variables for API key

# Import db and models using absolute imports from the r6_fan_app package
from r6_fan_app import db
from r6_fan_app.models import Operator, Map, GameInfo

# Create a Blueprint instance
main = Blueprint('main', __name__)


# Define routes using the blueprint
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
            operator_data.secondary_gadgets_list = [g.strip() for g in operator_data.secondary_gadgets.split(
                ',')] if operator_data.secondary_gadgets else []
            operator_data.synergy_list = [op.strip() for op in operator_data.synergy_examples.split(
                ',')] if operator_data.synergy_examples else []
            operator_data.counter_list = [op.strip() for op in operator_data.counter_examples.split(
                ',')] if operator_data.counter_examples else []

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


# API Endpoint for Map Sites (Moved from app.py)
@main.route('/api/map-sites/<map_name>')
def get_map_sites(map_name):
    mock_map_data = {
        "Bank": ["Vault", "Open Area - Teller", "Archives - Server", "CEO Office"],
        "Oregon": ["Kitchen", "Kids Bedroom", "Basement"],  # Simplified for example
        "Coastline": ["Hookah Lounge / Billiards Room", "Blue Bar / Sunrise Bar", "Penthouse / Theater"],
        "Kafe Dostoyevsky": ["Reading Room / Fireplace Hall", "Mining Room / Dining Room", "Kitchen / Bake Shop"],
        "Kanal": ["Secure Containers / Boats", "Server Room / Kayak", "Coast Guard Office / Lounge"],
        "Villa": ["Living Room / Bar", "Dining Room / Kitchen", "Classic Room / Games Room", "Statuary Room / Vault"],
        # Add more maps and their sites as needed
    }
    sites = mock_map_data.get(map_name, [])
    return jsonify(sites=sites)


@main.route('/lineup-suggestor', methods=['GET', 'POST'])
def lineup_suggestor():
    maps = Map.query.all()  # Fetch all maps for the dropdown

    suggested_operators = None
    selected_map_name = None
    selected_site = None
    selected_side = None
    is_solo_queue = False
    situation_description = ''
    error_message = None

    if request.method == 'POST':
        selected_map_name = request.form.get('map')
        selected_site = request.form.get('site')
        selected_side = request.form.get('side')
        solo_queue_str = request.form.get('solo_queue')
        situation_description = request.form.get('situation')

        is_solo_queue = (solo_queue_str == 'yes')

        # Basic validation
        if not selected_map_name or not selected_site or not selected_side or not situation_description:
            error_message = "Please fill in all required fields."
        else:
            # --- LLM Call to get suggestions ---
            try:
                # Construct the prompt for the LLM
                prompt = f"""
                You are an expert Rainbow Six Siege strategist.
                Given the following situation, suggest 5 operators (no more, no less) that would be ideal for the team.
                Prioritize operators that directly address the situation and work well together.
                If playing solo, suggest operators that are more self-sufficient.
                Provide only the operator names, separated by commas.

                Map: {selected_map_name}
                Site: {selected_site}
                Side: {selected_side}
                Playing: {'Solo Queue' if is_solo_queue else 'With a Team'}
                Situation: {situation_description}

                Example Output: Ash, Zofia, Thermite, Thatcher, Twitch
                """

                chat_history = []
                chat_history.append({"role": "user", "parts": [{"text": prompt}]})
                payload = {"contents": chat_history}
                # Get API key from environment variable using the correct name
                api_key = os.getenv("LLM_API_KEY")
                if not api_key:
                    raise ValueError("LLM_API_KEY environment variable not set.")

                # Call the Gemini API
                api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + api_key
                response = requests.post(api_url, json=payload)
                response.raise_for_status()  # Raise an exception for HTTP errors
                result = response.json()

                if result and result.get('candidates'):
                    llm_response_text = result['candidates'][0]['content']['parts'][0]['text'].strip()
                    suggested_operator_names = [name.strip() for name in llm_response_text.split(',') if name.strip()]

                    # Fetch operator details from your database
                    suggested_operators = []
                    for op_name in suggested_operator_names:
                        operator_obj = Operator.query.filter_by(name=op_name).first()
                        if operator_obj:
                            suggested_operators.append(operator_obj)
                        else:
                            print(f"Warning: Suggested operator '{op_name}' not found in database.")

                    if not suggested_operators:
                        error_message = "The AI could not suggest valid operators from our database. Please try a different situation."

                else:
                    error_message = "Failed to get a valid response from the AI. Please try again."

            except requests.exceptions.RequestException as req_err:
                print(f"API request failed: {req_err}")
                error_message = "Failed to connect to the AI service. Please try again later."
            except ValueError as val_err:  # Catch the new ValueError for missing API key
                print(f"Configuration error: {val_err}")
                error_message = "Server configuration error: LLM API Key not set."
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                error_message = "An unexpected error occurred while getting suggestions."

    return render_template(
        'lineup_suggestor.html',
        maps=maps,
        suggested_operators=suggested_operators,
        selected_map_name=selected_map_name,
        selected_site=selected_site,
        selected_side=selected_side,
        is_solo_queue=is_solo_queue,
        situation_description=situation_description,
        error=error_message
    )


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
