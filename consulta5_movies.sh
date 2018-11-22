#!/bin/bash
# -*- ENCODING: UTF-8 -*-
curl -XGET 'localhost:9200/moviesf/_search?pretty' -H 'Content-Type: application/json' -d'
{
  "size":0,
  "aggs": {
     "group_by_production_countries": { 
          "terms":{
              "field": "production_countries.keyword"}}
          }
}
'
