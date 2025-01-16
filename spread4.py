import pandas as pd


input_csv = "games.csv"  # CSV file
df = pd.read_csv(input_csv)

df = df.sort_values(by=['Spread'], key=lambda x: abs(x), ascending=False)

already_picked = ["PHI", "SF", "DAL", "CIN", "WAS", "MIA", "BUF", "BAL", "CLE", "SEA"]  # manually update
weeks_picked = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # manually update
final_picks = []

for index, row in df.iterrows():
    week = row['Week']
    team1 = row['Team 1']
    team2 = row['Team 2']
    spread = row['Spread']
    
    # check if the week or winning team is already picked
    if week not in weeks_picked and (spread < 0 and team1 not in already_picked or spread > 0 and team2 not in already_picked):

        final_picks.append((week, spread, team1 if spread < 0 else team2))
        
        # update arrays
        weeks_picked.append(week)
        already_picked.append(team1 if spread < 0 else team2)

# sort final_picks by week
final_picks.sort(key=lambda x: x[0])

for pick in final_picks:
    week_number, spread, winning_team = pick
    format_string = "Week {:<2} | {:<3}   spread - {:>2}"
    print(format_string.format(week_number, winning_team, int(abs(spread))))

