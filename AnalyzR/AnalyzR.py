from bs4 import BeautifulSoup
import requests
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

root_url = 'https://old.reddit.com/r/Romania/new/'

soup = BeautifulSoup(requests.get(root_url, headers={'User-Agent': 'TestCrawler by NoSkillz05'}).text, 'html.parser')

titles = [] # storing all links here
words = ''

while len(titles) < 10000:
    threads = soup.find_all('a', {'class': 'title'})
    for thread in threads:
        title = thread.text
        if title is not None and title not in titles:
            titles.append(title)

    load_more_link = soup.select_one('.next-button a').get('href')

    soup = BeautifulSoup(requests.get(load_more_link, headers={'User-Agent': 'TestCrawler by NoSkillz05'}).text, 'html.parser')


for title in titles:
    words += ' ' + title

print('Plotting...')

word_cloud = WordCloud(width=2048, height=1024).generate(''.join(words))
plt.figure(figsize=(20,10))
plt.imshow(word_cloud, interpolation="bilinear")
plt.axis("off")
plt.savefig('C:\\Users\\Andrei\\Desktop\\RomaniaWordCloud.png', dpi=200)