from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

driver = webdriver.Chrome(ChromeDriverManager().install())
# Enter the url of Problem set(i.e list of few 500-600 problems in one page)
driver.get("https://www.codechef.com/tags/problems/dynamic-programming")
time.sleep(5)
html = driver.page_source

# creating Soup for html page of Problems List
soup = BeautifulSoup(html, 'html.parser')

# Selecting div of Link and Title
problemTitleDiv = soup.findAll('div', {"class": "problem-tagbox-headtext"})

# Arrays for storing titles and links
dpProblemTitles = []
dpProblemLinks = []

# Fetching url & titles
for ques in problemTitleDiv[::2]:
    # url
    dpProblemLinks.append("https://www.codechef.com" + ques.find('a')['href'])
    # title
    dpProblemTitles.append(ques.find('a').text)

# Saving them into file
with open('problem_titles.txt', 'w+') as f:
    f.write('\n'.join(dpProblemTitles))

with open('problem_links.txt', 'w+') as f:
    f.write('\n'.join(dpProblemLinks))

# -- The urls taken from above will be opened and problem statement will be scraped

# Making Directory for Problems
mypath = 'C:\\Users\\himan\\PycharmProjects\\webscraperProject-Codechef\\Problems'
if not os.path.isdir(mypath):
    os.makedirs(mypath)

# Problem Content Scraping
i = 1
for link in dpProblemLinks:
    # Opening Problem Link
    driver.get(link)
    time.sleep(6)
    # Creating soup for Problems Page
    html2 = driver.page_source
    soup2 = BeautifulSoup(html2, 'html.parser')

    description = []
    # All Problems are inside a div named problem-statement, so I traversed in its children and saved all its text
    # content ignoring lower portion of cc problems
    psdiv = soup2.find('div', {'class': 'problem-statement'})
    #  If Page does not exist(VIMP - Some pages of cc were broken. This is to prevent crashing the programme)
    if not psdiv:
        description.append("Error Loading Problem")
    else:
        j = 0
        for x in psdiv.children:
            if x.name == 'aside':
                break
            if j == 0 and x.name == 'h3':
                j = j
            else:
                # Strip is used to ignore all inside tags but not their texts
                text = x.text.strip()
                description.append(text)
            j = j+1
    print(description)
    # Saving Problem into files at the Problem Directory
    # Encoding set to UTF8
    with open(os.path.join(mypath, 'problem' + str(i) + '.txt'), 'w+', encoding='utf-8') as f:
        f.write('\n'.join(description))
    i = i + 1
