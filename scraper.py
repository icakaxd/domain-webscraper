import requests
from bs4 import BeautifulSoup
import re
import os
import time, random
from urllib.parse import urlparse, urljoin

# List of URLs to scrape
urls = [
    "https://harmonica.bg/products/",
    "https://www.italia-bg.com/index.php?route=product/manufacturer/info&manufacturer_id=12",
    "https://shop.cherga.bg/produkt-kategoriya/%D0%B5%D0%BA%D0%BE-%D1%84%D0%B5%D1%80%D0%BC%D0%B0/",
    "https://villamelnik.com/vinen-magazin/",
    "https://www.otmanastira.com/%d0%bc%d0%b0%d0%b3%d0%b0%d0%b7%d0%b8%d0%bd/",
    "https://angus.bg/?lang=bg",
    "https://bredas.bg/magazin/",
    "https://www.facebook.com/magazinipopov/posts/120725726357876/",
    "http://www.mandravarbina.eu/portfolio.html",
    "https://tatkovatagradina.bg/magazin/krave-kiselo-mlyako-gerzovica-46/",
    "https://obedinenifermi-produkti.bg/",
    "https://receptite.com/%d1%80%d0%b5%d1%86%d0%b5%d0%bf%d1%82%d0%b0/%d0%b4%d0%be%d0%bc%d0%b0%d1%88%d0%bd%d0%be-%d1%84%d0%b8%d0%bb%d0%b5-%d0%b5%d0%bb%d0%b5%d0%bd%d0%b0",
    "https://smartorganic.bg/",
    "https://smartorganic.bg/shop/",
    "https://smartorganic.bg/organic-shop/",
    "https://sweettwins.eu/%d0%bc%d0%b0%d0%b3%d0%b0%d0%b7%d0%b8%d0%bd/",
    "https://mandraborino.com/",
    "https://jaltusha.bg/",
    "https://borovitza.com/%d0%bf%d1%80%d0%be%d0%b4%d1%83%d0%ba%d1%82%d0%b8/",
    "https://mesar.bg/%d0%ba%d0%be%d1%81-%d1%81%d0%bc%d0%be%d0%bb%d1%8f%d0%bd/",
    "https://www.ecosem.bg/bg/c-4/%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B8/",
    "https://fermagurmazovo.com/%d0%bf%d1%80%d0%be%d0%b4%d1%83%d0%ba%d1%82%d0%b8/",
    "https://rostar-bg.com/",
    "https://shop.labottega.bg/vendor/rummo",
    "https://blagite.com/",
    "https://ambrozia.bg/",
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
