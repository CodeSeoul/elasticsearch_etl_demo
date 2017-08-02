#!/usr/bin/env python

from elasticsearch import Elasticsearch
from pprint import PrettyPrinter

printer = PrettyPrinter()
es = Elasticsearch()

##########################
#######  FIND ALL ########
##########################
#results = es.search(index='github', body={
#    'query': {
#        'match_all': {}
#    }
#})
#
#for result in results['hits']['hits']:
#    printer.pprint(result) 

##########################
#######  FIND PYTHON #######
##########################

#results = es.search(index='github', body={
#    'query': {
#        'match': {
#            'file_extension': '.py'
#        }
#    },
#    'size': 3
#})

##########################
#######  FIND JAVA ARMOR #######
##########################

results = es.search(index='github', body={
    'query': {
        'bool': {
            'must': [
                { 'match': { 'contents': 'armor' } }
            ],
            'filter': {
                'match': { 'file_extension': '.java' }
            }
        }
    },
    '_source': ['contents'],
    'sort': { '_score': 'desc' },
    'size': 2
})


for result in results['hits']['hits']:
    printer.pprint(result) 


