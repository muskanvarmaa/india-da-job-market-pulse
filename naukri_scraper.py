from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time

def init_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.naukri.com/")
    return driver

def build_url(keyword, page_num):
    base = keyword.replace(" ", "-")
    if page_num == 1:
        return f"https://www.naukri.com/{base}-jobs?k={keyword.replace(' ', '+')}&experience=0"
    else:
        return f"https://www.naukri.com/{base}-jobs-{page_num}?k={keyword.replace(' ', '+')}&experience=0"

def scrape_page(driver, url):
    jobs = []
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_cards = soup.find_all("div", class_="srp-jobtuple-wrapper")
    print(f"Found {len(job_cards)} jobs on this page")

    for card in job_cards:
        try:
            title = card.find("a", class_="title").text.strip()
            company = card.find("a", class_="comp-name").text.strip()
            experience = card.find("span", class_="expwdth").text.strip()

            salary_tag = card.find("div", class_="sal-wrap")
            salary = salary_tag.find("span").text.strip() if salary_tag else "Not mentioned"

            location = card.find("span", class_="locWdth").text.strip()

            skill_tags = card.find_all("li", class_="tag-li")
            skills = ", ".join([s.text.strip() for s in skill_tags])

            posted = card.find("span", class_="job-post-day").text.strip()

            jobs.append({
                "title": title,
                "company": company,
                "experience": experience,
                "salary": salary,
                "location": location,
                "skills": skills,
                "posted": posted
            })
        except Exception as e:
            pass

    return jobs

def scrape_all_pages(keyword="data analyst", num_pages=10):
    driver = init_driver()
    all_jobs = []

    for page in range(1, num_pages + 1):
        url = build_url(keyword, page)
        jobs = scrape_page(driver, url)
        all_jobs.extend(jobs)
        print(f"Page {page} done — {len(all_jobs)} total jobs so far")
        time.sleep(2)

    driver.quit()
    return all_jobs

def save_to_csv(jobs):
    df = pd.DataFrame(jobs)
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    filename = f"data/raw/jobs_{date_str}.csv" 
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} jobs to {filename}")

if __name__ == "__main__":
    jobs = scrape_all_pages(num_pages=60)
    print(f"\nTotal jobs scraped: {len(jobs)}")
    save_to_csv(jobs)