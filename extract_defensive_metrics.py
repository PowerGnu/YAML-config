# clean_defensive_metrics.py
import pandas as pd

# Path to the defensive metrics file
defensive_metrics_path = r"C:\Users\ferga\OneDrive\Medium\New\PC\Bootstrap Static\Operation Holistic\Player Stats\Weekly Stats\defensive_metrics.csv"

# Load defensive metrics
print("Loading defensive metrics...")
defensive_metrics_df = pd.read_csv(defensive_metrics_path)

# Filter to include only the 2024 season
print("Filtering for the 2024 season...")
defensive_metrics_2024 = defensive_metrics_df.drop_duplicates(subset='team_name', keep='last')

# Save the cleaned defensive metrics
cleaned_defensive_metrics_path = r"C:\Users\ferga\OneDrive\Medium\New\PC\Bootstrap Static\Operation Holistic\Player Stats\Weekly Stats\cleaned_defensive_metrics.csv"
print(f"Saving cleaned defensive metrics to {cleaned_defensive_metrics_path}...")
defensive_metrics_2024.to_csv(cleaned_defensive_metrics_path, index=False)

print("Defensive metrics cleaned and saved successfully!")
