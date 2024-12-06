from understatapi import UnderstatClient
import pandas as pd
from datetime import datetime

# Define gameweek date ranges
gameweek_dates = {
    1: ("2024-08-16", "2024-08-19"),
    2: ("2024-08-24", "2024-08-25"),
    3: ("2024-08-31", "2024-09-01"),
    4: ("2024-09-14", "2024-09-15"),
    5: ("2024-09-21", "2024-09-22"),
    6: ("2024-09-28", "2024-09-30"),
    7: ("2024-10-05", "2024-10-06"),
    8: ("2024-10-19", "2024-10-21"),
    9: ("2024-10-25", "2024-10-27"),
    10: ("2024-11-02", "2024-11-04"),
    11: ("2024-11-09", "2024-11-10"),
    12: ("2024-11-23", "2024-11-25"),
    13: ("2024-11-29", "2024-12-01"),
    14: ("2024-12-03", "2024-12-05"),
    15: ("2024-12-07", "2024-12-09"),
    16: ("2024-12-14", "2024-12-16"),
    17: ("2024-12-21", "2024-12-22"),
    18: ("2024-12-26", "2024-12-27"),
    19: ("2024-12-29", "2024-12-30"),
    20: ("2025-01-01", "2025-01-01"),
    21: ("2025-01-04", "2025-01-06"),
    22: ("2025-01-14", "2025-01-16"),
    23: ("2025-01-18", "2025-01-20"),
    24: ("2025-01-25", "2025-01-27"),
    25: ("2025-02-01", "2025-02-03"),
    26: ("2025-02-15", "2025-02-17"),
    27: ("2025-02-22", "2025-02-24"),
    28: ("2025-03-08", "2025-03-10"),
    29: ("2025-03-15", "2025-03-17"),
    30: ("2025-04-01", "2025-04-02"),
    31: ("2025-04-05", "2025-04-07"),
    32: ("2025-04-12", "2025-04-14"),
    33: ("2025-04-19", "2025-04-21"),
    34: ("2025-04-26", "2025-04-28"),
    35: ("2025-05-03", "2025-05-05"),
    36: ("2025-05-10", "2025-05-12"),
    37: ("2025-05-18", "2025-05-18"),
    38: ("2025-05-25", "2025-05-25"),
}

# Define a run-to-date (only process matches up to this date)
run_to_date = "2024-12-15"  # Example: set to mid-season update weekly
run_to_date = datetime.strptime(run_to_date, "%Y-%m-%d")

# Helper function to map matches to gameweeks
def map_to_gameweek(match_date):
    match_date = datetime.strptime(match_date, "%Y-%m-%d")
    for week, (start, end) in gameweek_dates.items():
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        if start_date <= match_date <= end_date:
            return week
    return None  # If match doesn't fall within any gameweek

# Initialize Understat client
with UnderstatClient() as understat:
    # Retrieve matches for the league and season
    league_name = "EPL"
    season = "2024"
    matches = understat.league(league=league_name).get_match_data(season=season)

    if not matches:
        print("No matches found for the specified league and season.")
        exit()

    # Convert matches to DataFrame
    matches_df = pd.DataFrame(matches)
    matches_df['datetime'] = pd.to_datetime(matches_df['datetime'])
    matches_df['gameweek'] = matches_df['datetime'].dt.strftime("%Y-%m-%d").apply(map_to_gameweek)

    # Filter matches: Exclude future matches based on the run-to-date
    matches_df = matches_df[matches_df['datetime'] <= run_to_date]
    matches_df = matches_df.dropna(subset=['gameweek'])  # Ensure gameweek mapping is valid

    # Initialize a list to store player statistics
    player_stats_list = []

    for match_id in matches_df['id']:
        print(f"Processing match {match_id}...")
        try:
            roster = understat.match(match=match_id).get_roster_data()
            if not roster:
                print(f"No roster data for match {match_id}. Skipping...")
                continue
        except Exception as e:
            print(f"Skipping invalid match {match_id}: {e}")
            continue

        for team in roster:
            if not roster[team]:
                print(f"No data for team {team} in match {match_id}. Skipping...")
                continue
            for player_id, player_data in roster[team].items():
                player_data['match_id'] = match_id
                player_data['team'] = team
                player_stats_list.append(player_data)

    # Convert the list of player stats into a DataFrame
    if player_stats_list:
        player_stats = pd.DataFrame(player_stats_list)
    else:
        print("No player stats were collected. Exiting...")
        exit()

    # Merge match gameweek information
    print("Merging match gameweek information...")
    player_stats = player_stats.merge(matches_df[['id', 'gameweek']], left_on='match_id', right_on='id', how='left')

    # Drop unnecessary columns (id_x and id_y)
    player_stats = player_stats.drop(columns=["id_x", "id_y"], errors="ignore")

    # Convert numeric columns to avoid "numbers saved as text" warnings
    numeric_columns = [
        'id_x', 'goals', 'own_goals', 'shots', 'xG', 'time',
        'player_id', 'team_id', 'yellow_card', 'red_card',
        'roster_in', 'roster_out', 'key_passes', 'assists', 'xA',
        'xGChain', 'xGBuildup', 'positionOrder', 'match_id', 'id_y'
    ]
    for col in numeric_columns:
        if col in player_stats.columns:
            player_stats[col] = pd.to_numeric(player_stats[col], errors='coerce')

    # Save weekly stats to separate worksheets in one Excel file
    output_path = r"C:\Users\ferga\OneDrive\Modular Framework\Player Stats\weekly_player_stats.xlsx"
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for week in sorted(player_stats['gameweek'].unique()):
            week_data = player_stats[player_stats['gameweek'] == week]
            week_data.to_excel(writer, sheet_name=f"GW{int(week)}", index=False)
    print(f"Weekly player statistics saved to {output_path}")