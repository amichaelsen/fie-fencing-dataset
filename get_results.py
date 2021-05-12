import pandas as pd
import random
from progress.bar import Bar
import requests
import math
import json
from os import path, stat

from dataframe_columns import BOUTS_DF_COLS, TOURNAMENTS_DF_COLS, FENCERS_BIO_DF_COLS, FENCERS_RANKINGS_DF_COLS, FENCERS_RANKINGS_MULTI_INDEX
from dataframe_columns import multiIndex_relabeler, make_season_from_year
from tournaments.tournament_scraping import create_tournament_data_from_url, compile_bout_dict_list_from_tournament_data, process_tournament_data_from_urls
from tournaments.tournament_data import TournamentData
from fencers.fencer_scraping import get_fencer_data_lists_from_ID_list
from dataframe_columns import convert_list_to_dataframe_with_multi_index
from soup_scraping import get_search_params
from caching_methods import save_dict_to_cache

CACHE_FILENAME = 'tournaments/tournament_cache.txt'


def add_tournament_urls_to_list(url_list, tournament_dict_list):
    """
    Method for constructing a list of urls from a list of tournament_dict data

        Input:
        ------
        url_list : list
            Initial list of tournament urls represented as strings. 
            Urls will have the form: https://fie.org/competitions/2020/1080
        tournament_dict_list : list
            List of tournaments stored in dicts (from GET 'https://fie.org/competitions/search')
            with keys 'season' and 'competitionId' used to construct url

        Output:
        -------
        url_list : list
            Final list of tournament urls represented as strings. 
            Urls will have the form: https://fie.org/competitions/2020/1080
    """
    for tournament in tournament_dict_list:
        url = "https://fie.org/competitions/" + \
            str(tournament['season'])+"/"+str(tournament['competitionId'])
        url_list.append(url)
    return url_list


def get_url_list_from_seach(search_params):
    """
    Given dictionary of search parameters returns list of tournament urls in the search

        Input:
        ------
        search_params : dict 
            Search parameters modeled off 'Request Payload' from 'search' network call
            made by https://fie.org/competitions when results search parameters changed.
            Ex: { "name": "", "status": "passed", "gender": ['f'], "weapon": ['e'],
                "type": ["i"], "season": "-1", "level": 'c', "competitionCategory": "",
                "fromDate": "", "toDate": "", "fetchPage": 1 }
            Note: "season": '-1' returns *all* seasons

        Output:
        ------
        url_list : list
            List of tournament urls represented as strings. 
            Urls will have the form: https://fie.org/competitions/2020/1080
    """
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


def cleanup_dataframes(tournaments_dataframe, bouts_dataframe,
                       fencers_bio_dataframe, fencers_rankings_dataframe):
    """
    Performs relabeling/typecasting of tournament, bout, fencer_bio, and fencer_ranking pd.DataFrames

        Notes: 
            * No returns, makes changes to the dataframes in place
            * Currently no changes made to bouts_dataframe
    """
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


def get_dataframes_from_tournament_url_list(list_of_urls, use_tournament_cache=True, use_fencer_cache=True):
    """
    Given list of tournament urls (+ cache flags), returns dataframes of compiled data

        Input:
        ------
        list_of_urls : list
            List of tournament urls represented as strings. 
            Urls will have the form: https://fie.org/competitions/2020/1080

        use_tournament_cache : boolean
        use_fencer_cache : boolean

        Output:
        ------
        tournaments_dataframe : pandas.DataFrame 
            Dataframe with data about each tournament, with columns listed and described
            in dataframe_columns.py as TOURNAMENTS_DF_COLS
        bouts_dataframe  : pandas.DataFrame  
            Dataframe with data about each bout, with columns listed and described
            in dataframe_columns.py as BOUTS_DF_COLS
        fencers_bio_dataframe  : pandas.DataFrame  
            Dataframe with biographical data about each fencer, with columns listed 
            and described in dataframe_columns.py as FENCERS_BIO_DF_COLS
        fencers_rankings_dataframe : pandas.DataFrame 
            Dataframe with historical rankings data for each fencer, with columns listed 
            and described in dataframe_columns.py as FENCERS_RANKINGS_DF_COLS
            and pd.multiIndex created from FENCERS_RANKINGS_MULTI_INDEX 
            (see `convert_list_to_dataframe_with_multi_index` in dataframe_columns.py)
    """
    # PROCESS TOURNAMENTS FIRST
    tournaments_dict_list, bouts_dict_list, fencer_ID_list = process_tournament_data_from_urls(
        list_of_urls, use_cache=use_tournament_cache)

    bouts_dataframe = pd.DataFrame(data=bouts_dict_list, columns=BOUTS_DF_COLS)
    tournaments_dataframe = pd.DataFrame(
        data=tournaments_dict_list, columns=TOURNAMENTS_DF_COLS)

    # PROCESS INDIVIDUAL FENCER DATA

    fencers_bio_data_list, fencers_rankings_data_list = get_fencer_data_lists_from_ID_list(
        fencer_ID_list=fencer_ID_list, use_cache=use_fencer_cache)

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
    """
    Given division parameters returns dataframes with data for results 

        Input:
        ------
        weapon : list
            List of weapons to include in results search
            'e' = Epee, 'f' = Foil, 's' = Sabre
        gender : list
            List of genders to include in results search
                'f' = Female/Women's, 'm' = Male/Men's
        category : str
            Category (i.e. age group) to search
            'c' = Cadet, 'j' = Junior, 's' = Senior, 'v' = Veteran

        max_events : int
            Optional parameter to cap the number of tournaments to process

        use_tournament_cache : boolean
        use_fencer_cache : boolean

        Output:
        ______
        tournaments_dataframe : pandas.DataFrame 
            Dataframe with data about each tournament, with columns listed and described
            in dataframe_columns.py as TOURNAMENTS_DF_COLS
        bouts_dataframe  : pandas.DataFrame  
            Dataframe with data about each bout, with columns listed and described
            in dataframe_columns.py as BOUTS_DF_COLS
        fencers_bio_dataframe  : pandas.DataFrame  
            Dataframe with biographical data about each fencer, with columns listed 
            and described in dataframe_columns.py as FENCERS_BIO_DF_COLS
        fencers_rankings_dataframe : pandas.DataFrame 
            Dataframe with historical rankings data for each fencer, with columns listed 
            and described in dataframe_columns.py as FENCERS_RANKINGS_DF_COLS
            and pd.multiIndex created from FENCERS_RANKINGS_MULTI_INDEX 
            (see `convert_list_to_dataframe_with_multi_index` in dataframe_columns.py)
    """
    print("Gettting list of tournaments to process...", end="")
    search_params = get_search_params(weapon, gender, category)
    url_list = get_url_list_from_seach(search_params)
    print(" Done!")

    print("Results search found {} tournaments ".format(len(url_list)))
    if max_events == -1 or max_events > len(url_list):
        list_to_process = url_list
    else:
        list_to_process = random.sample(url_list, max_events)
        print("  (processing {} random tournaments)".format(len(list_to_process)))

    tournament_df, bouts_df, fencer_bio_df, fencer_rank_df = get_dataframes_from_tournament_url_list(
        list_of_urls=list_to_process, use_tournament_cache=use_tournament_cache, use_fencer_cache=use_fencer_cache)

    return tournament_df, bouts_df, fencer_bio_df, fencer_rank_df
