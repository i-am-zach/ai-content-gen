import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
from pathlib import Path
import logging
import datetime as dt

logging.basicConfig(level=logging.WARNING)

def scrape_india_today(driver, url):
    # Initialize the browser
    driver.get(url)
    
    # Wait for the 'description' div to be present
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'description'))
    WebDriverWait(driver, 10).until(element_present)

    # Wait an additional 10 seconds for the rest of the page to load
    time.sleep(2)

    # Double click on the title of the page
    # The title is the first h1 in the document
    title = driver.find_element(By.TAG_NAME, 'h1')
    driver.execute_script("arguments[0].scrollIntoView();", title)
    title.click()
    title.click()

    time.sleep(1)

    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1)

    # Find the first p in the document and scroll to it
    first_p = driver.find_element(By.TAG_NAME, 'p')
    driver.execute_script("arguments[0].scrollIntoView();", first_p)

    time.sleep(1)

    # Check if a button or div with text "Read full story" exists, and click it
    buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'Read Full Story')]")
    if buttons:
        # Scroll to the button
        driver.execute_script("arguments[0].scrollIntoView();", buttons[0])
        time.sleep(1)
        try:
            buttons[0].click()
        except:
            logging.warning('Could not click "Read Full Story" button')

    # Get all p elements inside of the div with class 'description'
    description_div = driver.find_element(By.CLASS_NAME, 'description')
    WebDriverWait(driver, 10).until(lambda x: len(description_div.find_elements(By.TAG_NAME, 'p')) > 2)
    paragraphs = description_div.find_elements(By.TAG_NAME, 'p')
    
    # Extract and return the text of each paragraph
    return [para.text for para in paragraphs]

def scrape_toi(driver, url):
    driver.get(url)

    time.sleep(2)
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    time.sleep(1)
    # Scroll to the first h1 in the document
    title = driver.find_element(By.TAG_NAME, 'h1')
    driver.execute_script("arguments[0].scrollIntoView();", title)

    time.sleep(2)

    # Find the div with data-articlebody="1"
    article_body = driver.find_element(By.XPATH, '//div[@data-articlebody="1"]')
    # If it doesn't exist, throw an error
    if not article_body:
        raise Exception('Could not find article body')
    
    # For each div inside of article body, get all the text content
    divs = article_body.find_elements(By.TAG_NAME, 'div')
    return [div.text for div in divs]


def scrape_ndtv(driver, url):
    driver.get(url)

    time.sleep(2)

    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1)

    # Scroll to the first h1 in the document
    title = driver.find_element(By.TAG_NAME, 'h1')
    driver.execute_script("arguments[0].scrollIntoView();", title)

    time.sleep(2)

    # Find the div with id="ins_storybody"
    article_body = driver.find_element(By.ID, 'ins_storybody')
    # Get all the p in the children of article_body
    paragraphs = article_body.find_elements(By.TAG_NAME, 'p')

    return [para.text for para in paragraphs]

def scrape_the_hindu(driver, url):
    driver.get(url)

    time.sleep(2)

    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1)

    # Scroll to the first h1 in the document
    title = driver.find_element(By.TAG_NAME, 'h1')
    driver.execute_script("arguments[0].scrollIntoView();", title)

    time.sleep(2)

    # Find the div with itemprop="articleBody"
    article_body = driver.find_element(By.XPATH, '//div[@itemprop="articleBody"]')
    # Get all the p in the children of article_body
    paragraphs = article_body.find_elements(By.TAG_NAME, 'p')

    return [para.text for para in paragraphs]

def main():
    driver = webdriver.Safari()
    title = sys.argv[1]
    url = sys.argv[2]
    provider = sys.argv[3]

    output_dir = Path('./out') / 'articles' / dt.date.today().strftime("%Y-%m-%d") / provider

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if provider == 'india_today':
        article_content = scrape_india_today(driver, url)
        with open(output_dir / f"{title}.txt", 'w') as f:
            f.write('\n'.join(article_content))
    elif provider == "timesofindia":
        # article_content = get_times_of_india_article_content(driver, url)
        # with open(output_dir / f"{title}.txt", 'w') as f:
        #     f.write('\n'.join(article_content))
        logging.warning("Times of India not implemented")
    elif provider == "ndtv":
        article_content = scrape_ndtv(driver, url)
        with open(output_dir / f"{title}.txt", 'w') as f:
            f.write('\n'.join(article_content))
    elif provider == "thehindu":
        article_content = scrape_the_hindu(driver, url)
        with open(output_dir / f"{title}.txt", 'w') as f:
            f.write('\n'.join(article_content))


if __name__ == "__main__":
    main()


