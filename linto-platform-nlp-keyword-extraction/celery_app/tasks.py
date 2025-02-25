import json
import re
from typing import Union, Dict, Any
from collections import Counter, OrderedDict
from keyword_extraction.frekeybert import get_frekeybert_keywords

from keyword_extraction.utils import get_keybert_keywords, get_word_frequencies, get_textrank_topwords, get_topicrank_topwords

from celery_app.celeryapp import celery

@celery.task(name="keyword_extraction_task", bind=True) # Task name definition
def keyword_extraction_task(self, documents: list, method: str, config: dict): # Task parameters
    """keyword_extraction_task"""
    self.update_state(state="STARTED")
    # print("Using " + method + "to extract keywords from " + str(documents))
    # print("With config " + str(config))

    methods_map = {"frequencies": get_word_frequencies,
                  "textrank": get_textrank_topwords,
                  "topicrank": get_topicrank_topwords,
                  "keybert": get_keybert_keywords,
                  "frekeybert": get_frekeybert_keywords}

    # print("Using " + method + "to extract keywords from " + str(documents))

    result = []
    if method in methods_map:
        try:
            extract_keywords = methods_map[method.lower()]
            for doc in documents:
                result.append(extract_keywords(doc, config)) 
        except Exception as e:
            raise Exception("Can't extract keywords at keyword_extraction_task: " + str(e) + "; config: " + str(config) + "; doc: " + str(documents))
    else:
        result = ["Method " + method + " can't be found"]

    result = [OrderedDict(sorted(r.items(), key=lambda x: -x[1])) for r in result]
    return result