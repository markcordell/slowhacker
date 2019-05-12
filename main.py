#!/usr/bin/env python3
import datetime
import requests
import time
import json

import boto3
from flask import Flask
from flask import render_template
from jinja2 import Template

days = 1
app = Flask(__name__)


def process_articles():
    return True


def get_articles(timestamp: str):
    r = requests.get("http://hn.algolia.com/api/v1/search?query=&hitsPerPage=10&minWordSizefor1Typo=4&minWordSizefor2Typos=8&advancedSyntax=true&ignorePlurals=false&tagFilters=%5B%22story%22%5D&numericFilters=%5B%22created_at_i%3E{seconds}%22%5D&page=0&queryType=prefixLast&typoTolerance=true&restrictSearchableAttributes=%5B%5D".format(seconds=timestamp))
    return r.text

def last_day():
    now = datetime.datetime.now()
    last_time = now - datetime.timedelta(days=days)

    seconds = (now-last_time).total_seconds()
    unix_date = time.time() - seconds
    articles = json.loads(get_articles(unix_date))
    return articles["hits"]

def main():
    s3 = boto3.resource('s3')
    template = get_last_day()

    s3.Bucket('slowhacker-site').put_object(key='index.html', Body=template)



    
    print(last_day())


@app.route("/v1/last-day")
def get_last_day():
    last = last_day()
    data = []
    for i in last:
        data.append([i["url"],i["title"]])
    print(data)
    return render_template('index.html',data=data)


if __name__ == "__main__":
    main()