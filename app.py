from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample match data
matches = [
    {
        "id": "12345",
        "home_team": {"id": "89", "title": "Manchester United", "short_title": "MUN"},
        "away_team": {"id": "228", "title": "Fulham", "short_title": "FUL"},
        "goals": {"home": 1, "away": 0},
        "xG": {"home": 2.04, "away": 0.42},
        "datetime": "2024-12-04T19:00:00Z",
        "forecast": {"win": 0.81, "draw": 0.15, "loss": 0.04},
    }
]

@app.route('/matches', methods=['GET'])
def get_matches():
    date = request.args.get('date')
    team = request.args.get('team')
    
    # Filter matches by date and/or team
    filtered_matches = [
        match for match in matches
        if (not date or match['datetime'].startswith(date)) and
           (not team or team in match['home_team']['title'] or team in match['away_team']['title'])
    ]
    return jsonify(filtered_matches)

if __name__ == '__main__':
    app.run(debug=True)
