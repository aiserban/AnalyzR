from bs4 import BeautifulSoup
import requests
import re

root_url = 'https://old.reddit.com/r/Romania/new/'

soup = BeautifulSoup(requests.get(root_url, headers={'User-Agent': 'TestCrawler by NoSkillz05'}).text, 'html.parser')

titles = [] # storing all links here


while len(titles) < 100:
    threads = soup.find_all('a', {'class': 'title'})
    for thread in threads:
        title = thread.text
        if title is not None and title not in titles:
            titles.append(title)

    load_more_link = soup.select_one('.next-button a').get('href')

    soup = BeautifulSoup(requests.get(load_more_link, headers={'User-Agent': 'TestCrawler by NoSkillz05'}).text, 'html.parser')

print(titles)
