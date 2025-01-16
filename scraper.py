import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


# Function to scrape and extract h2 elements from a URL
def scrape_h2_elements(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with class "article-meta"
        article_meta_div = soup.find('div', class_='article-body')

        #print(article_meta_div)

        # Check if the div was found
        if article_meta_div:
            # Find all h2 elements within the div
            h2_elements = article_meta_div.find_all('h2')

            print(len(h2_elements))

            # Extract the text from <a> elements within h2 elements
            a_texts = []
            for h2 in h2_elements:
                a_element = h2.find('a')
                if a_element:
                    a_texts.append(a_element.get_text())
                else:
                    a_texts.append('')

            return a_texts


        else:
            print("Div with class 'article-meta' not found.")
            return []

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

# Function to save extracted data to a CSV file
def save_to_csv(data, output_file):
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow([row])
        print(f'Data saved to {output_file}')

    except Exception as e:
        print(f"An error occurred while saving to CSV: {str(e)}")

if __name__ == "__main__":
    # Input URL
    input_url = input("Enter the URL: ")

    # Output CSV file
    output_file = "rankings.csv"

    # Scrape h2 elements
    h2_elements = scrape_h2_elements(input_url)

    if h2_elements:
        # Save to CSV
        save_to_csv(h2_elements, output_file)
    else:
        print("No data to save.")
