from bs4 import BeautifulSoup
import requests

# Prompt the user for a URL
url = input("Enter the URL of the page to scrape: ")

try:
    # Fetch the page content
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for HTTP issues
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate all games in the HTML
    games = soup.find_all('div', class_='PigJe')

    # Parse game details
    for game in games:
        # Extract team names
        teams = game.find_all('span', class_='RMSXo')
        if len(teams) >= 2:
            team1 = teams[0].get_text(strip=True)
            team2 = teams[1].get_text(strip=True)

            # Extract spreads
            spreads = game.find_all('div', class_='nfCSQ')  # Select the spreads only
            if len(spreads) >= 2:
                team1_spread = spreads[0].get_text(strip=True)
                team2_spread = spreads[1].get_text(strip=True)

                # Print the results
                print(f"Matchup: {team1} vs {team2}")
                print(f"Spreads: {team1} {team1_spread}, {team2} {team2_spread}\n")

except requests.exceptions.RequestException as e:
    print(f"Error fetching URL: {e}")
