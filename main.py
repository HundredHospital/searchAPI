# uvicorn main:app --reload --host=0.0.0.0 --port=5055

import json
from typing import Optional, List, Union
from fastapi import FastAPI, Header
import requests
from bs4 import BeautifulSoup
import re
import sys
import io

from starlette.middleware.cors import CORSMiddleware

from crowl_json.newsRank_crowl import newsRank_crowl
from crowl_json.news_crowl import news_crowl

app = FastAPI()

origins = ["*"]

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/search")
async def say_hello(name: Union[str] = Header(default=None), company: Union[str] = Header(default=None), use: Union[str] = Header(default=None)):

    if name is not None:
        name = '='+name
    if company is not None:
        company = '='+company
    if use is not None:
        use = '='+use

    result = []
    url = f"http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList?" \
          f"serviceKey=hLIMsRTbYc8aY8HV9IIyK79wlrdv9gW1AIol1wtLBjlIcBXmKwcAkLhOIFi8QoDSVg%2B9wvXzdH3gZY91%2FnSUjQ%3D%3D&type=json&itemName{name}&entpName{company}&efcyQesitm{use}"
    res = requests.get(url)
    data = json.loads(res.text)
    for i in data['body']['items']:
        data_appro = {}
        data_appro["name"] = i['itemName']
        data_appro["company"] = i['entpName']
        data_appro["use"] = re.sub('(<([^>]+)>)', '', i['efcyQesitm']).replace("\n", "")
        data_appro["amount"] = re.sub('(<([^>]+)>)', '', i['useMethodQesitm']).replace("\n", "")
        data_appro["danger"] = re.sub('(<([^>]+)>)', '', str(i['atpnQesitm'])).replace("\n", "")
        data_appro["keep"] = re.sub('(<([^>]+)>)', '', str(i['depositMethodQesitm'])).replace("\n", "")
        if i['itemImage'] is None:
            data_appro["img"] = "이미지 없음"
        else:
            data_appro["img"] = i['itemImage']
        result.append(data_appro)


    return result

@app.get("/news")
async def news(value: Union[str] = Header(default=None)):
    return news_crowl(value)

@app.get("/newsRank")
async def newsRank():
    result = []
    res = json.loads(newsRank_crowl())
    result.append(res)
    return result