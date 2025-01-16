import pandas as pd
import itertools
import sys
import time

# Read the CSV file
input_csv = "games.csv"
df = pd.read_csv(input_csv)

# Manually Input
already_picked = ["PHI", "SF", "DAL", "CIN", "WAS", "MIA", "BUF", "BAL", "CLE", "SEA", "DET"]
weeks_picked = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

remaining_weeks = set(df['Week']) - set(weeks_picked)

# Generate all possible picks for remaining weeks
def generate_possible_picks(df, already_picked, remaining_weeks):
    possible_picks = []
    for week in remaining_weeks:
        week_games = df[df['Week'] == week]
        for _, row in week_games.iterrows():
            team1 = row['Team 1']
            team2 = row['Team 2']
            spread = row['Spread']
            if spread < 0 and team1 not in already_picked:  # Negative spread, Team 1 wins
                possible_picks.append((week, spread, team1))
            elif spread > 0 and team2 not in already_picked:  # Positive spread, Team 2 wins
                possible_picks.append((week, spread, team2))
    return possible_picks

possible_picks = generate_possible_picks(df, already_picked, remaining_weeks)

# Prune the possible picks by ensuring each week has at least one valid pick
valid_weeks = set(pick[0] for pick in possible_picks)
pruned_remaining_weeks = remaining_weeks.intersection(valid_weeks)
if len(pruned_remaining_weeks) < len(remaining_weeks):
    print("Some weeks have no valid picks. Pruning applied.")
    remaining_weeks = pruned_remaining_weeks

# Evaluate each set of picks
def evaluate_picks(pick_set):
    min_spread = min(abs(pick[1]) for pick in pick_set)
    total_spread = sum(abs(pick[1]) for pick in pick_set)
    return min_spread, total_spread

# Find the best set of picks
best_set = None
best_evaluation = (0, 0)  # Initialize with (min spread, total spread)

# Progress calculation
total_combinations = 1
for i in range(len(remaining_weeks)):
    total_combinations *= len(remaining_weeks)

print("Total Combinations: " + f"{total_combinations:,}")

current_combination = 0

start_time = time.time()

for pick_set in itertools.combinations(possible_picks, len(remaining_weeks)):
    pick_weeks = set(pick[0] for pick in pick_set)
    pick_teams = set(pick[2] for pick in pick_set)
    # Ensure one pick per week and no repeated teams
    if len(pick_weeks) == len(remaining_weeks) and len(pick_teams) == len(pick_set):  
        evaluation = evaluate_picks(pick_set)
        if evaluation > best_evaluation:
            best_evaluation = evaluation
            best_set = pick_set
    
    # progress
    current_combination += 1

    if current_combination % 1000000 == 0:
        percentage_complete = (current_combination / total_combinations) * 100
        sys.stdout.write(f"\rPercentage complete: {percentage_complete:.2f}%")
        sys.stdout.flush()  # Flush the output buffer to ensure it prints immediately

print("\n")

# Update final picks and print
if best_set:
    for pick in sorted(best_set, key=lambda x: x[0]):
        week, spread, winning_team = pick

        format_string = "Week {:<2} | {:<3}   spread - {:>2}"
        print(format_string.format(week, winning_team, int(abs(spread))))

        weeks_picked.append(week)
        already_picked.append(winning_team)
else:
    print("No valid pick set found.")

# End timer and calculate total time
end_time = time.time()
total_seconds = end_time - start_time

# Calculate hours, minutes, and seconds
hours = int(total_seconds // 3600)
minutes = int((total_seconds % 3600) // 60)
seconds = total_seconds % 60

# Print the total time in hours:minutes:seconds format
print(f"\nTotal time taken for calculation: {hours}:{minutes:02}:{seconds:.2f}")
