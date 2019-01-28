from bs4 import BeautifulSoup
import requests
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta


#root_url = 'https://old.reddit.com/r/Romania/new/'

#soup = BeautifulSoup(requests.get(root_url, headers={'User-Agent': 'TestCrawler by NoSkillz05'}).text, 'html.parser')

#titles = [] # storing all links here
#words = ''

#while len(titles) < 10000:
#    threads = soup.find_all('a', {'class': 'title'})
#    for thread in threads:
#        title = thread.text
#        if title is not None and title not in titles:
#            titles.append(title)

#    load_more_link = soup.select_one('.next-button a').get('href')

#    soup = BeautifulSoup(requests.get(load_more_link, headers={'User-Agent': 'TestCrawler by NoSkillz05'}).text, 'html.parser')


#for title in titles:
#    words += ' ' + title
titles = []
subreddit = 'Romania'
done = False
start_date = datetime(2018, 1, 1)
end_date = datetime(2018, 1, 5)
days_to_increment = 5
after_date = start_date
before_date = start_date + timedelta(days_to_increment)


while not done:
    after = after_date.strftime('%Y-%m-%d')
    before = before_date.strftime('%Y-%m-%d')
    url = 'https://api.pushshift.io/reddit/submission/search?sort=desc&limit=10000&subreddit=' + subreddit + '&after=' + after + '&before=' + before
    response = requests.get(url).json();
    for item in response['data']:
        title = item['title']
        if title not in titles:
            titles.append(item['title'])
    print('Got titles between ' + after + ' and ' + before + '. Reached ' + str(len(titles)) + ' titles')
    if before_date >= end_date:
        done = True
    else:
        after_date += timedelta(days_to_increment)
        if before_date + timedelta(days_to_increment) >= end_date:
            before_date = end_date
        else:
            before_date += timedelta(days_to_increment)


print('Got a total of ' + str(len(titles)) + ' titles')

save_path = 'C:\\Users\\Andrei\\Desktop\\titles.txt'
saved_titles = open(save_path, 'x', encoding='utf-8')
saved_titles.writelines(titles)







#print('Plotting...')

#word_cloud = WordCloud(width=2048, height=1024).generate(''.join(words))
#plt.figure(figsize=(20,10))
#plt.imshow(word_cloud, interpolation="bilinear")
#plt.axis("off")
#plt.savefig('C:\\Users\\Andrei\\Desktop\\RomaniaWordCloud.png', dpi=200)