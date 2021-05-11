import pandas as pd
import random
from progress.bar import Bar
import requests
import math

from dataframe_columns import BOUTS_DF_COLS, TOURNAMENTS_DF_COLS, FENCERS_BIO_DF_COLS, FENCERS_RANKINGS_DF_COLS, FENCERS_RANKINGS_MULTI_INDEX
from dataframe_columns import multiIndex_relabeler, make_season_from_year
from tournaments.tournament_scraping import create_tournament_data_from_url, compile_bout_dataframe_from_tournament_data
from tournaments.tournament_data import TournamentData
from fencers.fencer_scraping import get_fencer_dataframes_from_ID_list, convert_list_to_dataframe_with_multi_index


def add_tournament_urls_to_list(url_list, tournament_dict_list):
    for tournament in tournament_dict_list:
        url = "https://fie.org/"+str(tournament['season'])+"/"+str(tournament['competitionId'])
        print('Event URL: \'{}\''.format(url))
        url_list.append(url) 
    return url_list


def get_url_list_from_seach(search_params):
    url_list = []

    # get first page of results and check if more pages needed 
    search_params['fetchPage'] = 1
    search_url = 'https://fie.org/competitions/search'
    req = requests.post(search_url, data=search_params)
    json = req.json()
    print("Total Events Found: {}".format(json['totalFound']))
    # json object sample in initial_testing/request_response.json
    pages_needed = math.ceil(json['totalFound']/json['pageSize'])
    url_list = add_tournament_urls_to_list(url_list, json['items'])
    for p in range(2,pages_needed+1):
        search_params['fetchPage'] = p
        req = requests.post(search_url, data=search_params)
        json = req.json()
        url_list = add_tournament_urls_to_list(url_list, json['items'])

    return url_list




def process_tournament_data_from_urls(list_of_urls):
    # tournaments_list = [] # TODO implement list -> dataframe
    # bouts_list = [] # TODO implement list -> dataframe
    tournaments_dataframe = pd.DataFrame(columns=TOURNAMENTS_DF_COLS)
    bouts_dataframe = pd.DataFrame(columns=BOUTS_DF_COLS)

    fencer_ID_list = []

    print("Processing {} tournaments: ".format(len(list_of_urls)), end="")

    for tournament_url in Bar('Loading Tournaments').iter(list_of_urls):
        # process data from the event
        tournament_data = create_tournament_data_from_url(tournament_url)
        tournament_bout_dataframe = compile_bout_dataframe_from_tournament_data(
            tournament_data)
        tournament_info_dict = tournament_data.create_tournament_dict()
        tournament_fencer_ID_list = list(tournament_data.fencers_dict.keys())

        # add tournament data to overall dataframes/lists
        fencer_ID_list = list(set(fencer_ID_list+tournament_fencer_ID_list))
        bouts_dataframe = bouts_dataframe.append(tournament_bout_dataframe)
        tournaments_dataframe = tournaments_dataframe.append(
            tournament_info_dict, ignore_index=True)
        # print("\rProcessing {} tournaments: {} tournaments done... ".format(
        #     len(list_of_urls), idx+1), end="")

    return tournaments_dataframe, bouts_dataframe, fencer_ID_list


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


def get_dataframes_from_tournament_url_list(list_of_urls, fencer_cap=-1):
    print("Preparing to process tournament data...\n", end="")

    # PROCESS TOURNAMENTS INDIVIDUALLY

    tournaments_dataframe, bouts_dataframe, fencer_ID_list = process_tournament_data_from_urls(
        list_of_urls)

    # PROCESS INDIVIDUAL FENCER DATA

    # Takes a while if lots of fencers are not cached
    if fencer_cap == -1:
        list_to_process = fencer_ID_list
    else:
        list_to_process = fencer_ID_list[0:fencer_cap]

    fencers_bio_dataframe, fencers_rankings_dataframe = get_fencer_dataframes_from_ID_list(
        list_to_process)

    # CLEAN UP DATAFRAMES
    print("Cleaning up dataframes...", end="")

    cleanup_dataframes(tournaments_dataframe, bouts_dataframe,
                       fencers_bio_dataframe, fencers_rankings_dataframe)

    print(" Done!")

    return tournaments_dataframe, bouts_dataframe, fencers_bio_dataframe, fencers_rankings_dataframe
