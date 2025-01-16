import pandas as pd
import pulp

# Read the CSV file
input_csv = "games.csv"
df = pd.read_csv(input_csv)

# Manually Input
already_picked = ["CIN", "NYJ", "CLE", "HOU", "CHI", "ATL"]
weeks_picked = [1, 2, 3, 4, 5, 6]

already_picked = ["CIN", "NYJ", "CLE", "HOU", "CHI", "ATL", "WAS", "PIT", "BUF", "MIN", "DET", "DEN", "KC", "TB", "BAL", "GB", "PHI"]
weeks_picked = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

# Test
# already_picked = ["PHI", "SF", "DAL", "CIN", "WAS", "MIA", "BUF", "BAL", "CLE", "SEA", "DET", "CLE"]
# weeks_picked = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

remaining_weeks = set(df['Week']) - set(weeks_picked)

# Generate possible picks per week
possible_picks = {}
teams = set()
pick_spreads = {}  # Dictionary to store spreads for each (week, team)

for week in remaining_weeks:
    week_games = df[df['Week'] == week]
    possible_picks[week] = []
    for _, row in week_games.iterrows():
        team1 = row['Team 1']
        team2 = row['Team 2']
        spread = row['Spread']
        if spread < 0 and team1 not in already_picked:
            possible_picks[week].append((team1, abs(spread)))
            teams.add(team1)
            pick_spreads[(week, team1)] = abs(spread)
        elif spread > 0 and team2 not in already_picked:
            possible_picks[week].append((team2, abs(spread)))
            teams.add(team2)
            pick_spreads[(week, team2)] = abs(spread)

# Define the problem
prob = pulp.LpProblem("Maximize_Minimum_Spread", pulp.LpMaximize)

# Decision variables
x = {}
for week in possible_picks:
    for team, spread in possible_picks[week]:
        x[(week, team)] = pulp.LpVariable(f"x_{week}_{team}", cat='Binary')

# Variables y[week] and s_min
y = {}
for week in possible_picks:
    y[week] = pulp.LpVariable(f"y_{week}", lowBound=0)
s_min = pulp.LpVariable("s_min", lowBound=0)

# Objective function
prob += s_min

# Constraints
# One pick per week
for week in possible_picks:
    prob += pulp.lpSum([x[(week, team)] for team, _ in possible_picks[week]]) == 1

# No team picked more than once
for team in teams:
    prob += pulp.lpSum([x[(week, team)] for week in possible_picks if (week, team) in x]) <= 1

# Relate y[week] to the spreads
for week in possible_picks:
    prob += y[week] == pulp.lpSum([spread * x[(week, team)] for team, spread in possible_picks[week]])

# Ensure s_min is less than or equal to each y[week]
for week in possible_picks:
    prob += s_min <= y[week]

# Solve the problem
prob.solve()

# Print the results
if pulp.LpStatus[prob.status] == 'Optimal':
    picks = []
    for v in prob.variables():
        if v.name.startswith('x_') and v.varValue == 1:
            # Extract week and team from the variable name
            week_team = v.name.lstrip('x_')
            # Handle team names that may include underscores
            week_str, team = week_team.split('_', 1)
            week = int(week_str)
            spread = pick_spreads[(week, team)]
            picks.append((week, team, spread))
    
    # Sort picks by week
    picks.sort(key=lambda x: x[0])
    
    # Print using the desired format
    format_string = "Week {:<2} | {:<3}   spread - {:>2}"
    for week, team, spread in picks:
        print(format_string.format(week, team, int(abs(spread))))
    print(f"Minimum spread achieved: {pulp.value(s_min)}")
    
    # Calculate and print the total spread
    total_spread = sum(spread for _, _, spread in picks)
    print(f"Total spread achieved: {total_spread}")
else:
    print("No valid pick set found.")