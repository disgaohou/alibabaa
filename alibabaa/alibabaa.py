#!/usr/bin/env python
# coding:utf-8

import re
import json
import urllib
import requests
from autouseragents.autouseragents import AutoUserAgents
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Alibabaa(object):

    def __init__(self, keywords=None, page=1):
        self.KEYWORDS = []
        if keywords:
            if isinstance(keywords, str):
                self.addKeyword(keywords, page)
            elif isinstance(keywords, list):
                self.addKeywords(keywords, page)
        self.PAGE = page
        self.URL = "https://s.1688.com/selloffer/rpc_async_render.jsonp?keywords={keyword}&button_click=top&n=y&uniqfield=pic_tag_id&templateConfigName=marketOfferresult&beginPage={page}&offset=9&pageSize=60&asyncCount=60&startIndex=0&async=true&enableAsync=true&rpcflag=new&_pageName_=market"
        self.MUA = AutoUserAgents()
        self.HEADERS = {
            "referer": "https://s.1688.com/",
            "user-agent": "",
            "x-requested-with": "XMLHttpRequest"
        }
        self.MODES = ["view", "save", "api"]
        self.RESULTS = {}
        self.DATAFILE = r"data.txt"

    def setPage(self, page):
        if page and isinstance(int, page) and page > 0:
            self.PAGE = page

    def addKeyword(self, keyword="", page=1):
        if keyword:
            if keyword not in self.KEYWORDS:
                self.KEYWORDS.append(keyword)
                return True
        else:
            raise KeyError("Keyword must be a string!")

    def addKeywords(self, keywords=[], page=1):
        if keywords:
            for keyword in keywords:
                self.addKeyword(keyword, page)
            return True
        else:
            raise KeyError("Keywords must be a non-empty list of strings!")

    def extract(self, item):
        data = {}
        mainBlock = item.find("div", class_="imgofferresult-mainBlock")
        if mainBlock:
            second = mainBlock.find(
                "div", class_=re.compile(r".*sm-offer-price.*"))
            if second:
                tag = second.find("span", class_=re.compile(r".*sm-offer-priceNum.*"))
                if tag:
                    priceStr = tag.getText().strip()
                    priceList = re.findall(r"\d*\.\d*", priceStr)
                    price = float(priceList[0])
                    data["price"] = price if r"万" not in priceStr else price * 10000
                else:
                    data["price"] = -1

            third = mainBlock.find("div", class_=re.compile(r".*sm-offer-title.*"))
            if third:
                tag = third.find("a", attrs={"offer-stat": "title"})
                data["item"] = "" if not tag else tag["title"].strip().encode("utf8")

            fourth = mainBlock.find(
                "div", class_=re.compile(r".*sm-offer-company.*"))
            if fourth:
                tag = fourth.find("a", attrs={"offer-stat": "com"})
                data["company"] = "unknown" if not tag else tag.getText(
                ).strip().encode("utf8")

            fifth = mainBlock.find("div", class_=re.compile(r".*sm-offer-sub.*"))
            if fifth:
                tag = fifth.find("div", class_=re.compile(r".*location.*"))
                data["location"] = "unknown" if not tag else tag.getText(
                ).strip().encode("utf8")
            return data
        return None

    def alimama(self, mode="view"):
        assert mode in self.MODES
        for keyword in self.KEYWORDS:
            self.RESULTS[self.KEYWORDS.index(keyword)] = []
            key = urllib.quote(keyword.decode("utf-8").encode("gbk"))
            for i in range(self.PAGE):
                pdata = []
                url = self.URL.format(keyword=key, page=i + 1)
                self.HEADERS["user-agent"] = self.MUA.random_agent().values()[0]
                response = requests.get(url, headers=self.HEADERS)
                print response.url
                html = response.content.decode("gbk")
                m = re.search(r"\<li.*\>", html).group(0)
                m = re.sub(r"\\n", "", m)
                m = re.sub(r"\\r", "", m)
                m = re.sub(r"\\", "", m)
                p = re.sub(r"\<!--.*?--\>", "", m)
                soup = BeautifulSoup(p, "lxml")
                items = soup.findAll("li", class_="sm-offer-item sw-dpl-offer-item ")
                for item in items:
                    data = self.extract(item)
                    if data:
                        pdata.append(data)
                if pdata:
                    self.RESULTS[self.KEYWORDS.index(keyword)] = pdata
                if mode == "view":
                    for data in pdata:
                        for k, v in data.items():
                            print k, v
        if mode == "save":
            with open(self.DATAFILE, "w") as f:
                try:
                    f.write(json.dumps(self.RESULTS))
                    return True
                except Exception as e:
                    raise RuntimeError("Unable to save scraped data to file {}".format(self.DATAFILE))
        if mode == "api":
            return self.RESULTS


if __name__ == '__main__':
    Alibabaa("自行车", page=2).alimama(mode="view")
