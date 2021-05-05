from bs4 import BeautifulSoup
import numpy as np
from pool_data import poolData



def extract_matches(pool):
    """ Creates an interator of the cells in the pool grid from pool dict """
    for row in pool['rows']:
        for match in row['matches']:
            yield match



def get_pool_data_from_dict(pool_dict):
    """
    Takes the html of a pool and reads it to a poolData object

        Input:
        ------
        pool_dict : dict
            A dictionary containing the following keys:
            ['poolId', 'piste', 'time', 'referee', 'rows']
            where 'rows' is a list of dicts containing row 
            information for the pool score grid

        Output:
        ------
        fencer_list : list[dict]
            A list of fencers represented by dicts with the keys:
            ['nationality', 'name', 'fencerId']

        pool : poolData
            A poolData object (see pool_data.py) containing the names, IDs,
            of every fencer along with wins and scores arrays. 
    """
    # generate list of fencers
    fencer_names = []
    fencer_IDs = []
    fencer_list = [] 
    for row in pool_dict['rows']:
        fencer_dict = {k:v for k,v in row.items() if k in ['nationality','name','fencerId']}
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

    pool = poolData(pool_size, fencer_names,
                    fencer_IDs, winners_array, score_array)

    return fencer_list, pool

# initial pool scraping using html file name


def get_pool_data_from_html(html_filename):
    """
    Takes the html of a pool and reads it to a poolData object

        Input:
        ------
        html_filename : str
            A string containing file location for the html from a pool.
            The file should have its outermost html tag as:
              <div class="ResultsPool-pool ResultsPool-pool">...</div>

        Output:
        ------
        pool : poolData
            A poolData object (see pool_data.py) containing the names, IDs,
            of every fencer along with wins and scores arrays. 
    """
    with open(html_filename) as html_pool:
        # caution: contains chlorine!
        pool_soup = BeautifulSoup(html_pool, 'html.parser')

    athlete_name_list = []
    athlete_ID_list = []

    # generate list of atheletes and IDs from <a href="/athletes/49321">SMITHISUKUL Chayada</a>
    for athlete in pool_soup.find_all('a'):
        link = athlete.get('href')
        link_pieces = link.split("/")
        athlete_name_list.append(athlete.get_text())
        athlete_ID_list.append(link_pieces[2])

    pool_size = len(athlete_name_list)
    winners_array = np.zeros((pool_size, pool_size), dtype=int)
    score_array = np.zeros((pool_size, pool_size), dtype=int)

    # read score entries and store data in a winners and score array
    for idx, entry in enumerate(pool_soup.find_all('div', class_="ResultsPool-score")):
        score = entry.get_text().strip()
        if score:
            # scores are stored in a 'V/5', 'D/2' format
            score_pieces = score.split("/")
            if score_pieces[0] == 'V':
                winners_array[idx // pool_size][idx % pool_size] = 1
            score_array[idx // pool_size][idx % pool_size] = score_pieces[1]

    pool = poolData(pool_size, athlete_name_list,
                    athlete_ID_list, winners_array, score_array)
    return pool
