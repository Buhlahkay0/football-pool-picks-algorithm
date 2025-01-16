from bs4 import BeautifulSoup

# Load the HTML file
with open('wayback_scraper/spreads.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Locate all games in the HTML
games = soup.find_all('div', class_='PigJe')

# Parse game details
for game in games:
    # Extract the teams
    teams = game.find_all('span', class_='RMSXo')
    if len(teams) >= 2:
        team1 = teams[0].get_text()
        team2 = teams[1].get_text()

        # Extract the spreads
        spreads = game.find_all('div', id='topOdd')
        if spreads:
            team1_spread = spreads[0].get_text()
            team2_spread = spreads[1].get_text()

            # Print the results
            print(f"Matchup: {team1} vs {team2}")
            print(f"Spreads: {team1} {team1_spread}, {team2} {team2_spread}\n")
