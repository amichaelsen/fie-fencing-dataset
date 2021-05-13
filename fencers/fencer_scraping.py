import requests
import json
from datetime import date, datetime
from os import path, stat
from bs4 import BeautifulSoup
import pandas as pd
import tabulate
from progress.bar import Bar

from soup_scraping import get_json_var_from_script
from caching_methods import save_dict_to_cache
from dataframe_columns import FENCERS_RANKINGS_MULTI_INDEX, FENCERS_RANKINGS_DF_COLS, FENCERS_BIO_DF_COLS

CACHE_FILENAME = 'fencers/fencer_cache.txt'


def get_req_content(fencer_ID, use_req_cache=True):
    """
    Gets athlete page content, either from cache or requests, stores in cache if new

        Input:
        ------
        fencer_ID : int 
            ID for the fencer to get page content for
        use_req_cache : boolean (default True)
            Flag allowing use of cache, if false will always pull 
            new request and load and store the new data to cache

        Output:
        ------
        content : bytes
            Represents the `content` of a requests.get to the fencers url
    """
    path_name = "fencers/athlete_pages/"+str(fencer_ID)+".txt"
    if (path.exists(path_name) and use_req_cache):
        with open(path_name, 'rb') as cache_file:
            content = cache_file.read()
    else:
        fencer_url = "https://fie.org/athletes/"+str(fencer_ID)
        req = requests.get(fencer_url)
        content = req.content
        with open(path_name, 'wb') as cache_file:
            cache_file.write(content)
    return content


def get_fencer_nationality_data(soup):
    """
    From the fencer's soup extracts country_code and country_name 

        Input:
        ------
        soup: bs4.BeautifulSoup
            A BeautifulSoup object created from the request content 
            from a fencers page (using 'html.parser')

        Output:
        -------
        country_code : str 
            Three letter code for fencer's country 
        country_name : str 
            Full name of the fencer's country 
    """
    try:
        flag_span = soup.find('span', class_='AthleteHero-flag')
        class_labels = flag_span['class']  # should be the third
    except:
        print("\n -->Failed to find <span class='AthleteHero-flag' for fencer")
        raise ValueError
    flag_indicator = class_labels[2]
    flag_label = flag_indicator.split('--')[1].upper()
    with open('fencers/flag_to_country_code.txt') as flag_file:
        with open('fencers/country_code_to_name.txt') as country_file:
            flag_data = json.load(flag_file)
            country_data = json.load(country_file)
            country_code = flag_data.get(flag_label, flag_label)
            country_name = country_data.get(country_code, flag_label)
    return country_code, country_name


def get_fencer_bio_from_soup(soup, fencer_ID):
    """
    Takes a BeautifulSoup object for the fencer's webpage and returns non-weapon/category bio data

        Input:
        ------
        soup: bs4.BeautifulSoup
            A BeautifulSoup object created from the request content 
            from a fencers page (using 'html.parser')
        fencer_ID : int
            ID for the fencer to get bio for

        Output:
        ------
        fencer_bio_dict : dict 
            Dictionary with fencer's bio data
                keys : 'name', 'country_code', 'country', 'hand', 'age'

    """
    fencer_name = ""
    hand = ""
    age = ""
    country_code = ""
    country_name = ""

    # find <h1 class="AthleteHero-fencerName">
    try:
        name_tag = soup.find('h1', class_='AthleteHero-fencerName')
        fencer_name = name_tag.get_text()
    except:
        print("\nFailed to read name from name_tag for fencer ID: {}".format(fencer_ID))

    # get nationality data
    try:
        country_code, country_name = get_fencer_nationality_data(soup)
    except:
        print("\n  WARNING:  Issue loading country data for fencer {}".format(fencer_ID))

    try:
        info_div = soup.find('div', class_="ProfileInfo")
        for info_item in info_div.children:
            if(info_item.get_text().startswith('Hand')):
                hand = list(info_item.children)[1].get_text()
            elif(info_item.get_text().startswith('Age')):
                age = list(info_item.children)[1].get_text()
    except:
        print("\nFailed to info_div from ProfileInfo for fencer ID: {}".format(fencer_ID))

    fencer_bio_dict = {'name': fencer_name,
                       'country_code': country_code,
                       'country': country_name,
                       'hand': hand, 'age': age}
    return fencer_bio_dict


def get_fencer_weapon_rankings_list_from_soup(soup):
    """
    Takes a BeautifulSoup object for the fencer's webpage and returns list of ranking data
    """
    # get window._tabRankings Data
    tabRank_var_name = "window._tabRanking "
    fencer_rankings_list = get_json_var_from_script(
        soup=soup, script_id="js-single-athlete", var_name=tabRank_var_name)
    return fencer_rankings_list


def get_fencer_rankings_list_from_soup(soup, fencer_ID, url):
    """
    Takes a BeautifulSoup for the fencer, their ID, and URL, and returns a list of rankings

        Input:
        ------
        soup: bs4.BeautifulSoup
            A BeautifulSoup object created from the request content 
            from a fencers page (using 'html.parser')
        fencer_ID : int
            ID for the fencer to get rankings data for
        url : str 
            URL of the fencers page to make separate weapon page calls

        Output:
        -------
        fencer_rankings_list : list
            List of rankings, each represented as a dict with 
            keys : "id", "rank", "points", "weapon", "season", "category"
    """
    # get weapons list from <select class="ProfileInfo-weaponDropdown...">
    weapon_dropdown = soup.find('select', class_="ProfileInfo-weaponDropdown")

    if(not weapon_dropdown or len(list(weapon_dropdown.children)) == 1):  # only 1 weapon, can re-use soup
        # only one weapon, so use current soup to read rankings
        fencer_rankings_list = get_fencer_weapon_rankings_list_from_soup(soup)
    else:
        # multiple weapons to process, read each and add to a rankings list
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

    # update their JSON labels for processing
    for rank_item in fencer_rankings_list:
        # add fencer ID for combining
        rank_item.update({"id": fencer_ID})
        # 'point' -> 'points'
        rank_item['points'] = rank_item.pop(
            'point')

    return fencer_rankings_list


def get_fencer_info_from_ID(fencer_ID, use_data_cache=True, use_req_cache=True):
    """
    Takes fencer ID and cache flags and returns and saves dict with bio and rankings data

        Input:
        -------
        fencer_ID : int
        use_data_cache : boolean (default True)
            Indicates whether to use data in fencers/fencer_cache.txt or reprocess data
        use_req_cache  : boolean (default True)
            Indicates whether to use req.content in fencers/ahtlete_pages/ or reload request

        Output:
        -------
        fencer_dict : dict 
            Dictionary containing both bio and rankings data for a fencer 
            Keys are combined from fencer_bio_dict (from get_fencer_bio_from_soup)
                and fencer_rankings_dict (from get_fencer_rankings_list_from_soup)

        Caching:
        --------
        fencer_cache.txt
            If creating fencer_dict (not loading from fencer_cache.txt) saves to cache
        athlete_pages/ 
            If loading request page (not loading from athlete_pages/) saves to cache
    """

    # Check if fencer is in cache (uses potentially old data)
    if use_data_cache and path.exists(CACHE_FILENAME) and stat(CACHE_FILENAME).st_size > 0:
        # check if fencer data is already stored
        with open(CACHE_FILENAME) as fencer_cache_read:
            cached_data = json.load(fencer_cache_read)
            if str(fencer_ID) in cached_data.keys():
                fencer_dict = cached_data[str(fencer_ID)]
                return fencer_dict

    # Load fencer request data from url OR req_cache
    content = get_req_content(fencer_ID=fencer_ID, use_req_cache=use_req_cache)
    soup = BeautifulSoup(content, 'html.parser')

    fencer_url = "https://fie.org/athletes/"+str(fencer_ID)
    fencer_id_dict = {'id': fencer_ID, 'url': fencer_url,
                      'date_accessed': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    fencer_bio_dict = get_fencer_bio_from_soup(soup, fencer_ID)

    fencer_rankings_list = get_fencer_rankings_list_from_soup(
        soup, fencer_ID, fencer_url)

    fencer_bio_dict = {**fencer_bio_dict, **fencer_id_dict}
    fencer_rankings_dict = {'rankings': fencer_rankings_list}

    # save fencer data to cache
    fencer_dict = {**fencer_bio_dict, **fencer_rankings_dict}
    save_dict_to_cache(cache_filename=CACHE_FILENAME,
                       dict_key=fencer_ID,
                       dict_value=fencer_dict)

    return fencer_dict


def load_fencer_data(all_fencer_bio_data_list, all_fencer_ranking_data_list, fencer_ID_list, use_data_cache=True, use_req_cache=True, label="fencer data"):
    """
    Loads fencer data from list with a progress bar and optional progress bar label

        Input:
        ------
        all_fencer_bio_data_list : list
            Accumulating list of bio data for all fencers being processed
        all_fencer_ranking_data_list : list 
            Accumulating list of rankings data for all fencers being processed

        fencer_ID_list : list
            List of IDs for fencers to be process and added to output lists

        use_data_cache : boolean (default True)
            Indicates whether to use data in fencers/fencer_cache.txt or reprocess data
        use_req_cache  : boolean (default True)
            Indicates whether to use req.content in fencers/ahtlete_pages/ or reload request

        label : boolean (default "fencer data")
            Label to use for progress bar (could indicate if fencers are cached/uncached)

        Output:
        -------
        Does not return anything, but makes updates to:
            all_fencer_bio_data_list,
            all_fencer_ranking_data_list
    """
    if len(fencer_ID_list) == 0:
        return
    for fencer_ID in Bar('  Loading {}    '.format(label)).iter(fencer_ID_list):
        fencer_info_dict = get_fencer_info_from_ID(
            fencer_ID, use_req_cache=use_req_cache, use_data_cache=use_data_cache)
        fencer_rankings_list = fencer_info_dict.pop('rankings')
        all_fencer_bio_data_list.append(fencer_info_dict)
        all_fencer_ranking_data_list += fencer_rankings_list


def get_fencer_data_lists_from_ID_list(fencer_ID_list, use_data_cache=True, use_req_cache=True):
    """
    Loads fencer data from list with a progress bar and optional progress bar label

        Input:
        ------
        fencer_ID_list : list
            List of IDs for fencers to be process and added to output lists

        use_data_cache : boolean (default True)
            Indicates whether to use data in fencers/fencer_cache.txt or reprocess data
        use_req_cache  : boolean (default True)
            Indicates whether to use req.content in fencers/ahtlete_pages/ or reload request

        Output:
        -------
        all_fencer_bio_data_list : list
            List of bio data for all fencers in fencer_ID_list
        all_fencer_ranking_data_list : list 
            :ist of rankings data for all fencers in fencer_ID_list
    """
    if 0 in fencer_ID_list:
        fencer_ID_list.remove(0)

    # TODO I think this can safely be removed now...
    if len(fencer_ID_list) == 0:
        return [], []

    all_fencer_bio_data_list = []
    all_fencer_ranking_data_list = []

    print("Processing {} fencers by ID ".format(len(fencer_ID_list)), end="")

    # split fencers into cached and not for progress bars
    if use_data_cache:
        with open(CACHE_FILENAME) as fencer_cache:
            cached_data = json.load(fencer_cache)
            cached_IDs = [int(id) for id in list(
                cached_data.keys()) if int(id) in fencer_ID_list]
            print("({} cached fencers)".format(len(cached_IDs)))
    else:
        cached_IDs = []
        print("")
    uncached_IDs = list(set(fencer_ID_list) - set(cached_IDs))

    # load fencer data for uncached then cached and 
    # add data to all_fencer_bio_data_list, all_fencer_ranking_data_list
    load_fencer_data(all_fencer_bio_data_list, all_fencer_ranking_data_list,
                     uncached_IDs, use_data_cache=use_data_cache, use_req_cache=use_req_cache, label="uncached fencers")

    load_fencer_data(all_fencer_bio_data_list, all_fencer_ranking_data_list,
                     cached_IDs, use_data_cache=use_data_cache, use_req_cache=use_req_cache, label="cached fencers  ")

    return all_fencer_bio_data_list, all_fencer_ranking_data_list
