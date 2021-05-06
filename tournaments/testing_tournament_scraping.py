import requests
import re
import json
import random
from bs4 import BeautifulSoup
import sys
from tournament_scraping import process_tournament_from_url

tournament_url = 'https://fie.org/competitions/2020/771'
# print("Tournament URL for lookup: {}".format(tournament_url))
# pool_list = get_pool_list_from_url(tournament_url)
# print("Number of Pools in Tournament: {}".format(len(pool_list)))

# pool_id = random.randint(1,len(pool_list))

# fencer_list, pool_data = get_pool_data_from_dict(pool_list[pool_id-1])
# print("Results for Pool #{}".format(pool_id))
# print(pool_data)


print("Tournament URL for lookup: {}".format(tournament_url))
process_tournament_from_url(tournament_url)

