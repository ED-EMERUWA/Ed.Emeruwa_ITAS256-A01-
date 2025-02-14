import certifi
import requests
from bs4 import BeautifulSoup
import json

URL = f"https://jobs.techtalent.ca/?k=information%20technology%E2%A6%81&%E2%A6%81l=British%20Columbia,%20Canada"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
headers = {'User-Agent':USER_AGENT}
page = requests.get(URL, headers=headers, verify=certifi.where())


def get_description(link, tag, class_):
    detail_page = requests.get(link, headers=headers, verify=certifi.where())
    broth = BeautifulSoup(detail_page.content,"html.parser")
    page_description = broth.find(tag, class_ = class_).get_text()
    return page_description

def refine_description(api_key, rough_desription)    :
    prompt = f'this is a job description, shorten it to less than 20 words: {rough_desription}'

    # Make the API call
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=60
    )

    # Print the response
    print(response.choices[0].text.strip())

def refine_description(api_key, rough_description):
    prompt = f'This is a job description, shorten it to less than 20 words: {rough_description}'

    # Make the API call
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=60
    )

    # Print the response



jobs = []

soup = BeautifulSoup(page.content,"html.parser")
all_job_container = soup.find("div", class_="jobContainer sm:overflow-hidden")
print(all_job_container)
all_jobs = all_job_container.find_all("a", class_ = "job-post-summary w-full no-underline block text-grey-darkest mb-2 mb-3 border bg-white rounded-lg")



for job in all_jobs:
    job_title = job.find("div", class_ ="job-post-summary__header flex items-center").text.strip()
    job_company = job.find("span", class_ = "flex items-center mir-2 no-underline w-full mb-2 md:w-auto md:mb-0").text.strip()
    job_logo = job.find("svg", class_ = "mir-1 flex-no-shrink")
    job_location = job.find("span", class_ = "flex flex-shrink items-center").text.strip()
    # job_link = all_jobs.find([href])

    jobs.append({"position": job_title, "company":job_company, "location": job_location})
print(jobs)
    