"""
Author: Ed Emeruwa
Course: ITAS 256
Description:
This script scrapes job postings from the Tech Talent website, refines job descriptions using OpenAI's GPT model, 
and stores job details in a JSON file.

"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import openai
from openai import OpenAI
from dotenv import load_dotenv
import json
import os

# Load environment variables from the .env file
load_dotenv()

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Initialize the browser
browser = webdriver.Firefox()

# URL of the job site
URL = "https://jobs.techtalent.ca/?k=information%20technology%E2%A6%81&%E2%A6%81l=British%20Columbia,%20Canada"
BASE_URL = "https://jobs.techtalent.ca"


def refine_description(link):
    """Refines and summarizes the job description. I know i shouldnt be creating a new browser instance but it helps with minimizing cloudflare verification"""
    try:
        new_browser = webdriver.Firefox()
        new_browser.get(link)
        new_browser.implicitly_wait(5)  # Increased wait time for better reliability
        
        # Get all paragraph elements
        description_list = new_browser.find_elements(By.TAG_NAME, "p")
        rough_description = ""

        # Combine all paragraphs with proper spacing
        for paragraph in description_list:
            text = paragraph.text.strip()
            if text:  # Only add non-empty paragraphs
                rough_description += text + " "
        
        if not rough_description:
            return "Description not available"
        
        if "Verifying you are human" in rough_description:
            return "No description retrieved. Scraping blocked by Cloudflare"
        
        prompt = f'Summarize this job description in about 20 words, focusing on key responsibilities and requirements: {rough_description}'
        
        # API call to OpenAI models for job description refinement
        try:
            response = client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": prompt,
                }],
                model="gpt-3.5-turbo",  
                max_tokens=50  
            )
            return response.choices[0].message.content
            
        except Exception as api_error:
            print(f"OpenAI API error: {api_error}")
            return "Error processing description"

    except Exception as e:
        print(f"Error in refine_description: {e}")
        return "Error retrieving description"
        
    finally:
        new_browser.quit()


def fetch_existing_jobs():
    """Fetches existing jobs from the JSON file."""
    try:
        with open("joblist.json", "r") as file:
            return json.load(file)  # Load the existing jobs
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # If file doesn't exist or is empty, initialize an empty list


def save_jobs_to_file(jobs):
    """Saves the job data to a JSON file."""
    try:
        with open("joblist.json", "w") as file:
            json.dump(jobs, file, indent=4)
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")


def scrape_jobs():
    """Scrapes jobs from the site and returns the jobn ."""
    jobs = fetch_existing_jobs()
    browser.get(URL)

    job_containers = browser.find_elements(By.CLASS_NAME, "jobContainer")

    for job_container in job_containers:
        all_jobs = job_container.find_elements(By.CLASS_NAME, "job-post-summary")
        print(f"Loading...")
        # Directly assigning in the dictionary
        for job in all_jobs:
            job_data = {
                "Position": job.find_element(By.CLASS_NAME, "job-post-summary__title").text.strip() or "Job title not provided",
                "Company": job.find_element(By.CSS_SELECTOR, "span.flex.items-center").text.strip() or "Company name not available",
                "Location": job.find_element(By.CLASS_NAME, "flex.flex-shrink.items-center").text.strip() or "Location details missing",
                "Description": refine_description(job.get_attribute("href"))
            }
            jobs.append(job_data)

    return jobs


if __name__ == "__main__":
    try:
        jobs = scrape_jobs()
        print(jobs)
        save_jobs_to_file(jobs)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        browser.quit()
