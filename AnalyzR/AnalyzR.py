import requests, re, os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from unidecode import unidecode

subreddit = 'Romania'
output_dir = os.getcwd()
output_filename = 'RomaniaWordCloud'


titles = []
done = False
start_date = datetime(2021, 1, 1)
end_date = datetime(2022, 1, 1)
days_to_increment = 5
after_date = start_date
before_date = start_date + timedelta(days_to_increment)


while not done:
    after = after_date.strftime('%Y-%m-%d')
    before = before_date.strftime('%Y-%m-%d')
    url = 'https://api.pushshift.io/reddit/submission/search?sort=desc&limit=10000&subreddit=' + subreddit + '&after=' + after + '&before=' + before
    response = requests.get(url).json();
    for item in response['data']:
        title = unidecode(item['title'])
        if title not in titles:
            titles.append(title)
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


words = ''

for title in titles:
    words_in_title = title.split()
    substring = ' '.join(map(str, words_in_title))
    substring = re.sub(r'[^\w\s\-]', '', substring)
    words += substring + ' '

# conjunctii, anomalii etc
exclusions = [
    'fost',
    'cine',
    'au',
    'ca',
    'că',
    'căci',
    'când',
    'cât',
    'cum',
    'dacă',
    'dar',
    'darămite',
    'de',
    'decât',
    'deci',
    'deoarece',
    'deși',
    'fără',
    'fie',
    'fiindcă',
    'iar',
    'isi',
    'încât',
    'însă',
    'întrucât',
    'necum',
    'nici',
    'numai',
    'or',
    'ori',
    'până',
    'uri',
    'F',
    'lui',
    'precum',
    'sau',
    'să',
    'și',
    'totuși',
    'unde',
    'pe',
    'la',
    'spre',
    'cu',
    'de',
    'fără',
    'sub',
    'în',
    'prin',
    'pentru',
    'către',
    'contra',
    'lângă',
    'ce',
    'si',
    'sa',
    'ma',
    'fi',
    'in',
    'din',
    'care',
    'se',
    'de',
    'va',
    'fi',
    'ati',
    'imi',
    'asa',
    'mi',
    'un',
    'nu',
    'da',
    'mai',
    'ati',
    'ce',
    'cat',
    'o',
    'e',
    'la',
    'ne',
    'pe',
    'au',
    'mi',
    'al',
    'cel',
    'vs',
    'își',
    'pt',
    'new',
    'home',
    'ati',
    'asa',
    'ai',
    'te',
    'le',
    'o',
    'mi',
    'ul',
    'n',
    'm',
    'l',
    'il',
    'ii'
]

word_list = words.split(' ')
curated_words = ''
for word in word_list:
    if word.lower() not in exclusions:
        curated_words += ' ' + word

print('Plotting...')

word_cloud = WordCloud(width=2048, height=1024).generate(curated_words)
plt.figure(figsize=(20,10))
plt.imshow(word_cloud, interpolation="bilinear")
plt.axis("off")
plt.savefig(output_dir + '/' + output_filename + '.png', dpi=200)
print('Done!')
