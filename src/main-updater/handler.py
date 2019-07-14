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

http_protocal = "http://"
hacker_news_api = "https://hn.algolia.com/api/v1/search"
hacker_news_url = "https://news.ycombinator.com"

smmry_api = "https://api.smmry.com"
smmry_length = 5
smmry_secret_name = "smmry_api_key"
smmry_secret_region = "us-west-2"

bucket = os.environ['S3_BUCKET']
styles = 'styles.css'

timestamp = datetime.datetime.now().strftime("%m-%d-%Y %I:%M %p")
now = datetime.datetime.now()
date = now.strftime("%m-%d-%Y")
yesterday = (now - datetime.timedelta(days=1)).strftime("%m-%d-%Y")


def get_articles(timestamp: str):
    r = requests.get("{url}?query=&hitsPerPage={number_of_articles}&tagFilters=%5B%22story%22%5D&numericFilters=%5B%22created_at_i%3E{seconds}%22%5D&queryType=prefixLast".format(url=hacker_news_api, seconds=timestamp, number_of_articles=number_of_articles))
    return r.text

def last_days_article():
    last_time = now - datetime.timedelta(days=days)
    seconds = (now-last_time).total_seconds()
    unix_date = time.time() - seconds
    articles = json.loads(get_articles(unix_date))
    return articles["hits"]

def summarize_article(article, smmry_api_key):
    params = {"SM_API_KEY" : smmry_api_key, "SM_LENGTH" : smmry_length, "SM_URL" : article["url"]}
    try:
        r = requests.get("{url}".format(url=smmry_api),params=params)
        data = json.loads(r.text)
        if 'sm_api_content' in data:
            return ""
        else:
            print(data['sm_api_content'])
            return data['sm_api_content']
    except:
        return ""

def get_smmry_api_key():
    client = boto3.client('secretsmanager')
    secret_value = json.loads(client.get_secret_value(SecretId=smmry_secret_name)['SecretString'])
    return secret_value['smmry_key']

def prepare_articles(articles):
    smmry_api_key = get_smmry_api_key()
    data = []
    for i in articles:
        comment = "{url}/item?id={id}".format(url=hacker_news_url, id=i["objectID"])
        summary = summarize_article(i, smmry_api_key)
        data.append([i["url"], i["title"], comment, summary])
    return data

def main():
    s3 = boto3.resource('s3')
    env = Environment(loader=FileSystemLoader('./templates'))
    articles = last_days_article()
    data = prepare_articles(articles)
    previous_url = "{protocal}{bucket}/archives/{yesterday}".format(protocal=http_protocal, bucket=bucket, yesterday=yesterday)

    template = env.get_template('index.html')
    content = template.render(data=data, previous=previous_url, timestamp=timestamp, styles=styles)
    archive_content = template.render(data=data, previous=previous_url, timestamp=timestamp, styles="../../{styles}".format(styles=styles))

    s3.Bucket(bucket).put_object(Key='index.html', Body=content, ContentType='text/html')
    s3.Bucket(bucket).put_object(Key="archives/{date}/index.html".format(date=date), Body=archive_content, ContentType='text/html')

if __name__ == "__main__":
    main()

def lambda_handler(event, context):
    main()