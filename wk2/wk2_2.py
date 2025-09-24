from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver= webdriver.Chrome()
driver.get("https://quotes.toscrape.com")
time.sleep(3)

answer= []
author_links=set()
state=0
while len(author_links)!=20:
    quotes = driver.find_elements(By.CLASS_NAME,"quote")       
    for author in quotes:
        if len(author_links)>=20:break
        links = author.find_element(By.TAG_NAME, "a").get_attribute("href")
        author_links.add(links) 
    if len(author_links)>=20:break
    try:
        driver.get("https://quotes.toscrape.com")
        state +=1
        print(state)
        for _ in range(state):
            next_button = driver.find_element(By.CLASS_NAME, "next").find_element(By.TAG_NAME, "a")
            next_button.click()
            time.sleep(2)
    except Exception as e:
        print("No more pages to scrape error:",e)
        break
    if len(author_links)>=20:break
    print(len(author_links))
    
 
for link in author_links:
    driver.get(link)
    time.sleep(2)

    try:
        name= driver.find_element(By.CLASS_NAME,"author-title").text
        nationality= driver.find_element(By.CLASS_NAME,"author-born-location").text
        description=driver.find_element(By.CLASS_NAME,"author-description").text
        dob=driver.find_element(By.CLASS_NAME,"author-born-date").text
        answer.append({
        "Name":name,
        "Nationality":nationality,
            "Description":description,
        "Date Of Birth":dob,
    })
    except Exception as e:
        print("something went wrong heres the error: ",e)
        break

        

driver.quit()

print(len(answer))
