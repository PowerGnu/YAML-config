import json
import os
from understatapi import UnderstatClient

# Specify the folder for saving outputs
base_folder = r"C:\Users\ferga\OneDrive\Modular Framework\EPL_Data"
os.makedirs(base_folder, exist_ok=True)  # Ensure the folder exists

# Define league and season
league = "EPL"
season = "2024"  # Replace with the desired season year

# Initialize UnderstatClient
with UnderstatClient() as understat:

    # 1. Fetch Player Data
    player_file = os.path.join(base_folder, f"EPL_Players_{season}.json")
    player_data = understat.league(league=league).get_player_data(season=season)
    with open(player_file, 'w') as f:
        json.dump(player_data, f, indent=4)
    print(f"Player data saved to: {player_file}")

    # 2. Fetch Team Data
    team_file = os.path.join(base_folder, f"EPL_Teams_{season}.json")
    team_data = understat.league(league=league).get_team_data(season=season)
    with open(team_file, 'w') as f:
        json.dump(team_data, f, indent=4)
    print(f"Team data saved to: {team_file}")

    # 3. Fetch Match Data
    match_file = os.path.join(base_folder, f"EPL_Matches_{season}.json")
    match_data = understat.league(league=league).get_match_data(season=season)
    with open(match_file, 'w') as f:
        json.dump(match_data, f, indent=4)
    print(f"Match data saved to: {match_file}")
