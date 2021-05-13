from os import path, stat
import json
import pandas as pd
from dataframe_columns import FENCERS_BIO_DF_COLS, FENCERS_RANKINGS_DF_COLS, FENCERS_RANKINGS_MULTI_INDEX
from dataframe_columns import convert_list_to_dataframe_with_multi_index
from progress.bar import Bar


def save_dict_to_cache(cache_filename, dict_key, dict_value):
    """Saves {dict_key:dict_value} to dict cached at cache_filename"""
    # save data to cache for potential future use (even if not drawing from cache)
    if((not path.exists(cache_filename)) or (stat(cache_filename).st_size == 0)):
        # cache file does not exist or is empty (cannt be json.loaded)
        with open(cache_filename, 'w') as write_file:
            new_cache_dict = {dict_key: dict_value}
            json.dump(new_cache_dict, write_file)
    else:
        with open(cache_filename) as read_file:
            cached_data = json.load(read_file)
            # store tournament dict, overwrite old data if it exists
            cached_data[dict_key] = dict_value
            with open(cache_filename, 'w') as write_file:
                json.dump(cached_data, write_file)


def clear_null_entries(cache_filename):
    """Removes any keys with None values from dict stored at cache_filename"""
    with open(cache_filename) as read_file:
        cached_data = json.load(read_file)
        for key, value in list(cached_data.items()):
            if value is None:
                del cached_data[key]
        with open(cache_filename, 'w') as write_file:
            json.dump(cached_data, write_file)


def load_all_cached_fencers_bio():
    """Returns dataframe with all fencer bio info from fencers/fencer_cache.txt"""
    cache_filename = 'fencers/fencer_cache.txt'
    with open(cache_filename) as read_file:
        cached_data = json.load(read_file)
        print(type(cached_data.values()))
    fencers_bio_dataframe = pd.DataFrame(
        data=cached_data.values(), columns=FENCERS_BIO_DF_COLS)
    return fencers_bio_dataframe


def load_all_cached_fencers_rankings():
    """Returns dataframe with all fencer rankings info from fencers/fencer_cache.txt"""
    cache_filename = 'fencers/fencer_cache.txt'
    fencer_rankings_list = []
    with open(cache_filename) as read_file:
        cached_data = json.load(read_file)
        print(type(cached_data.values()))
        for value in cached_data.values():
            fencer_rankings_list = fencer_rankings_list + value['rankings']
    fencers_rankings_df = convert_list_to_dataframe_with_multi_index(
        list_of_data=fencer_rankings_list,
        column_names=FENCERS_RANKINGS_DF_COLS, index_names=FENCERS_RANKINGS_MULTI_INDEX)
    return fencers_rankings_df

def get_tournament_from_fencer(fencer_ID):
    """Returns list of tournament unique_IDs the fencer appeared in from tournaments/tournament_cache.txt"""
    cache_filename = 'tournaments/tournament_cache.txt'
    with open(cache_filename) as read_file:
        cached_data = json.load(read_file)
    fencer_tournaments = []
    for tourn_id, tourn_data in Bar('Checking tournaments ').iter(cached_data.items()):
        if fencer_ID in tourn_data['fencer_list']:
            fencer_tournaments.append(tourn_data['unique_ID'])
    return fencer_tournaments
