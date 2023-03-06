import io
import json
import re
import sys

import requests
from bs4 import BeautifulSoup

def newsRank_crowl():
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
    url = "http://www.newsmp.com/news/articleList.html?sc_section_code=S1N2&view_type=sm"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        newslist = []
        data_news = {}
        thnlist = soup.select('#skin-1 > .item')
        count = 0
        # list2 = thnlist.find_all(".item")
        for i in thnlist:
            count += 1
            rank = count
            title = re.sub('(<([^>]+)>)', '', str(i.select_one("a > .auto-titles"))).replace("\n", "")
            newslist.append([rank, title])
            data_news[str(rank)] = {'title': title}
        json_val = json.dumps(data_news)
        return json_val
