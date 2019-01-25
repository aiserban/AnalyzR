from bs4 import BeautifulSoup
import requests
import re

root_url = 'https://old.reddit.com/r/Romania/new/'

soup = BeautifulSoup(requests.get(root_url, headers={'User-Agent': 'TestCrawler by NoSkillz05'}).text, 'html.parser')
thread_regex = re.compile('https:\/\/old.reddit.com\/r\/Romania\/comments\/')
load_more_regex = re.compile('^https:\/\/old.reddit.com\/r\/Romania\/new\/\?count=.*after')

links = [] # storing all links here
last_link = None
last_id = None
load_more_link = None


while len(links) < 100:
    anchors = soup.find_all('a')
    for anchor in anchors:
        href = anchor.get('href')
        if href is not None and href not in links and thread_regex.search(href):
            links.append(href)
        elif href is not None and load_more_regex.search(href):
            load_more_link = href

    soup = BeautifulSoup(requests.get(load_more_link, headers={'User-Agent': 'TestCrawler by NoSkillz05'}).text, 'html.parser')

print(links)
