import requests

class hn_client(object):
    def __init__(self):
        self.url = "http://hn.algolia.com/api/v1/"

    def items(self, post_id):
        request = requests.get('{url}/items/{post_id}'.format(url=self.url,post_id=post_id))
        if request.status_code == requests.codes.ok:
            return request.json()
    
    def users(self, username):
        request = requests.get('{url}/users/{username}'.format(url=self.url,username=username))
        if request.status_code == requests.codes.ok:
            return request.json()

    def search(self, query, tags, page):
        params = {}
        if query:
            params['query'] = query
        if tags:
            params['tags'] = tags
        if page:
            params['page'] = page
        request = requests.get('{url}/search'.format(url=self.url), params=params)
        if request.status_code == requests.codes.ok:
            return request.json()

    def search_by_date(self, query, start_date, end_date, tags, page):
        params = {}
        if query:
            params['query'] = query
        if tags:
            params['tags'] = tags
        if page:
            params['page'] = page
        if numericfilters:
            
        request = requests.get('{url}/search'.format(url=self.url), params=params)
        if request.status_code == requests.codes.ok:
            return request.json()

