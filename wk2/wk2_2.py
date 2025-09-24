# Import required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# ---------------------------
# Step 1: Set up WebDriver
# ---------------------------
driver = webdriver.Chrome()
driver.get("https://quotes.toscrape.com")
time.sleep(3)  # Wait for page to load

# ---------------------------
# Step 2: Initialize data structures
# ---------------------------
answer = []             # List to store author details
author_links = set()    # Use a set to avoid duplicate author links
state = 0               # Counter for page navigation

# ---------------------------
# Step 3: Collect author links (until we have 20 unique authors)
# ---------------------------
while len(author_links) != 20:
    quotes = driver.find_elements(By.CLASS_NAME, "quote")  # Get all quotes on the page
    
    for author in quotes:
        if len(author_links) >= 20:
            break
        links = author.find_element(By.TAG_NAME, "a").get_attribute("href")  # Extract author link
        author_links.add(links)
    
    if len(author_links) >= 20:
        break
    
    # Navigate to the next page(s)
    try:
        driver.get("https://quotes.toscrape.com")  # Return to homepage to click correct "next" page
        state += 1
        print("Navigating pages, state:", state)
        
        for _ in range(state):
            next_button = driver.find_element(By.CLASS_NAME, "next").find_element(By.TAG_NAME, "a")
            next_button.click()
            time.sleep(2)
    
    except Exception as e:
        print("No more pages to scrape, error:", e)
        break
    
    print("Number of unique authors collected so far:", len(author_links))

# ---------------------------
# Step 4: Visit each author page and scrape details
# ---------------------------
for link in author_links:
    driver.get(link)
    time.sleep(2)
    
    try:
        name = driver.find_element(By.CLASS_NAME, "author-title").text
        nationality = driver.find_element(By.CLASS_NAME, "author-born-location").text
        description = driver.find_element(By.CLASS_NAME, "author-description").text
        dob = driver.find_element(By.CLASS_NAME, "author-born-date").text
        
        answer.append({
            "Name": name,
            "Nationality": nationality,
            "Description": description,
            "Date Of Birth": dob,
        })
    
    except Exception as e:
        print("Something went wrong, error:", e)
        break

# ---------------------------
# Step 5: Close WebDriver
# ---------------------------
driver.quit()

# ---------------------------
# Step 6: Output result
# ---------------------------
print("Total authors scraped:", len(answer))
