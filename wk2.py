from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Initialize the WebDriver
opera="/Applications/Opera GX.app/Contents/MacOS/Opera"
chromedriver_path = "/usr/local/bin/chromedriver"
options = Options()
options.binary_location = opera
service = Service(chromedriver_path)


driver = webdriver.Chrome(service=service, options=options)
driver.get("https://books.toscrape.com")
time.sleep(3)

# Initialize a list to store scraped data
data = []

# Loop through 5 pages
for page in range(5):
    # Find all books on the current page
    books = driver.find_elements(By.CLASS_NAME, "product_pod")
    
    # Loop through each book and scrape details
    for book in books:
        # Click on the book to go to the product page
        link = book.find_element(By.TAG_NAME, "a")
        link.click()
        time.sleep(2)  # Wait for the product page to load

        # Scrape details
        try:
            book_name = driver.find_element(By.CSS_SELECTOR, ".product_main h1").text
            price = driver.find_element(By.CLASS_NAME, "price_color").text
            stock_status = driver.find_element(By.CLASS_NAME, "instock.availability").text.strip()
            rating = driver.find_element(By.CLASS_NAME, "star-rating").get_attribute("class").split()[-1]
            description = driver.find_element(By.ID, "product_description").find_element(By.XPATH, "following-sibling::p").text
            category = driver.find_element(By.CSS_SELECTOR, ".breadcrumb li:nth-child(3)").text
            product_info = driver.find_element(By.CLASS_NAME, "table.table-striped").text
        except Exception as e:
            print(f"Error scraping book details: {e}")
            driver.back()
            continue

        # Append the scraped data to the list
        data.append({
            "Book Name": book_name,
            "Price": price,
            "Stock Status": stock_status,
            "Rating": rating,
            "Description": description,
            "Category": category,
            "Product Info": product_info
        })

        # Go back to the catalog page
        driver.back()
        time.sleep(2)

    # Navigate to the next page
    try:
        next_button = driver.find_element(By.CLASS_NAME, "next")
        next_button.click()
        time.sleep(2)  # Wait for the next page to load
    except:
        print("No more pages to scrape.")
        break

# Quit the driver
driver.quit()

# Print the scraped data
for book in data:
    print(book)