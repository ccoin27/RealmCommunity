from flask import Flask, render_template, request, jsonify, abort
import json
import os
from datetime import datetime

app = Flask(__name__)

COUNTERS_FILE = 'counters.json'

def init_counters():
    if not os.path.exists(COUNTERS_FILE):
        default_data = {
            "members": 120,
            "online": 50,
            "messages": 3000,
            "rpg_players": 300,
            "last_updated": datetime.now().isoformat()
        }
        with open(COUNTERS_FILE, 'w') as f:
            json.dump(default_data, f)

def get_counters():
    init_counters()
    with open(COUNTERS_FILE, 'r') as f:
        return json.load(f)

def update_counters(new_data):
    counters = get_counters()
    counters.update(new_data)
    counters['last_updated'] = datetime.now().isoformat()
    with open(COUNTERS_FILE, 'w') as f:
        json.dump(counters, f)
    return counters

@app.route('/')
def index():
    counters = get_counters()
    return render_template('index.html', counters=counters)

@app.route('/api/counters', methods=['GET'])
def get_counters_api():
    return jsonify(get_counters())

@app.route('/api/counters', methods=['POST'])
def update_counters_api():
    if not request.is_json:
        abort(400, description="Request must be JSON")
    
    data = request.get_json()
    required_fields = ['members', 'online', 'messages', 'rpg_players', 'key']
    
    if not all(field in data for field in required_fields):
        abort(400, description="Missing required fields")

    if data['key'] != "coin":
        abort(400, description="Invalid key")

    try:
        updated = update_counters({
            "members": int(data['members']),
            "online": int(data['online']),
            "messages": int(data['messages']),
            "rpg_players": int(data['rpg_players'])
        })
        return jsonify(updated)
    except ValueError:
        abort(400, description="Invalid data types")

if __name__ == '__main__':
    app.run(debug=True, port=8080)