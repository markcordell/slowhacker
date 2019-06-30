#!/usr/bin/env python3
import os
import datetime
import time
import json

import boto3
from botocore.vendored import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template

days = 1
url = "https://hn.algolia.com/api/v1/search"
hacker_news_url = "https://news.ycombinator.com"
bucket = os.environ['S3_BUCKET']


def get_articles(timestamp: str):
    r = requests.get("{url}?query=&hitsPerPage=10&minWordSizefor1Typo=4&minWordSizefor2Typos=8&advancedSyntax=true&ignorePlurals=false&tagFilters=%5B%22story%22%5D&numericFilters=%5B%22created_at_i%3E{seconds}%22%5D&page=0&queryType=prefixLast&typoTolerance=true&restrictSearchableAttributes=%5B%5D".format(url=url, seconds=timestamp))
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
    env = Environment(loader=FileSystemLoader('./templates'))
    last = last_day()
    data = []
    for i in last:
        comment = "{url}/item?id={id}".format(url=hacker_news_url, id=i["objectID"])
        data.append([i["url"],i["title"],comment])
    template = env.get_template('s3-index.html')
    body = template.render(data=data, timestamp=datetime.datetime.now().strftime("%m-%d-%Y %I:%M %p"))
    body

    s3.Bucket(bucket).put_object(Key='index.html', Body=body, ContentType='text/html')

if __name__ == "__main__":
    main()

def lambda_handler(event, context):
    main()