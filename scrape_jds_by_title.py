"""
Scrape Indeed.com for job descriptions matching the top female
and male jobs extracted with get_job_titles.py.

e.g. https://www.indeed.com/jobs?q=%22computer+programmer%22&l=
(Where %22 is a double quotation mark - must use to get exact matches)
"""
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import random


def clean_html(html_str):
    """Clean text of html elements"""
    clean_html = re.sub(r"<.*>", " ", str(html_str))
    clean_html = clean_html.replace('\n', '')
    clean_html = clean_html.replace('\t', '')
    return clean_html

def get_links(titles, gender):
    """Retrieve the links to the top search results for a job title"""
    links = []
    secs_range = range(10, 20, 2)
    for title in titles:
        print(title)
        title = title.replace(' ', '+').replace('"', '')
        url = 'https://www.indeed.com/jobs?q=%22{}%22&l='.format(title)
        html_doc = requests.get(url)
        soup = BeautifulSoup(html_doc.content, 'html.parser')
        cnt = 0
        for link in soup.find_all('a'):
            href = link.get('href')
            if href != None and 'js=3' in href:
                link = 'https://www.indeed.com' + href
                links.append((gender, title, link))
                cnt+=1
        print('Number of links = ', cnt)
        # Pause for a few seconds (random lengths of time)
        time.sleep(random.choice(secs_range))
    return links

def get_jds(links):
    """Get the job description text"""
    fptr = open('data/job_data.tsv', 'w')
    secs_range = range(10, 20, 2)
    for gender, title, link in links:
        print(link)
        html_doc = requests.get(link)
        soup = BeautifulSoup(html_doc.content, 'html.parser')
        jd_html = soup.find(id="jobDescriptionText")
        jd = clean_html(jd_html)
        if jd == None or len(jd) == 0:
            print('No JD!')
        if len(jd) > 0:
            line = fptr.write('{}\t{}\t{}\t{}\n'.format(title, gender, link, jd))
        # Pause for a few seconds (random lengths of time)
        time.sleep(random.choice(secs_range))
    fptr.close()
    
if __name__ == '__main__':
    female_titles = pd.read_csv('data/female_occupations_top.csv')['Occupation']
    male_titles = pd.read_csv('data/male_occupations_top.csv')['Occupation']

    links_a = get_links(female_titles, 'Female')
    time.sleep(10)
    links_b = get_links(male_titles, 'Male')

    links_a.extend(links_b)
    job_descriptions = get_jds(links_a)