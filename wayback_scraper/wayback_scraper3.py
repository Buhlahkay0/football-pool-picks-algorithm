import requests
from bs4 import BeautifulSoup
import pyperclip  # Install this package if not already: pip install pyperclip

# Prompt the user for a URL and a week number
url = input("Enter the URL of the page to scrape: ")
week_number = input("Enter the week number (e.g., 5): ")

try:
    # Fetch the page content
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the header corresponding to the week
    header = soup.find('div', string=f"ESPN BET NFL Odds - Week {week_number}")
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
            
            # Store formatted output for terminal and plain output for clipboard
            formatted_output = f"Matchups for Week {week_number}:\n"
            plain_output = []
            for game in games:
                # Extract team names
                teams = game.find_all('span', class_='RMSXo')
                if len(teams) >= 2:
                    team1 = teams[0].get_text(strip=True)
                    team2 = teams[1].get_text(strip=True)

                    # Extract spreads (use only the first spread)
                    spreads = game.find_all('div', class_='nfCSQ')
                    if spreads:
                        team1_spread = spreads[0].get_text(strip=True)

                        # Format the output
                        formatted_output += f"{team1:<25} vs {team2:<30} Spread: {team1_spread:<5}\n"
                        plain_output.append(f"{team1}\t{team2}\t{team1_spread}")
            
            # Print the formatted output to the terminal
            print(formatted_output)
            
            # Copy plain data to the clipboard
            pyperclip.copy("\n".join(plain_output))
            print("\nThe plain data has been copied to your clipboard. You can paste it into Google Sheets.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching URL: {e}")
