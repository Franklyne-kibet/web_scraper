from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd


country_name = "United States"

url = "https://www.linkedin.com/jobs/search?keywords=&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"

#creating a webdriver instance 
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("detach", True)


service = Service('chromedriver')
service.start()
driver = webdriver.Chrome(options=options, service=service)
driver.get(url)
print(driver.title)

#Auto scroller
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

#Going through the job-search results
titles = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")
print(titles.text)

#Auto-scroller button the results
auto_scroller_button = driver.find_element(By.CLASS_NAME, "infinite-scroller__show-more-button infinite-scroller__show-more-button--visible")



