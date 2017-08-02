#!/usr/bin/env python

import requests

from elasticsearch import Elasticsearch
from pprint import PrettyPrinter
from configparser import ConfigParser
from os.path import splitext
from datetime import datetime

printer = PrettyPrinter(indent=2)

ACCEPTABLE_FILE_TYPES = ('.java', '.py', '.rb', '.js', '.go')

def main():
    config = ConfigParser()
    config.read('default.conf')
    
    gh_client_id = config['DEFAULT']['client_id']
    gh_client_secret = config['DEFAULT']['client_secret']
    
    headers = {
                'User-Agent': 'ElasticsearchETLDemo/1.0',
                'Accept': 'application/vnd.github.v3+json'
            }

    oauth_string = 'client_id=' + gh_client_id + '&client_secret=' + gh_client_secret
    
    result = requests.get('https://api.github.com/users/TheBeege/repos?' + oauth_string, headers=headers).json()
    #printer.pprint(result)
    
    repos_to_consume = [repo['name'] for repo in result ]
    #print('repos_to_consume:')
    #printer.pprint(repos_to_consume)
    
    es = Elasticsearch()
    
    for repo in repos_to_consume:
        current_contents_path = 'https://api.github.com/repos/TheBeege/' + repo + '/contents/?'
        
        result = requests.get(current_contents_path + oauth_string).json()
        #printer.pprint(result.json())
        while len(result) > 0:
            item = result.pop()
            print('item name:', item['name'])
            create_document_from_item(es, repo, item)
            if item['type'] == 'dir':
                url = item['_links']['self'] + '&' + oauth_string
                #print('url:', url)
                dir_contents = requests.get(url).json()
                #printer.pprint(dir_contents)
                result.extend(dir_contents)
            

def create_document_from_item(es, repo, item):
    file_name, file_extension = splitext(item['name'])
    if item['type'] == 'file' and file_extension in ACCEPTABLE_FILE_TYPES:
        document = {
                    'name': item['name'],
                    'url': item['download_url'],
                    'user': 'TheBeege',
                    'size': item['size'],
                    'file_extension': file_extension,
                    'repo': repo,
                    'contents': requests.get(item['download_url']).text,
                    'timestamp': datetime.now()
                }
        es.index(index='github', doc_type='source_file', id=item['_links']['self'], body=document)


if __name__ == '__main__':
    main()

