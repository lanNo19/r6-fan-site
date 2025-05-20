from flask import render_template, request, jsonify, Blueprint, url_for
from .app import db # Import db from the main app instance
from .models import Operator, Map, GameInfo

main = Blueprint('main', __name__)

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

@main.route('/lineup-suggestor', methods=['GET', 'POST'])
def lineup_suggestor():
    maps = []
    error = None

    try:
        maps = Map.query.order_by(Map.name).all() # Fetch all maps, ordered by name

        if request.method == 'POST':
            selected_map_name = request.form.get('map')
            selected_site = request.form.get('site')
            selected_side = request.form.get('side')
            is_solo_queue = request.form.get('solo_queue') == 'yes'
            situation_description = request.form.get('situation')

            print("Form Data Received:")
            print(f"Map: {selected_map_name}")
            print(f"Site: {selected_site}")
            print(f"Side: {selected_side}")
            print(f"Solo Queue: {is_solo_queue}")
            print(f"Situation: {situation_description}")

            # TODO(lanNo19): llm integration, result = suggested_operators
            suggested_operators = []

            return render_template(
                'lineup_suggestor.html',
                maps=maps, # Pass maps back for the dropdown
                selected_map_name=selected_map_name,
                selected_site=selected_site,
                selected_side=selected_side,
                is_solo_queue=is_solo_queue,
                situation_description=situation_description,
                suggested_operators=suggested_operators
            )

        return render_template('lineup_suggestor.html', maps=maps)

    except Exception as e:
        print(f"Error in lineup_suggestor route: {e}")
        error = "Could not load data for the lineup suggestor."
        # Ensure error.html exists
        return render_template('error.html', message=error), 500