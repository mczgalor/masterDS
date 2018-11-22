#!/bin/bash
# -*- ENCODING: UTF-8 -*-
curl -XGET 'localhost:9200/moviesf/_search?pretty' -H 'Content-Type: application/json' -d'
{
  "_source": ["title","original_language","popularity"],
  "query": { "match_all": {} },
  "size": 100
}
'
