import json
import numpy as np
import matplotlib.pyplot as plt

import requests

url = 'https://stats.nba.com/stats/playbyplayv2/?gameId=0021600732&startPeriod=0&endPeriod=14'


request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'stats.nba.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

r = requests.get(url, headers=request_headers)
y = r.json()
x = y['resultSets'][0]['rowSet']

scores = []



for row in y['resultSets'][0]['rowSet']:
    scores.append(row[y['resultSets'][0]['headers'].index('SCOREMARGIN')])


print(scores)

newscores = []

for score in scores:
    if score != None:
        newscores.append(score)

print(newscores)



cleanleads = []

for lead in newscores:
    lead = int(lead)
    cleanleads.append(lead)

print(cleanleads)

plt.plot(cleanleads)
plt.show()
