import numpy as np
import requests
import re
import json
from bs4 import BeautifulSoup
from pools.pool_data import PoolData
from pools.pool_scraping import get_pool_data_from_dict

# --------------------------------------------------------------------------------
#                         Test PoolData class
# --------------------------------------------------------------------------------

print("\nDOCSTRING for PoolData:\n{}".format(PoolData.__doc__))

winners = np.array([[0, 1, 1], [0, 0, 0], [0, 1, 0]])
scores = np.array([[0, 4, 5], [2, 0, 3], [3, 5, 0]])

id = 123
pool_size = 3
fake_pool = PoolData(id, pool_size, ['Alice', 'Bob', 'Charlie'], [1, 2, 3],
                     winners, scores, date="01.01.2021")

print("String representation of fake pool:\n")
print(fake_pool)


# --------------------------------------------------------------------------------
#                         Test pool scraping   --- Dict Version
# --------------------------------------------------------------------------------
# 'https://fie.org/competitions/2020/771'
tournament_url = 'https://fie.org/competitions/2021/1079'
req = requests.get(tournament_url)
soup = BeautifulSoup(req.content, 'html.parser')

script = next(
    soup.find('script', text=re.compile("window._pools = ")).children)
pools_string = [text.strip() for text in script.split(
    ';') if text.strip().startswith('window._pools ')][0]
# pools string = "window._pools = [{...dict info here...}]"
pool_dict = json.loads(pools_string.split(" = ")[1])['pools'][1]


pool_results = get_pool_data_from_dict(pool_dict)

print("Fencers List from Pool #2:")
print(pool_results.fencer_names)
print(pool_results)
