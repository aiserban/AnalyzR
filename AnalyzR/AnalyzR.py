import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime, timedelta



titles = []
subreddit = 'Romania'
done = False
start_date = datetime(2020, 1, 1)
end_date = datetime(2021, 1, 1)
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

save_path = '/Users/andrei/Source/AnalyzR/AnalyzR/postTitles2020.txt'
saved_titles = open(save_path, 'x', encoding='utf-8')
saved_titles.write('\n'.join(titles))



words = ''
for title in titles:
    words += ' ' + title


#exclusions = ['de','cu','din','un','mai','de','pe','despre','la','unde',
              #'ar','se','va','mai','cele','ca','sa','către','am','fi',
              #'li','in','se','îl','îţi','dă','cea','si','a','în','al','ne',
              #'te','și','să','ar','le','tot','ţi']
#for word in exclusions:
#    words = words.replace(' ' + word + ' ','')

print('Plotting...')

word_cloud = WordCloud(width=2048, height=1024).generate(''.join(words))
plt.figure(figsize=(20,10))
plt.imshow(word_cloud, interpolation="bilinear")
plt.axis("off")
plt.savefig('/Users/andrei/Source/AnalyzR/AnalyzR/RomaniaWordCloud2020.png', dpi=200)