import numpy as np
import requests
import re
import json
from bs4 import BeautifulSoup
from pools.pool_data import poolData
from pools.pool_scraping import get_pool_data_from_dict, get_pool_data_from_html


# --------------------------------------------------------------------------------
#                         Test poolData class
# --------------------------------------------------------------------------------

print("\nDOCSTRING for PoolData:\n{}".format(poolData.__doc__))

winners = np.array([[0, 1, 1], [0, 0, 0], [0, 1, 0]])
scores = np.array([[0, 4, 5], [2, 0, 3], [3, 5, 0]])

id = 123
pool_size = 3
fake_pool = poolData(id, pool_size, ['Alice', 'Bob', 'Charlie'], [1, 2, 3],
                     winners, scores)

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


fencers, pool_results = get_pool_data_from_dict(pool_dict)

print("Fencers List from Pool #2:")
print(fencers)
print(pool_results)

# --------------------------------------------------------------------------------
#                         Test pool scraping   --- HTML Version
# --------------------------------------------------------------------------------

test_pool = "pools/test_pool.html"
loaded_pool = get_pool_data_from_html(test_pool)
print("String representation of pool loaded from {}:\n".format(test_pool))
print(loaded_pool)

print("Winners Array:\n{}\n".format(loaded_pool.winners))

print("Score Array:\n{}\n".format(loaded_pool.scores))


# Print results of a single match
fencer_idx = 2
opponent_idx = 4
print("Showing result from single match (fencers #{} and #{}):".format(
    fencer_idx+1, opponent_idx+1))

print("   {name1:<15} (ID {id1}) vs {name2:<15} (ID {id2})\n\
        Score:  {score1} - {score2}     Winner: {winner}\n".format(
    name1=loaded_pool.get_fencer_name_by_idx(fencer_idx), name2=loaded_pool.get_fencer_name_by_idx(opponent_idx),
    id1=loaded_pool.get_fencer_ID_by_idx(fencer_idx), id2=loaded_pool.get_fencer_ID_by_idx(opponent_idx),
    score1=loaded_pool.scores[fencer_idx][opponent_idx],
    score2=loaded_pool.scores[opponent_idx][fencer_idx],
    winner=loaded_pool.get_fencer_name_by_idx(fencer_idx) if loaded_pool.winners[fencer_idx][opponent_idx] == 1 else loaded_pool.get_name_by_idx(opponent_idx)))
