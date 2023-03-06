import io
import json
import re
import sys
import time
from urllib import parse

from bs4 import BeautifulSoup
import requests
from urllib3 import response


def news_crowl(value):
    result = []
    newslist = []
    data_news = {}
    dataJson = []
    url = "http://www.newsmp.com/news/articleList.html"
    if value is None:
        request = requests.post(url, data={'sc_area': 'A', 'view_type': 'sm'})
    else:
        decordeValue = parse.unquote(value)
        request = requests.post(url, data={'sc_word': decordeValue, 'sc_area': 'A', 'view_type': 'sm'})
    html = request.text
    soup = BeautifulSoup(html, 'html.parser')
    thnlist = soup.select(".list-block")
    for i in thnlist:
        title = re.sub('(<([^>]+)>)', '', str(i.select_one("strong").text)).replace("\n", "")
        summary = re.sub('(<([^>]+)>)', '', str(i.select_one(".line-height-3-2x").text)).replace("\n","").replace(" &amp;", "").replace("\t", "").replace("[의약뉴스]", "").replace("]", "").replace("[", "")
        date = re.sub('(<([^>]+)>)', '', str(i.select_one(".list-dated").text)).replace("\n","").replace("[","").replace("]", "")
        link = "http://www.newsmp.com/"
        link += re.sub('(<([^>]+)>)', '', str(i.select_one("a").get_attribute_list("href"))).replace("['","").replace("']", "")
        newslist.append([title, summary, link, date])
        data_news = {'title': title, 'summary': summary, 'link': link, 'date': date}
        dataJson.append(data_news)
    return dataJson