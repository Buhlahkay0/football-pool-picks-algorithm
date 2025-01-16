import pandas as pd


input_csv = "team_matchups.csv"  # CSV name
df = pd.read_csv(input_csv, index_col=0)


schedule_df = pd.DataFrame(columns=["Week", "Team 1", "Team 2"])


for week in df.columns:
    # week_number = int(week[1:])
    week_number = int(week)
    for team_1, team_2 in zip(df.index, df[week]):
        if "@" not in str(team_2) and str(team_2).strip() != "nan":  # Check if "@" is not present and the cell is not empty
            schedule_df = pd.concat([schedule_df, pd.DataFrame({"Week": [week_number], "Team 1": [team_1.strip()], "Team 2": [str(team_2).strip()]})], ignore_index=True)


output_csv = "schedule.csv" # output file
schedule_df.to_csv(output_csv, index=False)
