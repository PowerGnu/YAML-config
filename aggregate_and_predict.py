import pandas as pd
import os
import json

# Load configuration
def load_config(config_path):
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config

# Aggregate team scores
def aggregate_scores(data, home_multiplier=1.05):
    team_scores = {}

    for _, row in data.iterrows():
        home_team = row['home_team']
        away_team = row['away_team']

        # Home team score
        home_score = row['home_score'] * home_multiplier
        if home_team not in team_scores:
            team_scores[home_team] = 0
        team_scores[home_team] += home_score

        # Away team score
        away_score = row['away_score']
        if away_team not in team_scores:
            team_scores[away_team] = 0
        team_scores[away_team] += away_score

    return team_scores

# Predict match outcomes
def predict_outcomes(schedule_data, team_scores, draw_threshold=0.1):
    predictions = []

    for _, row in schedule_data.iterrows():
        home_team = row['home_team']
        away_team = row['away_team']
        home_score = team_scores.get(home_team, 0)
        away_score = team_scores.get(away_team, 0)

        score_diff = home_score - away_score

        if abs(score_diff) < draw_threshold:
            result = 'D'
        elif score_diff > 0:
            result = 'H'
        else:
            result = 'A'

        predictions.append({
            'match_id': row['match_id'],
            'home_team': home_team,
            'away_team': away_team,
            'predicted_result': result,
            'home_score': home_score,
            'away_score': away_score
        })

    return pd.DataFrame(predictions)

def main():
    # Configuration path
    config_path = r"C:\Users\ferga\OneDrive\Modular Framework\config_template.json"
    config = load_config(config_path)

    # File paths
    base_directory = config['general']['base_directory']
    current_game_week = config['general']['current_game_week']
    schedule_path = os.path.join(base_directory, "Schedule", "aligned_schedule.csv")
    player_stats_path = os.path.join(base_directory, "Player Stats", "Weekly Stats")
    prediction_output_path = os.path.join(base_directory, "Predictions", f"predictions_week_{current_game_week}.csv")

    # Load aligned schedule
    print(f"Loading schedule data from {schedule_path}...")
    schedule_data = pd.read_csv(schedule_path)

    # Load player stats for cumulative weeks
    print(f"Aggregating player stats up to week {current_game_week}...")
    all_data = []
    for week in range(1, current_game_week + 1):
        week_file = os.path.join(player_stats_path, f"all_players_week_{week}_with_scores.csv")
        if os.path.exists(week_file):
            week_data = pd.read_csv(week_file)
            all_data.append(week_data)
        else:
            print(f"Warning: Missing data file for week {week}. Skipping.")

    if not all_data:
        print("No player stats data found. Exiting.")
        return

    all_data = pd.concat(all_data, ignore_index=True)

    # Aggregate scores
    print("Aggregating team scores...")
    team_scores = aggregate_scores(all_data)

    # Predict outcomes
    print("Predicting outcomes...")
    predictions = predict_outcomes(schedule_data, team_scores)

    # Save predictions
    os.makedirs(os.path.dirname(prediction_output_path), exist_ok=True)
    predictions.to_csv(prediction_output_path, index=False)
    print(f"Predictions saved to {prediction_output_path}")

if __name__ == "__main__":
    main()
