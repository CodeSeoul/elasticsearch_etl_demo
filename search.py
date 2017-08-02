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

#results = es.search(index='github', body={
#    'query': {
#        'bool': {
#            'must': [
#                { 'match': { 'contents': 'armor' } }
#            ],
#            'filter': {
#                'match': { 'file_extension': '.java' }
#            }
#        }
#    },
#    '_source': ['contents'],
#    'sort': { '_score': 'desc' },
#    'size': 2
#})

##########################
#######  COUNT FILES BY TYPE #######
##########################

#results = es.search(index='github', body={
#    'size': 0,
#    'aggs': {
#        'group_by_type': {
#            'terms': {
#                'field': 'file_extension.keyword'
#            },
#        }
#    }
#})

##########################
#######  AVG SIZE BY TYPE #######
##########################

results = es.search(index='github', body={
    'size': 0,
    'aggs': {
        'group_by_type': {
            'terms': {
                'field': 'file_extension.keyword'
            },
            'aggs': {
                'average_size': {
                    'avg': {
                        'field': 'size'
                    }
                }
            }
        }
    }
})



if len(results['hits']['hits']) > 0:
    for result in results['hits']['hits']:
        printer.pprint(result) 

if 'aggregations' in results:
    printer.pprint(results['aggregations'])


