import requests
import pandas as pd
import os

# Step 1: Fetch Schedule and Team Names
def fetch_schedule_and_teams():
    # Fetch team data from the FPL API
    teams_response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    teams_data = teams_response.json()["teams"]

    # Create a dictionary to map team IDs to team names
    team_mapping = {team["id"]: team["name"] for team in teams_data}

    # Fetch fixture data from the FPL API
    fixtures_response = requests.get("https://fantasy.premierleague.com/api/fixtures/")
    fixtures_data = fixtures_response.json()

    # Convert the fixtures data to a DataFrame
    fixtures_df = pd.DataFrame(fixtures_data)

    # Map team IDs to team names
    fixtures_df["home_team_name"] = fixtures_df["team_h"].map(team_mapping)
    fixtures_df["away_team_name"] = fixtures_df["team_a"].map(team_mapping)

    return fixtures_df

# Step 2: Parse Stats Data
def parse_stats_column(fixtures_df):
    def parse_stats(stats):
        result = {}
        for stat in stats:  # Directly iterate over the list of dictionaries
            metric = stat["identifier"]
            # Sum the values for home ('h') and away ('a') metrics
            home_value = sum(item["value"] for item in stat["h"]) if stat["h"] else 0
            away_value = sum(item["value"] for item in stat["a"]) if stat["a"] else 0
            result[f"home_{metric}"] = home_value
            result[f"away_{metric}"] = away_value
        return result

    # Apply parsing function to the `stats` column
    parsed_stats = fixtures_df["stats"].apply(parse_stats)

    # Create a new DataFrame from parsed stats and merge it with the original fixtures DataFrame
    stats_df = pd.DataFrame(parsed_stats.tolist())
    fixtures_with_stats = pd.concat([fixtures_df, stats_df], axis=1)

    return fixtures_with_stats

# Main Process
def main():
    # Step 1: Fetch schedule and team names
    print("Fetching schedule and team names...")
    fixtures_df = fetch_schedule_and_teams()

    # Step 2: Parse nested stats data
    print("Parsing stats column...")
    if "stats" in fixtures_df.columns:
        fixtures_with_stats = parse_stats_column(fixtures_df)
    else:
        fixtures_with_stats = fixtures_df
        print("Stats column not found, skipping stats parsing.")

    # Save the final DataFrame to a CSV file
    file_path = r"C:\Users\ferga\OneDrive\Modular Framework\Schedule\EPL_2024_2025_Fixtures_with_Parsed_Stats.csv"
    fixtures_with_stats.to_csv(file_path, index=False)

    print(f"Final data saved to {file_path}")

# Run the script
if __name__ == "__main__":
    main()
