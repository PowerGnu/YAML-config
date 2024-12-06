import pandas as pd
import os
import json

# Load configuration
config_path = r"C:\Users\ferga\OneDrive\Modular Framework\config_template.json"
with open(config_path, 'r') as file:
    config = json.load(file)
base_directory = config['general']['base_directory']
current_game_week = str(config['general']['current_game_week'])

# Define file paths
input_path = os.path.join(base_directory, "Player Stats", "Weekly Stats", "all_players_2024_epl.csv")
output_path = os.path.join(base_directory, "Player Stats", "Weekly Stats", f"all_players_week_{current_game_week}_with_scores.csv")

# Load the data
print(f"Loading data from {input_path}...")
all_players_df = pd.read_csv(input_path)

# Filter data for the current game week
print(f"Filtering data for Game Week {current_game_week}...")
current_week_data = all_players_df[all_players_df['match_date'].str.contains(f'{current_game_week}', na=False)].copy()

# Validate game week data
if current_week_data.empty:
    print(f"No data found for Game Week {current_game_week}. Exiting...")
else:
    # Ensure numeric columns are converted
    print("Ensuring numeric columns are converted...")
    numeric_columns = [
        'goals', 'own_goals', 'shots', 'xG', 'time', 'key_passes',
        'assists', 'xA', 'xGChain', 'xGBuildup', 'yellow_card', 'red_card'
    ]
    current_week_data.loc[:, numeric_columns] = current_week_data.loc[:, numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Define the advanced scoring formula
    def calculate_advanced_score(row):
        score = (
            (5 * row['goals']) +
            (4 * row['assists']) +
            (2.5 * row['xG']) +
            (2 * row['xA']) +
            (1.5 * row['shots']) +
            (1.5 * row['key_passes']) +
            (1 * row['xGChain']) +
            (0.75 * row['xGBuildup']) +
            (0.1 * row['time']) -
            (1 * row['yellow_card']) -
            (3 * row['red_card'])
        )
        return score

    # Calculate scores
    print("Calculating player scores...")
    current_week_data['score'] = current_week_data.apply(calculate_advanced_score, axis=1)

    # Save the updated DataFrame
    print(f"Saving the updated data to {output_path}...")
    current_week_data.to_csv(output_path, index=False)

    print("Player scores calculated and saved successfully!")
