
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

logging.basicConfig(filename="crawlvn30.log",level=logging.ERROR)

news_url = pd.read_csv("news_url.csv", usecols = range(1,5))

news_url_mini = news_url[news_url['ticker'].isin(['CII','CTD','CTG','DHG','DPM','EIB','FPT','GAS','GMD','HDB','HPG','MBB','MSN','MWG','NVL','PNJ','REE','ROS','SAB','SBT','SSI','STB','TCB','VCB','VHM','VJC','VIC','VPB','VRE','VNM'])]

# print(news_url_mini)
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
            row_dict['summary'] = article.summary
            row_dict['keywords'] = article.keywords
            data_dicts.append(row_dict)
        except Exception as e:
#             logging.error()
            continue
#         print(data_dicts)
    return data_dicts

#from multiprocessing.dummy import Pool as ThreadPool 
#pool = ThreadPool(32)
#results = pool.map(get_details_from_url(news_url_mini))
#pool.close() 
#pool.join()

newsvn30 = pd.DataFrame(get_details_from_url(news_url_mini))
newsvn30.to_csv('newsvn30.csv')