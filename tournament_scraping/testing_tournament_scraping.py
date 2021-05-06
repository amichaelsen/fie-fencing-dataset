import requests
import re
import json
import random
from bs4 import BeautifulSoup
from tournament_scraping import get_pool_list_from_url
from pool_scraping.pool_scraping import get_pool_data_from_dict

tournament_url = 'https://fie.org/competitions/2020/771'
print("Tournament URL for lookup: {}".format(tournament_url))
pool_list = get_pool_list_from_url(tournament_url)
print("Number of Pools in Tournament: {}".format(len(pool_list)))

pool_id = random.randint(1,len(pool_list))

fencer_list, pool_data = get_pool_data_from_dict(pool_list[pool_id-1])
print("Results for Pool #{}".format(pool_id))
print(pool_data)