import os
import json
from flask import Flask, jsonify, request

# Initialize Flask app
app = Flask(__name__)

# Paths to your JSON files
BASE_FOLDER = r"C:\Users\ferga\OneDrive\Modular Framework\EPL_Data"
PLAYER_FILE = os.path.join(BASE_FOLDER, "EPL_Players_2024.json")
ALL_PLAYERS_FILE = os.path.join(BASE_FOLDER, "EPL_AllPlayers_2024.json")
MATCH_FILE = os.path.join(BASE_FOLDER, "EPL_Matches_2024.json")
TEAM_FILE = os.path.join(BASE_FOLDER, "EPL_Teams_2024.json")

# Load JSON data into memory
def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        print(f"Error: {file_path} not found.")
        return []

players_data = load_json(PLAYER_FILE)
all_players_data = load_json(ALL_PLAYERS_FILE)
matches_data = load_json(MATCH_FILE)
teams_data = load_json(TEAM_FILE)

@app.route('/')
def home():
    return "Welcome to the EPL Data API! Use /players, /all_players, /matches, or /teams to access data."

# Endpoint for player data
@app.route('/players', methods=['GET'])
def get_players():
    return jsonify(players_data)

# Endpoint for all player data
@app.route('/all_players', methods=['GET'])
def get_all_players():
    return jsonify(all_players_data)

# Endpoint for match data with optional filtering
@app.route('/matches', methods=['GET'])
def get_matches():
    date = request.args.get('date')
    team = request.args.get('team')
    filtered_matches = [
        match for match in matches_data
        if (not date or match['datetime'].startswith(date)) and
           (not team or team in match['h']['title'] or team in match['a']['title'])
    ]
    return jsonify(filtered_matches)

# Endpoint for team data
@app.route('/teams', methods=['GET'])
def get_teams():
    return jsonify(teams_data)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
