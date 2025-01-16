import requests
from bs4 import BeautifulSoup
import pyperclip  # Install this package if not already: pip install pyperclip

# Custom headers to prevent 403 errors
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Prompt the user for a URL
# url = input("Enter the URL of the page to scrape: ")
url = "https://www.espn.com/nfl/odds"

try:
    # Fetch the page content with custom headers
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the parent section containing the odds module
    odds_module = soup.find('div', {'data-testid': 'oddsModule'})
    if not odds_module:
        print(f"No odds data found. Please check the input URL.")
    else:
        # Extract game data within the odds module
        games = odds_module.find_all('div', {'data-testid': lambda x: x and x.startswith('betSixPack')})
        
        # Store formatted output for terminal and plain output for clipboard
        formatted_output = "Matchups:\n"
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
