import requests
import json
from datetime import date, datetime
from os import path, stat
from bs4 import BeautifulSoup
import pandas as pd
import tabulate
from progress.bar import Bar

from soup_scraping import get_json_var_from_script
from dataframe_columns import FENCERS_RANKINGS_MULTI_INDEX, FENCERS_RANKINGS_DF_COLS, FENCERS_BIO_DF_COLS

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
    try:
        name_tag = soup.find('h1', class_='AthleteHero-fencerName')
        fencer_name = name_tag.get_text()
    except:
        print("\nFailed to read name from name_tag for fencer ID: {}".format(fencer_ID))

    # first approximation to get nationality
    # window._tabOpponents = [{"date":"2021-04-10", "fencer1":{"id":"52027","name":"PARK Faith","nationality":"USA","isWinner":true,"score":"5"},
    #                                               "fencer2":{"id":49302,"name":"CARDOSO Elisabete","nationality":"POR","isWinner":false,"score":"2"},"competition":"Championnats du monde juniors-cadets","season":"2021","competitionId":"235","city":"Le Caire"},
    tabOpp_list = get_json_var_from_script(
        soup=soup, script_id="js-single-athlete", var_name="window._tabOpponents")
    if len(tabOpp_list) > 0 and int(tabOpp_list[0]['fencer1']['id']) == fencer_ID:
        nationality = tabOpp_list[0]['fencer1']['nationality']

    info_div = soup.find('div', class_="ProfileInfo")

    try:
        for info_item in info_div.children:
            if(info_item.get_text().startswith('Hand')):
                hand = list(info_item.children)[1].get_text()
            elif(info_item.get_text().startswith('Age')):
                age = list(info_item.children)[1].get_text()
    except:
        print("\nFailed to info_div from ProfileInfo for fencer ID: {}".format(fencer_ID))

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


def get_fencer_weapon_rankings_list_from_soup(soup):
    # get window._tabRankings Data
    tabRank_var_name = "window._tabRanking "
    fencer_rankings_list = get_json_var_from_script(
        soup=soup, script_id="js-single-athlete", var_name=tabRank_var_name)
    return fencer_rankings_list


def get_fencer_rankings_list_from_soup(soup, fencer_ID, url):
    """
    TODO 
    """
    # get weapons list from <select class="ProfileInfo-weaponDropdown...">
    weapon_dropdown = soup.find('select', class_="ProfileInfo-weaponDropdown")
    if(not weapon_dropdown or len(list(weapon_dropdown.children)) == 1):  # only 1 weapon, can re-use soup
        fencer_rankings_list = get_fencer_weapon_rankings_list_from_soup(soup)
    else:
        fencer_rankings_list = []
        for weapon in weapon_dropdown.children:
            # create soup for page with specific weapon
            weapon_value = weapon['value']
            weapon_url = url + "?weapon="+weapon_value
            weapon_req = requests.get(weapon_url)
            weapon_soup = BeautifulSoup(weapon_req.content, 'html.parser')
            # process page for weapon specific rankings
            fencer_weapon_rankings_list = get_fencer_weapon_rankings_list_from_soup(
                weapon_soup)
            fencer_rankings_list += fencer_weapon_rankings_list

    for rank_item in fencer_rankings_list:
        rank_item.update({"id": fencer_ID})
        rank_item['points'] = rank_item.pop(
            'point')  # relabel from JSON 'point'

    return fencer_rankings_list


def get_fencer_info_from_ID(fencer_ID, use_cache=True):
    """
    Takes url for athlete page and returns dict of fencer data 

        Output:
        -------
        fencer_dict : dict 
            TODO Describe the dict structure here... 

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

    fencer_rankings_list = get_fencer_rankings_list_from_soup(
        soup, fencer_ID, fencer_url)

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


def get_fencer_dataframes_from_ID_list(fencer_ID_list, use_cache=True):
    all_fencer_bio_data_list = []
    all_fencer_ranking_data_list = []
    print("Processing fencers by ID")
    print(fencer_ID_list)

    for fencer_ID in Bar('  Loading fencers    ').iter(fencer_ID_list):
        fencer_info_dict = get_fencer_info_from_ID(fencer_ID, use_cache)
        fencer_rankings_list = fencer_info_dict.pop('rankings')
        all_fencer_bio_data_list.append(fencer_info_dict)
        all_fencer_ranking_data_list += fencer_rankings_list

        fencers_bio_dataframe = pd.DataFrame(
            data=all_fencer_bio_data_list, columns=FENCERS_BIO_DF_COLS)
        fencers_rankings_dataframe = convert_list_to_dataframe_with_multi_index(
            list_of_results=all_fencer_ranking_data_list,
            column_names=FENCERS_RANKINGS_DF_COLS, index_names=FENCERS_RANKINGS_MULTI_INDEX)

    return fencers_bio_dataframe, fencers_rankings_dataframe
