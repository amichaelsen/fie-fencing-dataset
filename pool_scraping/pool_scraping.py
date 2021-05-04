from bs4 import BeautifulSoup
import numpy as np
from pool_data import poolData


def get_pool_data(html_filename):
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

    return poolData(pool_size, athlete_name_list, athlete_ID_list, winners_array, score_array)
