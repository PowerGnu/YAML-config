import asyncio
import aiohttp
from understat import Understat
import pandas as pd

# Function to fetch league matches
async def fetch_league_matches(league, season):
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
            understat = Understat(session)
            matches = await understat.get_league_results(league, season)
            return matches
    except aiohttp.ClientConnectorError as e:
        print(f"Error fetching league matches: {e}")
        return None

# Function to fetch player data for a match
async def fetch_match_players(match_id):
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
            understat = Understat(session)
            players = await understat.get_match_players(match_id)
            return players
    except aiohttp.ClientConnectorError as e:
        print(f"Error fetching match players for match_id {match_id}: {e}")
        return None

# Main function to fetch all player data
async def fetch_all_player_data(league, season):
    matches = await fetch_league_matches(league, season)
    if matches is None:
        print("Failed to fetch matches. Exiting.")
        return None

    all_players_data = []

    for match in matches:
        match_id = match['id']
        home_team = match['h']['title']
        away_team = match['a']['title']
        match_date = match['datetime']

        print(f"Fetching player data for match {match_id} ({home_team} vs. {away_team})")
        players_data = await fetch_match_players(match_id)

        if players_data:
            for team_key, team_players in players_data.items():
                team_type = 'home' if team_key == 'h' else 'away'
                for player_id, player_stats in team_players.items():
                    player_stats.update({
                        'team_type': team_type,
                        'match_id': match_id,
                        'match_date': match_date,
                        'home_team': home_team,
                        'away_team': away_team
                    })
                    all_players_data.append(player_stats)

    return pd.DataFrame(all_players_data)

# Run the process
def main():
    league = 'epl'
    season = 2024
    try:
        all_players_df = asyncio.run(fetch_all_player_data(league, season))
        if all_players_df is not None:
            save_path = r"C:\Users\ferga\OneDrive\Modular Framework\Player Stats\Weekly Stats\all_players_2024_epl.csv"
            all_players_df.to_csv(save_path, index=False)
            print(f"File saved successfully to: {save_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
