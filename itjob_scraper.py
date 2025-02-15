"""
Author: Ed Emeruwa
Course: ITAS 256
Description:
This script extracts job information from the IT Jobs website in British Columbia.
It scrapes job titles, descriptions, company names, and locations from multiple pages,
and appends the data to an existing JSON file.

"""

import certifi
import requests
from bs4 import BeautifulSoup
import json

# Base URL for scraping job listings from multiple pages
URLS = [f"https://www.itjobs.ca/en/search-jobs/?location=British+Columbia&location-id=BC&location-type=2&search=1&sort_order=1&page={i}" for i in range(1, 4)]

# List to store extracted job data
jobs = []

def fetch_job_data(URL):
    """
    Fetch job data from a specific URL, extracting job details such as title, company, location, and description and returns a list of dictionaries containing job details.
    """
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    headers = {'User-Agent': USER_AGENT}
    page = requests.get(URL, headers=headers, verify=certifi.where())
    
    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")
    
    # Find all job containers on the page
    all_job_container = soup.find("div", class_="result-ctn")
    all_jobs = all_job_container.find_all("div", class_="details-wrapper")
    
    # Extract job details from each job container
    job_list = []
    for job in all_jobs:
        job_title = job.find("a", class_="offer-name").text.strip()
        job_description = job.find("p", class_="offer-description").text.strip()
        job_company = job.find("a", class_="company").text.strip()
        job_location = job.find("a", class_="location").text.strip()
        
        # Append the extracted job data to the list
        job_list.append({
            "Position": job_title,
            "Company": job_company,
            "Location": job_location,
            "Description": job_description
        })
    
    return job_list

def load_existing_jobs():
    """Load existing jobs from the JSON file."""
    try:
        with open("joblist.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty list if the file does not exist

def append_jobs_to_file(jobs):
    """Append new jobs to the existing JSON file."""
    existing_jobs = load_existing_jobs()

    # Only append jobs that are not already in the existing job list
    for job in jobs:
        if job not in existing_jobs:
            existing_jobs.append(job)

    try:
        with open("joblist.json", "w") as file:
            json.dump(existing_jobs, file, indent=4)  # Save the updated job list to file
            print("Added jobs succesfully")
    except Exception as e:
        print(f"An error occurred while saving to the file: {e}")

def main():

    for URL in URLS:
        new_jobs = fetch_job_data(URL)
        append_jobs_to_file(new_jobs)

if __name__ == "__main__":
    main()
