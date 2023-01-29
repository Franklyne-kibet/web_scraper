from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd


job_name = "Data Analyst"
country_name = "United States"

job_url = " "
for item in job_name.split(" "):
    if item != job_name.split(" ")[-1]:
        job_url = job_url + item + "%20"
    else: 
        job_url = job_url + item

country_url = " "
for item in country_name.split(" "):
    if item != country_name.split(" ")[-1]:
        country_url = country_url + item + "%20"
    else:
        country_url = country_url + item

url = f"https://www.linkedin.com/jobs/search?keywords={job_url}&location={country_url}&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"


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

#Detecting how many jobs are available
jobs_num = driver.find_element(By.CSS_SELECTOR, "h1>span").get_attribute("innerText")
if len(jobs_num.split(',')) > 1:
    jobs_num = int(jobs_num.split(',')[0])*1000
else:
    jobs_num = int(jobs_num)

jobs_num = int(jobs_num)

#while loop to browse all jobs
i = 2
while i <= int(jobs_num/2) + 1:
    #we keep scrolling down to the end of the view
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    i += 1
    print("Current at: ", i, "percentage at:", ((i+1)/(int(jobs_num/2)+1))*100, "%", end="\r")
    try:
        #We try to click on the load more results buttons in case it is already 
        infinite_scroller_button = driver.find_element(By.XPATH, ".//button[@aria-label='Load more results']")
        infinite_scroller_button.click()
        time.sleep(0.1)
    except:
        #If there is no button, there will be an error, so we keep scrolling down.
        time.sleep(0.1)
        pass

#get a list containing all jobs that we have found
job_lists  = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")
jobs = job_lists.find_elements(By.TAG_NAME, "li") #returns a list

#We declare void list to keep track of all obtaind data.
job_title_list = []
company_name_list = []
location_list = []
salary_list = []
date_list = []
job_link_list = []

# We loop through every job and obtain the info
for job in jobs:
    #job_title
    job_title = job.find_element(By.CSS_SELECTOR, "h3").get_attribute("innerText")
    job_title_list.append(job_title)

    #company_name
    company_name = job.find_element(By.CSS_SELECTOR, "h4").get_attribute("innerText")
    company_name_list.append(company_name)

    #location
    location = job.find_element(By.CSS_SELECTOR, "div>span").get_attribute("innerText")
    location_list.append(location)

    #compensation
    salary = job.find_element(By.CSS_SELECTOR, "div>div>span").get_attribute("innerText")
    salary_list.append(salary)

    #date
    date = job.find_element(By.CSS_SELECTOR, "div>div>time").get_attribute("innerText")
    date_list.append(date)

    #job_link
    job_link = job.find_element(By.CSS_SELECTOR,"a").get_attribute("href")
    job_link_list.append(job_link)


job_data = pd.DataFrame({
    'Date': date,
    'Company': company_name,
    'Title': job_title,
    'Location': location,
    'Salary': salary
})

print(job_title_list)
print(salary_list)
print(company_name_list)
print(date_list)
print(location_list)