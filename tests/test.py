from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd


url = "https://www.techwithtim.net/"

#creating a webdriver instance 
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
service = Service('chromedriver')
service.start()
driver = webdriver.Chrome(options=options, service=service)

driver.get(url)
print(driver.title)

#search thorough the website
search = driver.find_element(By.NAME , "s")
search.send_keys("test")
search.send_keys(Keys.RETURN)

try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "main"))
    )

    articles = main.find_elements(By.TAG_NAME, "article")
    for article in articles:
        header = article.find_elements(By.CLASS_NAME,"entry-summary")
        print(article.text)

except:
    driver.quit()
