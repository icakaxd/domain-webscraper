# Domain Web Scraper

This is a Python script to scrape text data from a list of URLs and save it to a file. It's designed to scrape all the pages within the same domain as the initial URL. It makes use of the `requests`, `BeautifulSoup`, `re`, `os`, `time`, `random`, and `urlparse` libraries.

## Features

- Scrapes all pages within the same domain as the initial URL.
- Ignores PDF files and external links.
- Writes scraped data to a text file, appending the URL of the source page to each piece of text.
- Waits for a random interval between 1.27 and 8.73 seconds between requests to avoid overloading the server.
- Removes empty lines and lines containing only whitespace from the output file.

## Usage

To use this script, you'll need Python 3.6+ installed on your machine.

First, install the required Python libraries with:

```bash
pip install requests beautifulsoup4
```


Then, you can run the script with:

```bash
python scrape.py
```


The script will scrape the websites listed in the `urls` variable in `scrape.py`. You can replace these URLs with any URLs of your choice.

The scraped data will be saved to a file named 'training_data-xxx.txt'. 

## Note

Please be aware of the terms of service of any website you're scraping, as web scraping is not allowed by all websites.
