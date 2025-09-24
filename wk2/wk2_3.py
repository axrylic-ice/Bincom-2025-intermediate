# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# ---------------------------
# Step 1: Set up the WebDriver
# ---------------------------
driver = webdriver.Chrome()

# ---------------------------
# Step 2: Go to a random Wikipedia page
# ---------------------------
driver.get("https://en.wikipedia.org/wiki/Special:Random")
time.sleep(3)  # Wait for page to load

# ---------------------------
# Step 3: Extract the page title
# ---------------------------
title = driver.find_element(By.ID, "firstHeading").text

# ---------------------------
# Step 4: Extract the first paragraphs
# ---------------------------
try:
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "div.mw-parser-output > p")
except:
    paragraphs = ["No paragraph found."]  # Ensure it's a list for iteration

# ---------------------------
# Step 5: Extract categories
# ---------------------------
try:
    categories = driver.find_elements(By.CSS_SELECTOR, "#mw-normal-catlinks ul li a")
    category_list = [cat.text for cat in categories]
except:
    category_list = []

# ---------------------------
# Step 6: Print results
# ---------------------------
print("Title:", title)
print("\nParagraphs:")
for paragraph in paragraphs[:3]:  # Print first 3 paragraphs
    print(paragraph.text)

print("\nCategories:", category_list)

# ---------------------------
# Step 7: Close the WebDriver
# -------------
