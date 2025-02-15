from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up Firefox WebDriver
browser = webdriver.Firefox()

# Open the job website
browser.get("https://jobs.techtalent.ca/?k=information%20technology%E2%A6%81&%E2%A6%81l=British%20Columbia,%20Canada")

jobs = []  # List to store job data

try:
    # Find all job containers
    job_containers = browser.find_elements(By.CLASS_NAME, "jobContainer")

    for job_container in job_containers:
        # Find all job posts inside this container
        all_jobs = job_container.find_elements(By.CLASS_NAME, "job-post-summary")

        for job in all_jobs:
            job_title = job.find_element(By.CLASS_NAME, "job-post-summary__title").text.strip()
            job_title = job_title if job_title else "Job title not provided"


            job_company = job.find_element(By.CSS_SELECTOR, "span.flex.items-center").text.strip()
            job_company = job_company if job_company else "Company name not available"

            job_location = job.find_element(By.CLASS_NAME, "flex.flex-shrink.items-center").text.strip()
            job_location = job_location if job_location else "Location details missing"

            print(f"Job Title: {job_title}")
            print(f"Company: {job_company}")
            print(f"Location: {job_location}")
            


            # Print job title
            print(job_title)

except Exception as e:
    print("Error:", e)

finally:
    # Close the browser
    browser.quit()
