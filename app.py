from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import os


def read_config(file_path):
    config = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Remove any surrounding whitespace and ignore empty lines or comments
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config


def parse_range(range_str):
    """Parse a range string formatted as 'min,max' into a tuple of integers."""
    parts = range_str.split(',')
    if len(parts) != 2:
        raise ValueError(f"Invalid range format: {range_str}")
    return (int(parts[0].strip()), int(parts[1].strip()))


def load_urls(file_path):
    """Load URLs from a given file into a set. If the file doesn't exist, return an empty set."""
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r', encoding='utf-8') as file:
        return set(line.strip() for line in file if line.strip())


def append_url(file_path, url):
    """Append a single URL to the specified file."""
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(url + '\n')


# Configuration Files
CONFIG_FILE = 'config.txt'
FIT_ARTICLES_FILE = 'fit_articles.txt'
CHECKED_ARTICLES_FILE = 'checked_articles.txt'

# Read configuration
config = read_config(CONFIG_FILE)

initial_url = config.get('initial_url')
if not initial_url:
    raise ValueError("initial_url is not defined in the config file.")

n_pages = config.get('n_pages')
if n_pages:
    try:
        n_pages = int(n_pages)
    except ValueError:
        raise ValueError("n_pages must be an integer.")

# Parse measurement ranges
try:
    arm_range = parse_range(config.get('arm_range', '0,0'))
    waist_range = parse_range(config.get('waist_range', '0,0'))
    shoulder_range = parse_range(config.get('shoulder_range', '0,0'))
    leg_range = parse_range(config.get('leg_range', '0,0'))
except ValueError as e:
    raise ValueError(f"Error parsing ranges: {e}")

ranges = [arm_range, waist_range, shoulder_range, leg_range]

# Load previously fit and checked articles
fit_articles = load_urls(FIT_ARTICLES_FILE)
checked_articles = load_urls(CHECKED_ARTICLES_FILE)

# Set up the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    page = 1
    while True:
        # Insert the page number into the URL
        if "page=" in initial_url:
            url = initial_url.replace("page=", f"page={page}&")
        else:
            # Check if the initial_url already has query parameters
            if '?' in initial_url:
                url = initial_url + f"&page={page}"
            else:
                url = initial_url + f"?page={page}"

        print(f"\nNavigating to page {page}: {url}")

        # Open the web page and wait for it to load
        driver.get(url)
        time.sleep(3)  # Adjust time as necessary based on your network speed and page response time

        # Get the page source after JavaScript execution
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Process the content using BeautifulSoup
        articles_found = False  # Flag to check if any articles are present on the page
        for article in soup.find_all("div", class_="item-tile-container"):
            articles_found = True
            article_tag = article.find('a')

            if not article_tag or 'href' not in article_tag.attrs:
                continue

            article_href_tail = article_tag["href"]
            if "sell" in article_href_tail:
                continue

            article_url = "https://www.sellpy.se" + article_href_tail

            # Check if the article has already been checked
            if article_url in checked_articles:
                print(f"Already checked: {article_url}")
                continue  # Skip to the next article

            # Mark this article as checked
            append_url(CHECKED_ARTICLES_FILE, article_url)
            checked_articles.add(article_url)

            # Navigate to the article URL
            driver.get(article_url)
            time.sleep(0.5)  # Adjust based on the observed load time for the page

            # Parse the new page content
            article_html = driver.page_source
            article_soup = BeautifulSoup(article_html, 'html.parser')
            print(f"Processing article: {article_url}")

            # Extract the desired table(s)
            article_sizing_tables = article_soup.find_all('table')

            # Filter tables containing "Man"
            article_sizing_table = [x for x in article_sizing_tables if "Man" in x.get_text()]
            if len(article_sizing_table) != 1:
                print(f"Skipping article due to unexpected sizing tables: {article_url}")
                continue  # Skip if not exactly one sizing table found

            article_sizing_table = article_sizing_table[0]
            article_sizing_rows = article_sizing_table.find_all('tr')

            # Extract measurement values
            article_sizing_values = []
            for row in article_sizing_rows:
                cols = row.find_all('p')
                if len(cols) >= 2:
                    value = cols[1].get_text(strip=True)
                    if value.isdigit():
                        article_sizing_values.append(int(value))

            measurements = article_sizing_values

            if len(measurements) != 4:
                print(f"Skipping article due to insufficient measurements: {article_url}")
                continue  # Skip if not exactly 4 measurements found

            # Check if measurements fit within the specified ranges
            fit = True
            for i in range(4):
                if not (ranges[i][0] <= measurements[i] <= ranges[i][1]):
                    fit = False
                    break

            if fit:
                if article_url not in fit_articles:
                    append_url(FIT_ARTICLES_FILE, article_url)
                    fit_articles.add(article_url)
                    print(f"Added to fit_articles: {article_url}")
                else:
                    print(f"Article already in fit_articles: {article_url}")
            else:
                print(f"Article does not fit: {article_url}")

        if not articles_found:
            print(f"No articles found on page {page}. Terminating the scraper.")
            break  # Terminate if no articles are found on the current page

        # Optional: If n_pages is set, enforce the maximum number of pages
        if n_pages and page >= n_pages:
            print(f"Reached the maximum number of pages: {n_pages}. Terminating the scraper.")
            break

        page += 1  # Move to the next page

    print("\nScraping completed.")
    print(f"Total fitting articles found: {len(fit_articles)}")
    print("These articles fit the specified measurements:")
    for article in fit_articles:
        print(article)

finally:
    # Clean up: close the browser window
    driver.quit()
