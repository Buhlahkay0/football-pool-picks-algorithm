import random
from collections import defaultdict
from itertools import product

# Function to calculate win probability based on rankings
def calculate_win_probability(rank_team1, rank_team2):
    """
    Calculate the probability of team1 winning against team2.
    Higher-ranked teams have better odds (lower rank value is better).
    This function can be modified later.
    """
    diff = rank_team2 - rank_team1
    return 1 / (1 + 10 ** (diff / 10))  # Logistic-style model

# Generate all possible outcomes for a single round
def generate_outcomes(matchups, power_rankings):
    """
    Generate all possible outcomes for the given matchups with their probabilities.
    """
    outcomes = []

    for matchup in matchups:
        team1, team2 = matchup
        prob_team1_wins = calculate_win_probability(power_rankings[team1], power_rankings[team2])
        outcomes.append([(team1, prob_team1_wins), (team2, 1 - prob_team1_wins)])

    return list(product(*outcomes))

# Recursive function to simulate all possible outcomes of the playoffs
def simulate_all_outcomes(bracket, power_rankings):
    """
    Simulate all possible outcomes for the playoff bracket and calculate probabilities.
    """
    round_results = defaultdict(float)  # team -> cumulative probability of reaching a round

    def helper(current_bracket, round_number, probability):
        for team in current_bracket:
            round_results[(team, round_number)] += probability

        if len(current_bracket) == 1:
            # Final round: record the winner
            return

        next_round = []
        matchups = []

        # Create matchups, handling the case of an odd number of teams
        for i in range(0, len(current_bracket) - 1, 2):
            matchups.append((current_bracket[i], current_bracket[i + 1]))

        # If there is an odd team out, it gets a bye
        if len(current_bracket) % 2 == 1:
            next_round.append(current_bracket[-1])

        outcomes = generate_outcomes(matchups, power_rankings)

        for outcome in outcomes:
            outcome_probability = probability
            next_round_teams = next_round[:]

            for team, prob in outcome:
                outcome_probability *= prob
                next_round_teams.append(team)

            helper(next_round_teams, round_number + 1, outcome_probability)

    # Start the recursive simulation
    initial_teams = [team for match in bracket for team in match]

    # Add teams with byes to the first round's results and propagate them to the next round
    teams_with_byes = list(set(power_rankings.keys()) - set(initial_teams))
    for team in teams_with_byes:
        round_results[(team, 1)] += 1.0

    helper(initial_teams + teams_with_byes, 1, 1.0)

    # Aggregate results for easier interpretation
    final_results = defaultdict(lambda: defaultdict(float))
    for (team, round_number), prob in round_results.items():
        final_results[round_number][team] += prob

    return final_results

# Example data
power_rankings = {
    "DET": 1, "KC": 1,  # Top seeds
    "PHI": 2, "BUF": 2,
    "LAR": 3, "BAL": 3,
    "ATL": 4, "HOU": 4,
    "MIN": 5, "PIT": 5,
    "GB": 6, "LAC": 6,
    "WSH": 7, "DEN": 7
}

# Initial playoff bracket (rounds: list of matchups)
# NFC and AFC brackets
initial_bracket = [
    ["MIN", "ATL"], ["GB", "LAR"], ["WSH", "PHI"],  # NFC Wild Card
    ["PIT", "HOU"], ["LAC", "BAL"], ["DEN", "BUF"]   # AFC Wild Card
]

# Simulate all outcomes
probabilities = simulate_all_outcomes(initial_bracket, power_rankings)

# Print the results
rounds = sorted(probabilities.keys())
for round_ in rounds:
    print(f"Round {round_}:")
    for team in sorted(probabilities[round_].keys(), key=lambda x: x):
        print(f"  {team}: {probabilities[round_][team]:.2%}")
