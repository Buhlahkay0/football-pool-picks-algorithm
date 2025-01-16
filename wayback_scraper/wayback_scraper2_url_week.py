import requests
from bs4 import BeautifulSoup

# Prompt the user for a URL and a week number
url = input("Enter the URL of the page to scrape: ")
week_number = input("Enter the week number (e.g., 4): ")

try:
    # Fetch the page content
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the header corresponding to the week
    header = soup.find('div', text=f"ESPN BET NFL Odds - Week {week_number}")
    if not header:
        print(f"No data found for Week {week_number}. Please check the input or the webpage.")
    else:
        # Find the parent section containing the odds module
        odds_module = header.find_next('div', {'data-testid': 'oddsModule'})
        if not odds_module:
            print(f"No odds data found for Week {week_number}.")
        else:
            # Extract game data within the odds module
            games = odds_module.find_all('div', {'data-testid': lambda x: x and x.startswith('betSixPack')})
            for game in games:
                # Extract team names
                teams = game.find_all('span', class_='RMSXo')
                if len(teams) >= 2:
                    team1 = teams[0].get_text(strip=True)
                    team2 = teams[1].get_text(strip=True)

                    # Extract spreads
                    spreads = game.find_all('div', class_='nfCSQ')  # Adjust class for spreads
                    if len(spreads) >= 2:
                        team1_spread = spreads[0].get_text(strip=True)
                        team2_spread = spreads[1].get_text(strip=True)

                        # Print the matchup and spreads
                        print(f"Matchup: {team1} vs {team2}")
                        print(f"Spreads: {team1} {team1_spread}, {team2} {team2_spread}\n")

except requests.exceptions.RequestException as e:
    print(f"Error fetching URL: {e}")
