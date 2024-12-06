from understatapi import UnderstatClient

try:
    with UnderstatClient() as understat:
        print("Fetching EPL team data for the 2024 season...")
        league_teams = understat.league(league="EPL").get_team_data(season="2024")
        
        # Extract team ID and team name
        team_mapping = {team_id: team_data['title'] for team_id, team_data in league_teams.items()}
        
        # Display the cleaned mapping
        print("Team ID to Team Name Mapping:")
        for team_id, team_name in team_mapping.items():
            print(f"Team ID: {team_id}, Team Name: {team_name}")
except Exception as e:
    print("An error occurred:", e)
