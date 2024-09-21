from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

initial_url = "https://www.sellpy.se/search/Man/Kl%C3%A4der/Kavajer-%26-Kostymer/Kostymer?minPrice=200&material=Ull&material=Bomull&material=Linne&material=Kashmir&material=Mohair&material=Silke&material=Merinoull&color=Bl%C3%A5&color=Gr%C3%A5&brand=-H%26M&brand=-Zara+Man&brand=-Dressmann&brand=-Bl%C3%A4ck&brand=-Zara&brand=-GANT&brand=-H%26M+Man&brand=-Jack+%26+Jones&brand=-Premium+by+Jack+%26+Jones&brand=-Suitsupply&brand=-ESPRIT&brand=-Scotch+%26+Soda&brand=-H%26M+Modern+Classic&brand=-Riley&brand=-Bruuns+Bazaar&brand=-Calvin+Klein&condition=Mycket+bra&condition=Bra&condition=Nytt"
budget = 2000

# Set up the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


articles = []

n_pages = 23

arm_range = (67, 69)
waist_range = (86, 92)
shoulder_range = (48, 49)
leg_range = (83, 90)
ranges = [arm_range, waist_range, shoulder_range, leg_range]

for page in range(1, n_pages + 1):

    url = initial_url.replace("?", "?page=" + str(page) + "&")

    # Open the web page and wait for it to load
    driver.get(url)
    time.sleep(3)  # Adjust time as necessary based on your network speed and page response time

    # Get the page source after JavaScript execution
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    print()
    print("we are on page number ", page)

    # Process the content using BeautifulSoup
    for article in soup.find_all("div", class_="item-tile-container"):
        article_tag = article.find('a')

        article_href_tail = article_tag["href"]
        if "sell" in article_href_tail:
            continue

        article_url = "https://www.sellpy.se" + article_href_tail

        # here i want to go into to the article url and pull out a div on that page

        # Navigate to the article URL
        driver.get(article_url)
        time.sleep(0.5)  # Adjust based on the observed load time for the page

        # Parse the new page content
        article_html = driver.page_source
        article_soup = BeautifulSoup(article_html, 'html.parser')
        print(article_url)
        # Extract the desired div (adjust the class to the specific one you need)
        article_sizing_tables = article_soup.find_all('table')

        article_sizing_table = [x for x in article_sizing_tables if "Man" in str(x)]
        if len(article_sizing_table) != 1:
            continue
        article_sizing_table = article_sizing_table[0]
        article_sizing_rows = article_sizing_table.find_all('tr')
        article_sizing_values = [x.find_all('p')[1].text for x in article_sizing_rows]

        measurements = [int(x) for x in article_sizing_values if x.isnumeric()]

        if len(measurements) != 4:
            continue
        fit = True
        for i in range(4):
            if measurements[i] < ranges[i][0] or measurements[i] > ranges[i][1]:
                fit = False

        if fit:
            articles.append(article_url)

print()
print("These fit:")
for article in articles:
    print(article)

# Clean up: close the browser window
driver.quit()
