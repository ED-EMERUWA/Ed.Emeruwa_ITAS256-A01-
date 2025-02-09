import certifi
import requests
from bs4 import BeautifulSoup
import json

URL = f"https://jobs.techtalent.ca/?k=information%20technology%E2%A6%81&%E2%A6%81l=British%20Columbia,%20Canada"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
headers = {'User-Agent':USER_AGENT}
page = requests.get(URL, headers=headers, verify=certifi.where())

jobs = []

soup = BeautifulSoup(page.content,"html.parser")
all_job_container = soup.find  ("div", class_ ="jobContainer sm:overflow-hidden")
all_jobs = all_job_container.find_all("a", clas_ = "job-post-summary w-full no-underline block text-grey-darkest mb-2 mb-3 border bg-white rounded-lg")


for job in all_jobs:
    job_title = job.find("div", class_ ="job-post-summary__header flex items-center").text.strip()