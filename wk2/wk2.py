# Import required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()
driver.get("https://books.toscrape.com")
time.sleep(3)  # Wait for page to load

# Initialize list to store scraped book data
data = []

# Loop through first 4 pages
for i in range(4):
    # ---------------------------
    # Step 1: Extract all book detail page links on the current page
    # ---------------------------
    books = driver.find_elements(By.CLASS_NAME, "product_pod")
    book_links = []
    
    for book in books:
        # Find link to each book's detail page
        link = book.find_element(By.CLASS_NAME, "image_container").find_element(By.TAG_NAME, "a").get_attribute("href")
        book_links.append(link)

    # ---------------------------
    # Step 2: Visit each book page and scrape details
    # ---------------------------
    for link in book_links:
        driver.get(link)
        time.sleep(2)  # Allow page to load

        try:
            # Extract book details
            book_name = driver.find_element(By.CLASS_NAME, "product_main").find_element(By.TAG_NAME, "h1").text
            price = driver.find_element(By.CLASS_NAME, "price_color").text
            stock_status = driver.find_element(By.CLASS_NAME, "instock.availability").text.strip()
            rating = driver.find_element(By.CLASS_NAME, "star-rating").get_attribute("class").split()[-1]
            description = driver.find_element(By.CLASS_NAME, "product_page").find_element(By.TAG_NAME, "p").text
            product_info = driver.find_element(By.CLASS_NAME, "table").text
            category = driver.find_element(By.CSS_SELECTOR, ".breadcrumb li:nth-child(3)").text

            # Append book details to data list
            data.append({
                "Book Name": book_name,
                "Price": price,
                "Stock Status": stock_status,
                "Rating": rating,
                "Description": description,
                "Product Information": product_info,
                "Category": category,
            })

        except Exception as e:
            print("Error scraping page details:", e)

    # ---------------------------
    # Step 3: Go to the next page
    # ---------------------------
    try:
        driver.get("https://books.toscrape.com")  # Return to homepage
        for _ in range(_ + 1):  # Click "next" the correct number of times
            next_button = driver.find_element(By.CLASS_NAME, "next").find_element(By.TAG_NAME, "a")
            next_button.click()
            time.sleep(2)
    except:
        print("No more pages to scrape")
        break

# Close the WebDriver
driver.quit()

# ---------------------------
# Step 4: Print scraped data
# ---------------------------
for book in data:
    print(book)
