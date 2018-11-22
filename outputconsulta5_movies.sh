{
  "took" : 429,
  "timed_out" : false,
  "_shards" : {
    "total" : 5,
    "successful" : 5,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : 45554,
    "max_score" : 0.0,
    "hits" : [ ]
  },
  "aggregations" : {
    "group_by_production_countries" : {
      "doc_count_error_upper_bound" : 165,
      "sum_other_doc_count" : 11922,
      "buckets" : [
        {
          "key" : "[{'iso_3166_1': 'US', 'name': 'United States of America'}]",
          "doc_count" : 17834
        },
        {
          "key" : "[]",
          "doc_count" : 6261
        },
        {
          "key" : "[{'iso_3166_1': 'GB', 'name': 'United Kingdom'}]",
          "doc_count" : 2235
        },
        {
          "key" : "[{'iso_3166_1': 'FR', 'name': 'France'}]",
          "doc_count" : 1648
        },
        {
          "key" : "[{'iso_3166_1': 'JP', 'name': 'Japan'}]",
          "doc_count" : 1354
        },
        {
          "key" : "[{'iso_3166_1': 'IT', 'name': 'Italy'}]",
          "doc_count" : 1029
        },
        {
          "key" : "[{'iso_3166_1': 'CA', 'name': 'Canada'}]",
          "doc_count" : 838
        },
        {
          "key" : "[{'iso_3166_1': 'DE', 'name': 'Germany'}]",
          "doc_count" : 746
        },
        {
          "key" : "[{'iso_3166_1': 'RU', 'name': 'Russia'}]",
          "doc_count" : 735
        },
        {
          "key" : "[{'iso_3166_1': 'IN', 'name': 'India'}]",
          "doc_count" : 734
        }
      ]
    }
  }
}
