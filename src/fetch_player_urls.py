import requests
from bs4 import BeautifulSoup
import time

# Function to get the HTML of a page
def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error fetching {url}: {response.status_code}")
        return None

# Function to scrape player URLs from a letter page (A-Z)
def scrape_player_urls_by_letter(letter):
    url = f"https://www.basketball-reference.com/players/{letter}/"
    html = get_html(url)
    if not html:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the table that contains player links
    player_table = soup.find('table', {'id': 'players'})
    player_links = []

    # Extract player profile URLs
    if player_table:
        for row in player_table.find('tbody').find_all('tr'):
            active_check = row.find('td', {'data-stat': 'year_max'})
            max_year = int(active_check.text)
            if max_year <= 2020:
                continue
            player_anchor = row.find('th').find('a')
            if player_anchor:
                player_url = "https://www.basketball-reference.com" + player_anchor['href']
                player_links.append(player_url)
    
    return player_links

# Function to get URLs for all players (A-Z)
def scrape_all_player_urls():
    all_player_urls = []
    
    # Loop over A-Z to scrape each letter's player page
    for letter in "abcdefghijklmnopqrstuvwxyz":
        print(f"Scraping player URLs from letter: {letter.upper()}")
        player_urls = scrape_player_urls_by_letter(letter)
        all_player_urls.extend(player_urls)
        
        # Pause between requests to avoid overwhelming the server
        time.sleep(2)
    
    print(f"Total players found: {len(all_player_urls)}")
    return all_player_urls

# Example usage:
player_urls = scrape_all_player_urls()

# Save the URLs to a file for later use
with open('data/player_urls.txt', 'w') as f:
    for url in player_urls:
        f.write(f"{url}\n")

print("Player URLs saved to player_urls.txt")
