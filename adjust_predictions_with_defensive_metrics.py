import pandas as pd

# File paths update weekly
predictions_path = r"C:\Users\ferga\OneDrive\Medium\New\PC\Bootstrap Static\Operation Holistic\Player Stats\Weekly Stats\predictions_week_6.csv"
defensive_metrics_path = r"C:\Users\ferga\OneDrive\Medium\New\PC\Bootstrap Static\Operation Holistic\Player Stats\Weekly Stats\cleaned_defensive_metrics.csv"
output_path = r"C:\Users\ferga\OneDrive\Medium\New\PC\Bootstrap Static\Operation Holistic\Player Stats\Weekly Stats\adjusted_predictions_with_defensive_metrics_week_6.csv"

# Team name mapping: short names to full names
team_name_mapping = {
    "Arsenal": "Arsenal",
    "Brighton": "Brighton",
    "Brentford": "Brentford",
    "Southampton": "Southampton",
    "Everton": "Everton",
    "Bournemouth": "Bournemouth",
    "Ipswich": "Ipswich",
    "Fulham": "Fulham",
    "Leicester": "Leicester",
    "Aston Villa": "Aston Villa",
    "Nott'm Forest": "Nottingham Forest",
    "Wolves": "Wolverhampton Wanderers",
    "West Ham": "West Ham",
    "Man City": "Manchester City",
    "Chelsea": "Chelsea",
    "Crystal Palace": "Crystal Palace",
    "Newcastle": "Newcastle United",
    "Spurs": "Tottenham",
    "Man Utd": "Manchester United",
    "Liverpool": "Liverpool"
}

# Load predictions
print("Loading predictions...")
predictions_df = pd.read_csv(predictions_path)

# Map short team names to full names
print("Mapping short team names to full names...")
predictions_df['home_team'] = predictions_df['home_team'].map(team_name_mapping)
predictions_df['away_team'] = predictions_df['away_team'].map(team_name_mapping)

# Validate mappings
if predictions_df['home_team'].isnull().any() or predictions_df['away_team'].isnull().any():
    raise ValueError("Some team names in predictions could not be mapped to full names. Check the mapping dictionary.")

# Load defensive metrics
print("Loading defensive metrics...")
defensive_metrics_df = pd.read_csv(defensive_metrics_path)

# Merge defensive metrics into predictions
print("Merging defensive metrics into predictions...")
predictions_df = predictions_df.merge(
    defensive_metrics_df,
    left_on="home_team",
    right_on="team_name",
    how="left"
).rename(columns={
    'xGA': 'xGA_home',
    'shots_against': 'shots_against_home',
    'goals_conceded': 'goals_conceded_home'
})

predictions_df = predictions_df.merge(
    defensive_metrics_df,
    left_on="away_team",
    right_on="team_name",
    how="left",
    suffixes=('', '_away')
).rename(columns={
    'xGA': 'xGA_away',
    'shots_against': 'shots_against_away',
    'goals_conceded': 'goals_conceded_away'
})

# Drop redundant columns
predictions_df = predictions_df.drop(columns=["team_name", "team_name_away"], errors="ignore")

# Adjust team scores based on defensive metrics
print("Adjusting team scores...")
alpha, beta, gamma = 0.1, 0.05, 0.2  # Coefficients for xGA, shots_against, and goals_conceded
predictions_df['adjusted_score_home'] = (
    predictions_df['total_score_home'] - 
    alpha * predictions_df['xGA_home'] - 
    beta * predictions_df['shots_against_home'] - 
    gamma * predictions_df['goals_conceded_home']
)
predictions_df['adjusted_score_away'] = (
    predictions_df['total_score_away'] - 
    alpha * predictions_df['xGA_away'] - 
    beta * predictions_df['shots_against_away'] - 
    gamma * predictions_df['goals_conceded_away']
)

# Predict adjusted outcomes
print("Predicting adjusted outcomes...")
predictions_df['adjusted_outcome'] = predictions_df.apply(
    lambda row: 'H' if row['adjusted_score_home'] > row['adjusted_score_away'] 
    else 'A' if row['adjusted_score_away'] > row['adjusted_score_home'] 
    else 'D',
    axis=1
)

# Save adjusted predictions
print(f"Saving adjusted predictions to {output_path}...")
predictions_df.to_csv(output_path, index=False)

print("Adjustment process complete!")
