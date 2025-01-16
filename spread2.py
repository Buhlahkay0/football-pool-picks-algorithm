import pandas as pd

# Load the CSV file
input_csv = "games.csv"  # Replace with your CSV file path
df = pd.read_csv(input_csv)

# Initialize a list to keep track of picked teams
picked_teams = []

# Group the data by week
grouped = df.groupby('Week')

# Initialize a variable to track if duplicates exist
has_duplicates = True

while has_duplicates:
    has_duplicates = False  # Assume no duplicates initially

    # Iterate through each week
    for week, group in grouped:
        # Filter out teams that have already been picked
        group = group[~group['Team 1'].isin(picked_teams) & ~group['Team 2'].isin(picked_teams)]
        
        if not group.empty:
            max_spread_row = group.loc[group['Spread'].abs().idxmax()]  # Find the row with the highest absolute spread
            week_number = int(week)  # Convert week to an integer
            spread = max_spread_row['Spread']
            team1 = max_spread_row['Team 1']
            team2 = max_spread_row['Team 2']
            
            if spread > 0:
                winning_team = team1
            else:
                winning_team = team2
            
            print(f"Week {week_number} | {winning_team} spread: {spread}")
            
            # Add the picked team to the list
            picked_teams.append(winning_team)

        # Check for duplicate team picks
        duplicate_teams = group[group['Team 1'].isin(picked_teams) | group['Team 2'].isin(picked_teams)]
        if not duplicate_teams.empty:
            has_duplicates = True  # Set flag to True if duplicates exist
            # Choose the game with the highest spread for the duplicate team
            max_spread_row = duplicate_teams.loc[duplicate_teams['Spread'].abs().idxmax()]
            week_number = int(week)
            spread = max_spread_row['Spread']
            team1 = max_spread_row['Team 1']
            team2 = max_spread_row['Team 2']
            
            if spread > 0:
                winning_team = team1
            else:
                winning_team = team2
            
            print(f"Week {week_number} | {winning_team} spread: {spread}")
            
            # Add the picked team to the list
            picked_teams.append(winning_team)
