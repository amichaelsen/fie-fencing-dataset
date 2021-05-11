from bs4 import BeautifulSoup
import numpy as np
from pools.pool_data import PoolData


def extract_matches(pool):
    """ Creates an interator of the cells in the pool grid from pool dict """
    for row in pool['rows']:
        if int(row['fencerId']) > 0:
            for match in row['matches']:
                yield match


def get_pool_data_from_dict(pool_dict):
    """
    Takes the dict representation of a pool and reads it to a PoolData object

        Input:
        ------
        pool_dict : dict
            A dictionary containing the following keys:
            ['poolId', 'piste', 'time', 'referee', 'rows']

            For more information about how this dictionary is 
            being extracted from the website see:
                tournament_scraping/exploring_json_extraction.py

        Output:
        ------
        fencer_list : list[dict]
            A list of fencers represented by dicts with the keys:
            ['nationality', 'name', 'fencerId']

        pool : PoolData
            A PoolData object (see pool_data.py) containing the names, IDs,
            of every fencer along with wins and scores arrays. 
    """
    # generate list of fencers
    fencer_names = []
    fencer_IDs = []
    fencer_list = []
    for row in pool_dict['rows']:
        fencer_dict = {k: v for k, v in row.items(
        ) if k in ['name', 'fencerId']}
        fencer_list.append(fencer_dict)
        fencer_names.append(row['name'])
        fencer_IDs.append(row['fencerId'])

    pool_size = len(fencer_IDs)
    winners_array = np.zeros((pool_size, pool_size), dtype=int)
    score_array = np.zeros((pool_size, pool_size), dtype=int)

    # generate winners and score array for a pool (relies on pool_size)
    for idx, bout in enumerate(extract_matches(pool_dict)):
        # print("match #{}: {}".format(idx+1, bout))
        if bout:
            score = bout['score']
            if bout['v']:
                winners_array[idx // pool_size][idx % pool_size] = 1
            score_array[idx // pool_size][idx % pool_size] = score

    id = pool_dict['poolId']
    date = pool_dict['time']

    pool = PoolData(id, pool_size, fencer_names,
                    fencer_IDs, winners_array.tolist(), score_array.tolist(), date)

    return pool
