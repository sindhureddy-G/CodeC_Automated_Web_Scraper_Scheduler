!pip install beautifulsoup4 selenium schedule

import requests
from bs4 import BeautifulSoup
import csv
import time
import schedule
from datetime import datetime


def scrape_quotes():
    url = "http://quotes.toscrape.com"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all('div', class_='quote')


    data = []
    for quote in quotes:
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]

        data.append({
            'quote': text,
            'author': author,
            'tags': ', '.join(tags),
            'scraped_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })


    filename = f"quotes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['quote', 'author', 'tags', 'scraped_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f"Scraped {len(data)} quotes and saved to {filename}")
    return data


def run_scheduler():

    schedule.every(1).minutes.do(scrape_quotes)

    print("Scheduler started. Press Ctrl+C to stop.")
    print("First run will happen immediately...")


    scrape_quotes()


    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped.")


print("Web Scraper Demonstration")
print("=" * 40)

print("Scraping quotes from http://quotes.toscrape.com...")
data = scrape_quotes()


print("\nSample of scraped data:")
for i, quote in enumerate(data[:3]):
    print(f"{i+1}. '{quote['quote']}' - {quote['author']}")
    print(f"   Tags: {quote['tags']}")
    print()


print("Simulating scheduled run after 10 seconds...")
time.sleep(10)
print("\nSecond run:")
data = scrape_quotes()
