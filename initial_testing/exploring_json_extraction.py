import requests
import re
import json
import numpy as np
from bs4 import BeautifulSoup

req = requests.get('https://fie.org/competitions/2020/771')
soup = BeautifulSoup(req.content, 'html.parser')


# ---------------------------------------------
# Step 1: Extract the string with Pools Data
# ---------------------------------------------


# pulls out the <Script> with the json data for all pools
# could also use 'id="js-competition"'
script = next(soup.find('script', text=re.compile("window._pools = ")).children)
print("type for script: {}".format(type(script)))

# creates of list of the objects stored in the json
temp_list = script.split(';')
print("type for temp_list: {}".format(type(temp_list)))
print("type for text in script.split(';'): {}".format(
    type(script.split(";")[0])))

print("start of text string for each split:")
for text in script.split(';'):
    print("    ", end="")
    print(text.strip()[0:100])
    # need to specify up to " " here to distinguish frmo window._poolsMobile
    if text.strip().startswith('window._pools '):
        pools_string = text.strip()

print("start of string for window._pools:\n    {}".format(pools_string[0:100]))


# ---------------------------------------------
# Step 2: Extract dictionary data for Pools
# ---------------------------------------------


# pools string = "window._pools = [{...dict info here...}]"
extract_json_pools = pools_string.split(" = ")[1]


# load json info into a python dict object
json_data = json.loads(extract_json_pools)  # type(json_data) = <class 'dict'>
# print("type for json_data: {}".format(type(json_data)))
print("json_data keys: {}".format(json_data.keys()))

# pools is a list with an entry for each pool
pools = json_data['pools']  # type(pools) = <class 'list'>
# print(type(pools))
print("number of pools found: {}".format(len(pools)))

# select the first pool to examine
pool = pools[0]  # type(pool) = <class 'dict'>
# print("type for pool: {}".format(type(pool)))

# 'rows' value contains the pool results information")
print("pool keys: {}".format(pool.keys()))

rows = pool['rows']  # type(rows) = <class 'list'>
# print("type for rows: {}".format(type(rows)))

# select the first row of pool to examine,
# each row is a dictionary with results for a single fencer
row = rows[0]  # type(row) = <class 'dict'>
print("type for single row in rows: {}".format(type(row)))

# key 'versus' contains the table results for all bouts (not summary stats)
print("row keys: {}".format(row.keys()))

# ---------------------------------------------
# Step 3: Interpret 'versus' structure
# ---------------------------------------------

# row bouts is list of each bout
row_bouts = row['matches']  # type(row_bouts) = <class 'list'>
print("type for row_bouts: {}".format(type(row_bouts)))
print("number of bouts in this row: {}".format(len(row_bouts)))

# 'None' fills the empty spot on the diagonal
# each other bout is a dict {'score': int, 'v': bool}
print(row_bouts)


# generate list of fencers
def get_fencers(pool):
    fencer_names = []
    fencer_IDs = []
    for row in pool['rows']:
        fencer_names.append(row['name'])
        fencer_IDs.append(row['fencerId'])
    return fencer_names, fencer_IDs

names, ids = get_fencers(pool)

print(names)
print(ids)


pool_size = len(row_bouts)

winners_array = np.zeros((pool_size, pool_size), dtype=int)
score_array = np.zeros((pool_size, pool_size), dtype=int)

'''
pull out a list of indidual "bout" score from pools grid
each bout represented by a dict {'score': int, 'v': bool}
'''
def extract_matches(pool):
    for row in pool['rows']:
        for match in row['matches']:
            yield match


# generate winners and score array for a pool (relies on pool_size)
for idx, bout in enumerate(extract_matches(pool)):
    # print("match #{}: {}".format(idx+1, bout))
    if bout:
        score = bout['score']
        if bout['v']:
            winners_array[idx // pool_size][idx % pool_size] = 1
        score_array[idx // pool_size][idx % pool_size] = score


print(score_array)
