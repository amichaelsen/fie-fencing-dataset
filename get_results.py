import pandas as pd
import random
from progress.bar import Bar
import requests
import math
import json
from os import path, stat

from dataframe_columns import BOUTS_DF_COLS, TOURNAMENTS_DF_COLS, FENCERS_BIO_DF_COLS, FENCERS_RANKINGS_DF_COLS, FENCERS_RANKINGS_MULTI_INDEX
from dataframe_columns import multiIndex_relabeler, make_season_from_year
from tournaments.tournament_scraping import create_tournament_data_from_url, compile_bout_dict_list_from_tournament_data
from tournaments.tournament_data import TournamentData
from fencers.fencer_scraping import get_fencer_data_lists_from_ID_list, convert_list_to_dataframe_with_multi_index
from soup_scraping import get_search_params
from caching_methods import save_dict_to_cache

CACHE_FILENAME = 'tournaments/tournament_cache.txt'


def add_tournament_urls_to_list(url_list, tournament_dict_list):
    for tournament in tournament_dict_list:
        url = "https://fie.org/competitions/" + \
            str(tournament['season'])+"/"+str(tournament['competitionId'])
        url_list.append(url)
    return url_list


def get_url_list_from_seach(search_params):
    url_list = []

    # get first page of results and check if more pages needed
    search_params['fetchPage'] = 1
    search_url = 'https://fie.org/competitions/search'
    req = requests.post(search_url, data=search_params)
    json = req.json()
    # json object sample in initial_testing/request_response.json
    pages_needed = math.ceil(json['totalFound']/json['pageSize'])
    url_list = add_tournament_urls_to_list(url_list, json['items'])
    for p in range(2, pages_needed+1):
        search_params['fetchPage'] = p
        req = requests.post(search_url, data=search_params)
        json = req.json()
        url_list = add_tournament_urls_to_list(url_list, json['items'])

    return url_list


def process_tournament_data_from_urls(list_of_urls, use_cache=True):
    # tournaments_dataframe = pd.DataFrame(columns=TOURNAMENTS_DF_COLS)

    tournaments_dict_list = []
    bouts_dict_list = []
    fencer_ID_list = []

    for tournament_url in Bar('  Loading tournaments').iter(list_of_urls):
        load_from_cache = False
        # Check if tournament is in cache (uses potentially old data)
        if use_cache and path.exists(CACHE_FILENAME) and stat(CACHE_FILENAME).st_size > 0:
            # check if fencer data is already stored
            with open(CACHE_FILENAME) as read_file:
                cached_data = json.load(read_file)
                if str(tournament_url) in cached_data.keys():
                    # may be null if tournament has missing data
                    cached_tournament_dict = cached_data[str(tournament_url)]
                    tournament_bout_dict_list = cached_tournament_dict.pop(
                        'bout_list')
                    tournament_fencer_ID_list = cached_tournament_dict.pop(
                        'fencer_list')
                    tournament_info_dict = cached_tournament_dict.copy()
                    load_from_cache = True

        if not load_from_cache:
            # generate tournament data from url
            has_results_data, tournament_data = create_tournament_data_from_url(
                tournament_url)
            if has_results_data:
                tournament_bout_dict_list = compile_bout_dict_list_from_tournament_data(
                    tournament_data)
                tournament_info_dict = tournament_data.create_tournament_dict()
                tournament_fencer_ID_list = list(
                    tournament_data.fencers_dict.keys())
            else:
                tournament_fencer_ID_list = []
                tournament_bout_dict_list = []
                tournament_info_dict = tournament_data.create_tournament_dict()
                print("\nfound a tournamnet with missing data: {} ".format(tournament_url))
                print("missing data flag is: \'{}\'".format(tournament_info_dict['missing_results_flag']))

            dict_to_cache = {**tournament_info_dict, 'bout_list': tournament_bout_dict_list,
                             'fencer_list': tournament_fencer_ID_list}
            save_dict_to_cache(
                CACHE_FILENAME, tournament_url, dict_to_cache)

        # append tournament data to the list
        fencer_ID_list = list(
            set(fencer_ID_list+tournament_fencer_ID_list))
        bouts_dict_list = bouts_dict_list + tournament_bout_dict_list
        tournaments_dict_list.append(tournament_info_dict)

    return tournaments_dict_list, bouts_dict_list, fencer_ID_list


def cleanup_dataframes(tournaments_dataframe, bouts_dataframe,
                       fencers_bio_dataframe, fencers_rankings_dataframe):
    # expand labels for 'weapon', 'gender' and 'category' in the tournament dataframe
    weapon_dict = {'E': "Epee", "F": "Foil", "S": "Sabre"}
    gender_dict = {"M": "Mens", "F": "Womens"}
    category_dict = {"J": "Junior", "C": "Cadet",
                     "S": "Senior", "V": "Veterans"}
    hand_dict = {"R": "Right", "L": "Left"}

    # relabel keys to full words
    tournaments_dataframe['weapon'] = tournaments_dataframe['weapon'].map(
        weapon_dict)
    tournaments_dataframe['gender'] = tournaments_dataframe['gender'].map(
        gender_dict)
    tournaments_dataframe['category'] = tournaments_dataframe['category'].map(
        category_dict)

    fencers_bio_dataframe['hand'] = fencers_bio_dataframe['hand'].map(
        hand_dict)

    # no entries -> no index to label 
    if fencers_rankings_dataframe.size > 0:
        multiIndex_relabeler(fencers_rankings_dataframe,
                            level=1, mapper=weapon_dict)
        multiIndex_relabeler(fencers_rankings_dataframe,
                            level=2, mapper=category_dict)
        multiIndex_relabeler(fencers_rankings_dataframe,
                            level=3, mapper=make_season_from_year)

    # # fix up date formats
    # df['col'] = pd.to_datetime(df['col']) # converts to a datetime columns in pandas
    # df['col'] = df['col'].dt.date # converts from datetime to just the YYYY-MM-DD

    # convert to pd categories
    categorical_data = ['weapon', 'gender', 'category']
    for cat in categorical_data:
        tournaments_dataframe[cat] = tournaments_dataframe[cat].astype(
            'category')


def get_dataframes_from_tournament_url_list(list_of_urls, fencer_cap=-1, use_tournament_cache=True, use_fencer_cache=True):

    # PROCESS TOURNAMENTS FIRST
    tournaments_dict_list, bouts_dict_list, fencer_ID_list = process_tournament_data_from_urls(
        list_of_urls, use_cache=use_tournament_cache)

    bouts_dataframe = pd.DataFrame(data=bouts_dict_list, columns=BOUTS_DF_COLS)
    tournaments_dataframe = pd.DataFrame(
        data=tournaments_dict_list, columns=TOURNAMENTS_DF_COLS)

    # PROCESS INDIVIDUAL FENCER DATA

    # Takes a while if lots of fencers are not cached
    if fencer_cap == -1:
        list_to_process = fencer_ID_list
    else:
        list_to_process = random.sample(fencer_ID_list, fencer_cap)

    fencers_bio_data_list, fencers_rankings_data_list = get_fencer_data_lists_from_ID_list(
        list_to_process, use_cache=use_fencer_cache)
    

    fencers_bio_dataframe = pd.DataFrame(
        data=fencers_bio_data_list, columns=FENCERS_BIO_DF_COLS)
    fencers_rankings_dataframe = convert_list_to_dataframe_with_multi_index(
        list_of_results=fencers_rankings_data_list,
        column_names=FENCERS_RANKINGS_DF_COLS, index_names=FENCERS_RANKINGS_MULTI_INDEX)

    # CLEAN UP DATAFRAMES
    print("Cleaning up dataframes...", end="")

    cleanup_dataframes(tournaments_dataframe, bouts_dataframe,
                       fencers_bio_dataframe, fencers_rankings_dataframe)

    print(" Done!")

    return tournaments_dataframe, bouts_dataframe, fencers_bio_dataframe, fencers_rankings_dataframe


def get_results_for_division(weapon=[], gender=[], category="", max_events=-1, use_tournament_cache=True, use_fencer_cache=True):
    print("Gettting list of tournaments to process...", end="")
    search_params = get_search_params(weapon, gender, category)
    url_list = get_url_list_from_seach(search_params)
    print(" Done!")

    print("Results search found {} tournaments ".format(len(url_list)))
    if max_events == -1:
        list_to_process = url_list
    else:
        list_to_process = random.sample(url_list, max_events)
        print("  (processing {} random tournaments)".format(len(list_to_process)))

    tournament_df, bouts_df, fencer_bio_df, fencer_rank_df = get_dataframes_from_tournament_url_list(
        list_of_urls=list_to_process, use_tournament_cache=use_tournament_cache, use_fencer_cache=use_fencer_cache)
    return tournament_df, bouts_df, fencer_bio_df, fencer_rank_df
