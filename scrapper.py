import os
import time
import requests
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the URL and local path
base_url = https://www.gov.uk/government/collections/country-policy-and-information-notes
local_path = "C:\\Users\\ksmuv\\Downloads\\Docs_loadder"  # Replace with your actual local path

# Create the local directory if it doesn't exist
if not os.path.exists(local_path):
    os.makedirs(local_path)

# Set up Selenium WebDriver
chromedriver_path = "C:\\Users\\ksmuv\\Downloads\\Docs_loadder\\chromedriver.exe"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Function to download a file
def download_file(url, local_filename):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        logging.info(f"Downloaded {local_filename}")
    except Exception as e:
        logging.error(f"Failed to download {url}: {e}")

# Function to find and download all PDF links on the current page
def find_pdfs_on_page():
    document_links = driver.find_elements(By.XPATH, "//a[contains(@class, 'gem-c-attachment__link') and contains(@href, '.pdf')]")
    for link in document_links:
        href = link.get_attribute('href')
        if href:
            file_name = os.path.join(local_path, href.split('/')[-1])
            logging.info(f"Downloading {href} to {file_name}")
            download_file(href, file_name)

# Function to navigate through country sublinks and find PDFs
def navigate_and_download_pdfs(url):
    logging.info(f"Accessing country URL: {url}")
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    # Download PDFs on the current page
    find_pdfs_on_page()

# Start the process by visiting the base URL
logging.info(f"Accessing base URL: {base_url}")
driver.get(base_url)
time.sleep(5)  # Wait for the page to load

# Load alphabet links into a list
alphabet_links = driver.find_elements(By.XPATH, "//a[contains(@class, 'gem-c-contents-list__link')]")
alphabet_fragments = [link.get_attribute('href') for link in alphabet_links]

logging.info("Alphabet links found:")
for alphabet_fragment in alphabet_fragments:
    logging.info(f"Alphabet fragment: {alphabet_fragment}")

# Iterate over each alphabet link
for alphabet_fragment in alphabet_fragments:
    if alphabet_fragment.startswith('#'):
        alphabet_url = base_url + alphabet_fragment  # Correctly form the URL
    else:
        alphabet_url = alphabet_fragment
    logging.info(f"Clicking on alphabet link: {alphabet_url}")
    driver.get(alphabet_url)
    time.sleep(5)  # Wait for the page to load

    # Find all country sublinks on the alphabetical page
    country_sublinks = driver.find_elements(By.XPATH, "//a[contains(@data-track-category, 'navDocumentCollectionLinkClicked') and contains(@href, '/government/publications/')]")
    if country_sublinks:
        logging.info(f"Found {len(country_sublinks)} country sublinks.")
    else:
        logging.info("No country sublinks found.")

    country_urls = [link.get_attribute('href') for link in country_sublinks]

    # Log each country sublink found
    for country_url in country_urls:
        if country_url.startswith(https://):
            full_country_url = country_url
        else:
            full_country_url = https://www.gov.uk + country_url
        logging.info(f"Country sublink URL: {full_country_url}")

        # Navigate to the country sublink
        navigate_and_download_pdfs(full_country_url)

# Close the browser
driver.quit()

logging.info("Download completed.")
