import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to get the HTML of a page
def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error fetching {url}: {response.status_code}")
        return None

# Function to extract player stats from a game log page
def extract_player_stats(player_url):
    html = get_html(player_url)
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the game logs table
    table = soup.find('table', {'id': 'pgl_basic'})
    
    # Store rows
    player_data = []
    headers = []
    
    if table:
        # Find table headers (column names)
        headers = [th.getText() for th in table.find('thead').find_all('th')]
        
        # Find all rows in the table
        rows = table.find('tbody').find_all('tr', class_=lambda x: x != 'thead')
        
        # Iterate over rows and extract data
        for row in rows:
            cols = [col.getText() for col in row.find_all('td')]
            if cols:  # Only add non-empty rows
                player_data.append(cols)
    
    return player_data, headers

# Main function to scrape player stats across matches and save as CSV
def scrape_player_game_logs(player_urls, output_file='player_stats.csv'):
    all_player_data = []
    
    # Loop over player URLs to collect data
    for player_url in player_urls:
        print(f"Scraping data from: {player_url}")
        player_stats, headers = extract_player_stats(player_url)
        all_player_data.extend(player_stats)
        
        # Pause between requests to avoid overwhelming the server
        time.sleep(0.5)
    
    # Convert to a DataFrame and save to CSV
    if all_player_data:
        df = pd.DataFrame(all_player_data, columns=[
            'GameNumber', 'Date', 'Age', 'Team', 'Home/Away', 'Opponent', 'Result', 'GS', 'MP', 'FG', 'FGA', 'FG%', 
            '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 
            'BLK', 'TOV', 'PF', 'PTS', 'GmSc', '+/-'
        ])
        df.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")
    else:
        print("No data found")

# Example usage:
player_urls = [
    'https://www.basketball-reference.com/players/j/jamesle01/gamelog/2024',  # LeBron James game log (2024)
    # Add more player URLs here
]
player_urls = open('data/player_urls.txt', 'r').read().split('\n')

urls_to_log = []
for player in player_urls:
    for stat_year in ['2023','2024']:
        url = player.replace('.html', f'/gamelog/{stat_year}')
        urls_to_log.append(url)

scrape_player_game_logs(urls_to_log, 'data/player_stats.csv')
