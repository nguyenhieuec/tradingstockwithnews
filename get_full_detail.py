
import pandas as pd
import numpy as np

#internet package

import urllib3
from bs4 import BeautifulSoup  
http = urllib3.PoolManager()

#functional package
import logging
import requests
from newspaper import Article
from newspaper import fulltext
from tqdm import tqdm
from tqdm import tnrange, tqdm_notebook

logging.basicConfig(filename="crawlfulltext.log",level=logging.ERROR)

news_url = pd.read_csv("news_url.csv", usecols = range(1,5))


def get_details_from_url(df_to_get):
    data_dicts = []
    for newsdate, url in tqdm(zip(df_to_get['newsdate'].values, df_to_get['url'].values)):
        row_dict = {}
        try:
            article = Article(url, language='vi')
            article.download()
            article.parse()
            article.nlp()
            row_dict['newsdate'] = newsdate
            row_dict['fulltext'] = article.text
            row_dict['summnary'] = article.summary
            row_dict['keyword'] = article.keywords
            data_dicts.append(row_dict)
        except Exception:
#             logging.error()
            continue
    return data_dicts


# from multiprocessing.dummy import Pool as ThreadPool 
# pool = ThreadPool(32)
# results = pool.map(get_details_from_url(news_url))
# pool.close() 
# pool.join()

newfull = pd.DataFrame(get_details_from_url(news_url))
newfull.to_csv('newfull.csv')
