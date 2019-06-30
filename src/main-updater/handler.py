#!/usr/bin/env python3
import os
import datetime
import time
import json

import boto3
from botocore.vendored import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template

days = 1
number_of_articles = 10
url = "https://hn.algolia.com/api/v1/search"
hacker_news_url = "https://news.ycombinator.com"
bucket = os.environ['S3_BUCKET']
styles = 'styles.css'


def get_articles(timestamp: str):
    r = requests.get("{url}?query=&hitsPerPage={number_of_articles}&tagFilters=%5B%22story%22%5D&numericFilters=%5B%22created_at_i%3E{seconds}%22%5D&queryType=prefixLast".format(url=url, seconds=timestamp, number_of_articles=number_of_articles))
    return r.text

def last_days_article():
    now = datetime.datetime.now()
    last_time = now - datetime.timedelta(days=days)
    seconds = (now-last_time).total_seconds()
    unix_date = time.time() - seconds
    articles = json.loads(get_articles(unix_date))
    return articles["hits"]

def parse_articles(articles):
    data = []
    for i in articles:
        comment = "{url}/item?id={id}".format(url=hacker_news_url, id=i["objectID"])
        data.append([i["url"],i["title"],comment])
    return data


def main():
    s3 = boto3.resource('s3')
    env = Environment(loader=FileSystemLoader('./templates'))
    articles = last_days_article()
    data = parse_articles(articles)
    template = env.get_template('index.html')
    content = template.render(data=data, timestamp=datetime.datetime.now().strftime("%m-%d-%Y %I:%M %p"), styles=styles)
    archive_content = template.render(data=data, timestamp=datetime.datetime.now().strftime("%m-%d-%Y %I:%M %p"), styles="../../{styles}".format(styles=styles))
    date = datetime.datetime.now().strftime("%m-%d-%Y")

    s3.Bucket(bucket).put_object(Key='index.html', Body=content, ContentType='text/html')
    s3.Bucket(bucket).put_object(Key="archives/{date}/index.html".format(date=date), Body=archive_content, ContentType='text/html')

if __name__ == "__main__":
    main()

def lambda_handler(event, context):
    main()