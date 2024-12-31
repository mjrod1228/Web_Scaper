import requests
from bs4 import BeautifulSoup
import sqlite3

# Database setup
DB_NAME = "scraper_results.db"

def setup_database():
    """Set up the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scraped_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_database(data):
    """Save the scraped data to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO scraped_data (title, link)
        VALUES (?, ?)
    ''', data)
    conn.commit()
    conn.close()

# Scraping setup
URL = "https://example.com"

def scrape_website(url):
    """Scrape the website and return extracted data."""
    print(f"Scraping {url}...")
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    soup = BeautifulSoup(response.text, "html.parser")

    # Example: Extract titles and links from a page
    articles = soup.find_all("article")  # Adjust based on the website structure
    results = []
    for article in articles:
        title = article.find("h2").text.strip()  # Adjust the tag as needed
        link = article.find("a")["href"]
        results.append((title, link))
    
    print(f"Scraped {len(results)} items.")
    return results

# Main workflow
if __name__ == "__main__":
    try:
        # Setup database
        setup_database()
        
        # Scrape website
        scraped_data = scrape_website(URL)
        
        # Save to database
        save_to_database(scraped_data)
        
        print("Data saved to database successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
