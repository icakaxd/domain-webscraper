import requests
from bs4 import BeautifulSoup
import re
import os
import time, random
from urllib.parse import urlparse, urljoin

# List of URLs to scrape
urls = [
    "",
    # Put URLs here.
]

def get_links(url):
    """Scrape a webpage and retrieve all linked URLs."""
    response = requests.get(url)
    response.encoding = 'utf-8'  # Use utf-8 encoding
    soup = BeautifulSoup(response.text, 'html.parser')

    links = set()  # use a set to avoid duplicates

    # Find all 'a' tags and extract the href attribute
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if href and not href.endswith(('.pdf', '.jpg', '.jpeg', '.png', '.gif', '.svg')):  # ignore PDF files and images
            full_url = urljoin(url, href)
            if urlparse(full_url).netloc == urlparse(url).netloc:  # ignore external links
                links.add(full_url)
    
    return links


def scrape_text(url):
    """Scrape text from a webpage."""
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'  # Use utf-8 encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all text
        text = soup.get_text(separator=' ')
        
        # Replace sequences of two or more newlines with a single newline
        text = re.sub('\n{2,}', '\n', text)
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        text = ""
    return text


def remove_empty_lines(filename):
    """Overwrite the file, removing empty lines and lines that contain only whitespace."""
    with open(filename, 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            if line.strip():
                f.write(line)
        f.truncate()

def scrape_site(url, scraped_urls, f):
    """Scrape a website and all internal URLs."""
    if url not in scraped_urls:
        print(f"Scraping URL: {url}")
        text = scrape_text(url)
        f.write(f'URL: {url}\n{text}\n')
        scraped_urls.add(url)
        for link in get_links(url):
            if link not in scraped_urls:
                scrape_site(link, scraped_urls, f)  # recursive call
                time.sleep(random.uniform(1.27, 8.73))  # wait before the next request

def main():
    """Scrape text from each URL and save to a file."""
    with open('training_data-xxx.txt', 'w', encoding='utf-8') as f:
        for url in urls:
            scrape_site(url, set(), f)
    remove_empty_lines('training_data-xxx.txt')
    print("Finished scraping all URLs.")

if __name__ == "__main__":
    main()
