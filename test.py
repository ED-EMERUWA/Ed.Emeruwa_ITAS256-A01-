from bs4 import BeautifulSoup
import requests
import certifi

html_content = '''
<div class="hi">
    <div class="jobContainer sm:overflow-hidden">
        <a href="/jobs/police"></a>
        <a href="/jobs/pole"></a>
        <a href="/jobs/lice"></a>
    </div>
</div>
'''

URL = f"https://jobs.techtalent.ca/?k=information%20technology%E2%A6%81&%E2%A6%81l=British%20Columbia,%20Canada"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
headers = {'User-Agent':USER_AGENT}
page = requests.get(URL, headers=headers, verify=certifi.where())

jobs = []

soup = BeautifulSoup(page.content,"html.parser")


# Find the div with class 'jobContainer sm:overflow-hidden'
job_container = soup.find('div', class_='jobContainer sm:overflow-hidden')

# Extract the content inside the jobContainer
if job_container:
    links = job_container.find_all('a')  # Find all <a> tags inside it
    for link in links:
        print(link['href'])  # Print the href attribute of each <a> tag
else:
    print("No job container found.")
