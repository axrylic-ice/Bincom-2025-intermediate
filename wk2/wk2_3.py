from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up the driver
driver = webdriver.Chrome()

# Go to Wikipedia Random page
driver.get("https://en.wikipedia.org/wiki/Special:Random")
time.sleep(3)

# Get page title
title = driver.find_element(By.ID, "firstHeading").text

# Get first paragraph from the content area
try:
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "div.mw-parser-output > p")
except:
    paragraphs = "No paragraph found."

# Get categories (usually at the bottom of the page)
try:
    categories = driver.find_elements(By.CSS_SELECTOR, "#mw-normal-catlinks ul li a")
    category_list = [cat.text for cat in categories]
except:
    category_list = []

# Print results
print("Title:", title)
print("Paragraphs")
for paragraph in paragraphs[:3]:
    print(paragraph.text)
print("\nCategories:", category_list)

driver.quit()
