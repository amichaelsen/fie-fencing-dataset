import requests
import json
from datetime import date, datetime
from os import path, stat
from bs4 import BeautifulSoup
import pandas as pd

import tabulate

CACHE_FILENAME = 'fencers/fencer_cache.txt'


def get_fencer_bio_from_soup(soup, fencer_ID):
    """
    Takes a BeautifulSoup object for the fencer's webpage and returns non-weapon/category bio data
    """
    fencer_name = ""
    hand = ""
    age = ""
    nationality = ""

    # find <h1 class="AthleteHero-fencerName">
    name_tag = soup.find('h1', class_='AthleteHero-fencerName')
    fencer_name = name_tag.get_text()

    # first approximation to get nationality

    # window._tabOpponents = [{"date":"2021-04-10",
    #                           "fencer1":{"id":"52027","name":"PARK Faith","nationality":"USA","isWinner":true,"score":"5"},
    #                           "fencer2":{"id":49302,"name":"CARDOSO Elisabete","nationality":"POR","isWinner":false,"score":"2"},"competition":"Championnats du monde juniors-cadets","season":"2021","competitionId":"235","city":"Le Caire"},
    script = next(soup.find('script', id="js-single-athlete").children)
    # each variable window._XXXX is ';' separated and window._tabOpponents contains data that includes fencer nationality
    var_list = script.split(';')

    # get window._tabOpponents Data
    tabOpp_var_name = "window._tabOpponents "
    tabOpp_string = [text.strip() for text in var_list if
                     text.strip().startswith(tabOpp_var_name)][0]
    tabOpp_list = json.loads(tabOpp_string.split(" = ")[1])
    if len(tabOpp_list) > 0 and int(tabOpp_list[0]['fencer1']['id']) == fencer_ID:
        nationality = tabOpp_list[0]['fencer1']['nationality']

    info_div = soup.find('div', class_="ProfileInfo")

    for info_item in info_div.children:
        if(info_item.get_text().startswith('Hand')):
            hand = list(info_item.children)[1].get_text()
        elif(info_item.get_text().startswith('Age')):
            age = list(info_item.children)[1].get_text()

    return {'name': fencer_name,
            'nationality': nationality,
            'hand': hand, 'age': age}


def save_fencer_to_cache(cache_filename, fencer_ID, fencer_dict):

    # save data to cache for potential future use (even if not drawing from cache)
    if((not path.exists(cache_filename)) or (stat(cache_filename).st_size == 0)):
        # cache file does not exist or is empty (cannt be json.loaded)
        with open(cache_filename, 'w') as fencer_cache_write:
            new_cache_dict = {fencer_ID: fencer_dict}
            json.dump(new_cache_dict, fencer_cache_write)
    else:
        with open(cache_filename) as fencer_cache_read:
            cached_data = json.load(fencer_cache_read)
            # store fencer dict, overwrite old data if it exists
            cached_data[fencer_ID] = fencer_dict
            with open(cache_filename, 'w') as fencer_cache_write:
                json.dump(cached_data, fencer_cache_write)


def get_fencer_curr_rankings_list_from_soup(soup, fencer_ID):
    info_div = soup.find('div', class_="ProfileInfo")

    weapon = ""
    points = 0
    rank = ""
    category = ""
    season = ""
    for info_item in info_div.children:
        if(info_item.get_text().startswith('foil') or info_item.get_text().startswith('epee') or info_item.get_text().startswith('sabre')):
            weapon = info_item.get_text()
        # second text is either value of points (may be 0) or "-"
        elif(info_item.get_text().startswith('Pts')):
            pts_text = list(info_item.children)[1].get_text()
            try:
                points = float(pts_text)
            except ValueError:
                points = 0
        elif(info_item.get_text().startswith('Hand')):
            hand = list(info_item.children)[1].get_text()
        elif(info_item.get_text().startswith('Age')):
            age = list(info_item.children)[1].get_text()
        elif(info_item.get_text().startswith('Rank')):
            rank = list(info_item.children)[1].get_text()

    fencer_rankings_list = [{'id': fencer_ID, 'weapon': weapon, 'category': category,
                             'season': season, 'points': points, 'rank': rank}]

    return fencer_rankings_list

def get_fencer_rankings_list_from_soup(soup, fencer_ID, url):
    return 

def get_fencer_info_from_ID(fencer_ID, use_cache=True):
    """
    Takes url for athlete page and returns dict of fencer data 

        Output:
        -------
        fencer_dict : dict 

    """
    # Check if fencer is in cache (uses potentially old data)

    if use_cache and path.exists(CACHE_FILENAME) and stat(CACHE_FILENAME).st_size > 0:
        # check if fencer data is already stored
        with open(CACHE_FILENAME) as fencer_cache_read:
            cached_data = json.load(fencer_cache_read)
            if str(fencer_ID) in cached_data.keys():
                fencer_dict = cached_data[str(fencer_ID)]
                return fencer_dict

    # If not cached or using cache, pull fencer data from url
    fencer_url = "https://fie.org/athletes/"+str(fencer_ID)
    req = requests.get(fencer_url)
    soup = BeautifulSoup(req.content, 'html.parser')

    fencer_id_dict = {'id': fencer_ID, 'url': fencer_url,
                      'date_accessed': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    fencer_bio_dict = get_fencer_bio_from_soup(soup, fencer_ID)
    
    fencer_rankings_list = get_fencer_curr_rankings_list_from_soup(
        soup, fencer_ID)

    fencer_bio_dict = {**fencer_bio_dict, **fencer_id_dict}
    fencer_rankings_dict = {'rankings': fencer_rankings_list}

    # save fencer data to cache
    fencer_dict = {**fencer_bio_dict, **fencer_rankings_dict}
    save_fencer_to_cache(cache_filename=CACHE_FILENAME,
                         fencer_ID=fencer_ID,
                         fencer_dict=fencer_dict)

    return fencer_dict


def convert_list_to_dataframe_with_multi_index(list_of_results, column_names, index_names):
    """
    Takes a list of dict data and returns a pd.DataFrame with multiIndex from specified columns
    """
    # create dataframe from list
    dataframe = pd.DataFrame(data=list_of_results, columns=column_names)

    # construct multiIndex (sort first to group by heirarchy)
    idx_array = []
    dataframe.sort_values(by=index_names, inplace=True)
    for name in index_names:
        idx_array.append(dataframe[name])
    new_index = pd.MultiIndex.from_arrays(idx_array)

    # convert to multi index and drop columns used to create multiIndex
    dataframe.index = new_index
    dataframe = dataframe.drop(columns=index_names)

    return dataframe
