import pandas as pd
import os

def load_schedule(schedule_path):
    try:
        schedule_df = pd.read_csv(schedule_path)
        required_columns = ['home_team_name', 'away_team_name', 'home_goals_scored', 'away_goals_scored']
        missing_columns = [col for col in required_columns if col not in schedule_df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns in schedule data: {', '.join(missing_columns)}")
        
        return schedule_df
    except FileNotFoundError:
        print(f"Error: Schedule file not found at {schedule_path}")
        raise
    except pd.errors.EmptyDataError:
        print("Error: Schedule file is empty")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise

def align_schedule(schedule_path, output_path):
    try:
        print(f"Loading schedule data from {schedule_path}...")
        schedule_df = load_schedule(schedule_path)
        
        print("Aligning schedule data...")
        schedule_df['home_score_margin'] = schedule_df['home_goals_scored'] - schedule_df['away_goals_scored']
        schedule_df['away_score_margin'] = schedule_df['away_goals_scored'] - schedule_df['home_goals_scored']
        
        print(f"Saving aligned schedule data to {output_path}...")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        schedule_df.to_csv(output_path, index=False)
        print("Schedule alignment and save completed successfully!")
    except Exception as e:
        print(f"An error occurred during alignment: {e}")

def main():
    schedule_path = r"C:\Users\ferga\OneDrive\Modular Framework\Schedule\EPL_2024_2025_Fixtures_with_Parsed_Stats.csv"
    output_path = r"C:\Users\ferga\OneDrive\Modular Framework\Schedule\aligned_schedule.csv"
    align_schedule(schedule_path, output_path)

if __name__ == "__main__":
    main()
