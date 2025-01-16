import pandas as pd

# Load the CSV file
input_csv = "games.csv"  # Replace with your CSV file path
df = pd.read_csv(input_csv)

# Sort the DataFrame by absolute spread (highest spread first) and then by week (ascending order)
df = df.sort_values(by=['Spread', 'Week'], ascending=[False, True])

# Initialize a list to keep track of picked teams
already_picked = []

# Initialize a list to store the final picks
final_picks = []

# Iterate through the sorted DataFrame
for index, row in df.iterrows():
    week = row['Week']
    team1 = row['Team 1']
    team2 = row['Team 2']
    spread = row['Spread']
    
    # Check if either team has been picked in previous weeks
    if team1 not in already_picked and team2 not in already_picked:
        # Add the team to the list of picked teams
        already_picked.append(team1)
        
        # Store the pick in the final picks list
        final_picks.append((week, team1, spread))
    
    # Check for duplicate picks
    elif team1 in already_picked and team2 not in already_picked:
        # Find the existing pick and compare spreads
        existing_pick = next((pick for pick in final_picks if pick[1] == team1), None)
        if existing_pick and abs(spread) > abs(existing_pick[2]):
            # Replace the existing pick
            final_picks.remove(existing_pick)
            already_picked.remove(existing_pick[1])
            already_picked.append(team1)
            final_picks.append((week, team1, spread))
    
    elif team2 in already_picked and team1 not in already_picked:
        # Find the existing pick and compare spreads
        existing_pick = next((pick for pick in final_picks if pick[1] == team2), None)
        if existing_pick and abs(spread) > abs(existing_pick[2]):
            # Replace the existing pick
            final_picks.remove(existing_pick)
            already_picked.remove(existing_pick[1])
            already_picked.append(team2)
            final_picks.append((week, team2, spread))

# Print the final picks
for pick in final_picks:
    week_number, winning_team, spread = pick
    if spread > 0:
        winning_team = team1
    else:
        winning_team = team2
    print(f"Week {week_number} | {winning_team} spread: {spread}")
