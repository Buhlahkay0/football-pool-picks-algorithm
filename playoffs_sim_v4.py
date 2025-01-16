import itertools

# -------------------------------
# 1. Power Rankings
# -------------------------------
power_rankings = {
    "DET": 1, "KC": 1,  # Top seeds (byes)
    "PHI": 2, "BUF": 2,
    "LAR": 3, "BAL": 3,
    "ATL": 4, "HOU": 4,
    "MIN": 5, "PIT": 5,
    "GB": 6,  "LAC": 6,
    "WSH": 7, "DEN": 7
}
# power_rankings = {
#     "DET": 1, "KC": 2,  # Top seeds (byes)
#     "PHI": 3, "BUF": 4,
#     "LAR": 5, "BAL": 6,
#     "ATL": 7, "HOU": 8,
#     "MIN": 9, "PIT": 10,
#     "GB": 11,  "LAC": 12,
#     "WSH": 13, "DEN": 14
# }

# -------------------------------
# 2. Utility to compute P(A beats B)
# -------------------------------
def win_probability(teamA, teamB, power_rankings):
    """
    Given two teams and their power rankings,
    return probability that teamA beats teamB.
    Smaller power ranking => stronger team.
    """
    rankA = power_rankings[teamA]
    rankB = power_rankings[teamB]
    # Example formula:
    return rankB / float(rankA + rankB)

# -------------------------------
# 3. Organize teams by conference (example)
# -------------------------------
afc_teams = ["KC", "BUF", "BAL", "HOU", "PIT", "LAC", "DEN"]  # 7 teams
nfc_teams = ["DET", "PHI", "LAR", "ATL", "MIN", "GB", "WSH"]  # 7 teams

# -------------------------------
# 4. Probability dictionaries
# -------------------------------
rounds = [1, 2, 3, 4, 5]
round_names = {
    1: "Round 1 (Wild Card)",
    2: "Round 2 (Divisional)",
    3: "Round 3 (Conference Championships)",
    4: "Round 4 (Super Bowl)",
    5: "Win Super Bowl"
}

prob_reach_round = {
    team: {r: 0.0 for r in rounds}
    for team in power_rankings
}

# Everyone reaches Round 1 with probability 1.0
for team in power_rankings:
    prob_reach_round[team][1] = 1.0

# Byes for KC and DET => 100% reach Round 2
prob_reach_round["KC"][2] = 1.0
prob_reach_round["DET"][2] = 1.0

# -------------------------------
# 5. Round 1 (Wild Card) matchups
# -------------------------------
afc_R1_matchups = [
    ("BUF", "DEN"),  # #2 vs #7
    ("BAL", "LAC"),  # #3 vs #6
    ("HOU", "PIT"),  # #4 vs #5
]
nfc_R1_matchups = [
    ("PHI", "WSH"),  # #2 vs #7
    ("LAR", "GB"),   # #3 vs #6
    ("ATL", "MIN"),  # #4 vs #5
]

def process_round(matchups, round_num, next_round_num):
    """
    Given a list of matchups (like [("BUF","DEN"), ("BAL","LAC"), ...]),
    update each team's prob_reach_round for the next round.
    """
    for (teamA, teamB) in matchups:
        pA_reach = prob_reach_round[teamA][round_num]
        pB_reach = prob_reach_round[teamB][round_num]

        # Probability that this particular matchup actually occurs
        match_probability = pA_reach * pB_reach
        if match_probability == 0:
            continue

        pA_win = win_probability(teamA, teamB, power_rankings)
        pB_win = 1 - pA_win

        pA_advance = match_probability * pA_win
        pB_advance = match_probability * pB_win

        prob_reach_round[teamA][next_round_num] += pA_advance
        prob_reach_round[teamB][next_round_num] += pB_advance

# Process Round 1
process_round(afc_R1_matchups, round_num=1, next_round_num=2)
process_round(nfc_R1_matchups, round_num=1, next_round_num=2)

# -------------------------------
# 6. Round 2 (Divisional) matchups
# -------------------------------
afc_R2_matchups = [
    ("KC", "HOU"),  # placeholder
    ("BUF", "BAL"), # placeholder
]
nfc_R2_matchups = [
    ("DET", "ATL"), # placeholder
    ("PHI", "LAR"), # placeholder
]

process_round(afc_R2_matchups, round_num=2, next_round_num=3)
process_round(nfc_R2_matchups, round_num=2, next_round_num=3)

# -------------------------------
# 7. Round 3 (Conference Championships)
# -------------------------------
afc_R3_matchups = [
    ("KC", "BUF"),  # placeholder
]
nfc_R3_matchups = [
    ("DET", "PHI"), # placeholder
]

process_round(afc_R3_matchups, round_num=3, next_round_num=4)
process_round(nfc_R3_matchups, round_num=3, next_round_num=4)

# -------------------------------
# 8. Round 4 (Super Bowl)
# -------------------------------
super_bowl_matchup = [
    ("KC", "DET")  # placeholder
]

process_round(super_bowl_matchup, round_num=4, next_round_num=5)

# -------------------------------
# 9. Print Results by Round
# -------------------------------
for r in rounds:
    print(f"{round_names[r]}:")
    for team in power_rankings:
        print(f"  {team}: {prob_reach_round[team][r] * 100:.2f}%")
    print()
