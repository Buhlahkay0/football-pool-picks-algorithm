import csv
import requests
from bs4 import BeautifulSoup

def scrape_week_data(week_number, url):
    """Scrape matchup and spread data for a given week and URL."""
    try:
        # Fetch the page content
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the header corresponding to the week
        header = soup.find('div', string=f"ESPN BET NFL Odds - Week {week_number}")
        if not header:
            print(f"No data found for Week {week_number} at {url}.")
            return []
        else:
            # Find the parent section containing the odds module
            odds_module = header.find_next('div', {'data-testid': 'oddsModule'})
            if not odds_module:
                print(f"No odds data found for Week {week_number} at {url}.")
                return []
            else:
                # Extract game data within the odds module
                games = odds_module.find_all('div', {'data-testid': lambda x: x and x.startswith('betSixPack')})
                results = []
                for game in games:
                    # Extract team names
                    teams = game.find_all('span', class_='RMSXo')
                    if len(teams) >= 2:
                        team1 = teams[0].get_text(strip=True)
                        team2 = teams[1].get_text(strip=True)

                        # Extract spreads (only the first spread is accurate)
                        spreads = game.find_all('div', class_='nfCSQ')
                        if spreads:
                            team1_spread = spreads[0].get_text(strip=True)
                            # Save the matchup and spread
                            results.append((team1, team2, team1_spread))
                return results

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return []

# Hardcoded path to the CSV file
csv_file = "urls.csv"

try:
    # Open and read the CSV file
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)

        # First row contains the weeks
        weeks = data[0]

        # Process each week and its URLs
        for week_index, week in enumerate(weeks):
            print(f"\nScraping data for Week {week}...\n")
            for row in data[1:]:  # Skip the header row
                if week_index < len(row):
                    url = row[week_index].strip()
                    if url and url.startswith("http"):  # Skip empty or invalid cells
                        print(f"Scraping URL: {url}\n")
                        matchups = scrape_week_data(week, url)
                        if matchups:
                            print(f"Matchups for Week {week}:")
                            for matchup in matchups:
                                team1, team2, team1_spread = matchup
                                # Align output for formatting
                                print(f"{team1:<25} vs {team2:<25} Spread: {team1_spread:<5}")
                        print()  # Add a newline between URLs
            print("\n")  # Add two newlines between weeks

except FileNotFoundError:
    print("Error: 'urls.csv' file not found. Please ensure the file is in the current directory.")
except Exception as e:
    print(f"Error processing the CSV file: {e}")
