"""



THis os a file that extracts meta information on a job websitevv  







"""
import certifi
import requests
from bs4 import BeautifulSoup
import json

URLS = [f"https://www.itjobs.ca/en/search-jobs/?location=British+Columbia&location-id=BC&location-type=2&search=1&sort_order=1&page={i}" for i in range(1,3)]

for URL in URLS:
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"

    headers = {'User-Agent':USER_AGENT}

    page = requests.get(URL, headers=headers, verify=certifi.where())
    jobs = []
    soup = BeautifulSoup(page.content,"html.parser")
    all_job_container = soup.find("div", "result-ctn")
    all_jobs = all_job_container.find_all("div","offer-details")
    for job in all_jobs:
        job_title = all_jobs.find("a", class_="offer-name")
        job_description = all_jobs.find("p", class_="offer-description")
        job_company = all_job_container.find("div", "company-details")
        job_location =job_company.find("a", class_ = "location") 
        jobs.append({"position": job_title, "company":job_company, "location": job_location, "description":job_description })
    # Make the bjson of all te jobs 
    joblist = json.dumps(jobs, indent=4)
    # a try and except for writing json to a file
    try:
        with open("joblist", "w") as file:
            json.dump(jobs, file, indent=4)  # Save dict as JSON file
    except Exception as e:
        print(f"An error occurred: {e}")

        
print(all_jobs)