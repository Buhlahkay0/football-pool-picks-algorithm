import pandas as pd

# Load the CSV file
input_csv = "games.csv"  # Replace with your CSV file path
df = pd.read_csv(input_csv)

# Group the data by week
grouped = df.groupby('Week')

# Iterate through each week
for week, group in grouped:
    max_spread_row = group.loc[group['Spread'].abs().idxmax()]  # Find the row with the highest absolute spread
    week_number = int(week)  # Convert week to an integer
    spread = max_spread_row['Spread']
    team1 = max_spread_row['Team 1']
    team2 = max_spread_row['Team 2']
    
    if spread < 0:
        winning_team = team1
    else:
        winning_team = team2
    
    print(f"Week {week_number} | {winning_team} spread: {spread}")
