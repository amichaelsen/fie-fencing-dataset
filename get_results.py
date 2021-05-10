import pandas as pd
import random

from dataframe_columns import BOUTS_DF_COLS, TOURNAMENTS_DF_COLS, FENCERS_BIO_DF_COLS, FENCERS_RANKINGS_DF_COLS, FENCERS_RANKINGS_MULTI_INDEX
from dataframe_columns import multiIndex_relabeler, make_season_from_year
from tournaments.tournament_scraping import create_tournament_data_from_url, compile_bout_dataframe_from_tournament_data
from tournaments.tournament_data import TournamentData
from fencers.fencer_scraping import get_fencer_dataframes_from_ID_list, convert_list_to_dataframe_with_multi_index


def process_tournament_data_from_urls(list_of_urls):
    # tournaments_list = [] # TODO implement list -> dataframe
    # bouts_list = [] # TODO implement list -> dataframe
    tournaments_dataframe = pd.DataFrame(columns=TOURNAMENTS_DF_COLS)
    bouts_dataframe = pd.DataFrame(columns=BOUTS_DF_COLS)

    fencer_ID_list = []
    for idx, tournament_url in enumerate(list_of_urls):
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
        print("\rProcessing {} tournaments: {} tournaments done... ".format(
            len(list_of_urls), idx+1), end="")

    return tournaments_dataframe, bouts_dataframe, fencer_ID_list


def cleanup_dataframes(tournaments_dataframe, bouts_dataframe,
                       fencers_bio_dataframe, fencers_rankings_dataframe):
    # expand labels for 'weapon', 'gender' and 'category' in the tournament dataframe
    weapon_dict = {'E': "Epee", "F": "Foil", "S": "Sabre"}
    gender_dict = {"M": "Mens", "F": "Womens"}
    category_dict = {"J": "Junior", "C": "Cadet",
                     "S": "Senior", "V": "Veterans"}

    # relabel keys to full words
    tournaments_dataframe['weapon'] = tournaments_dataframe['weapon'].map(
        weapon_dict)
    tournaments_dataframe['gender'] = tournaments_dataframe['gender'].map(
        gender_dict)
    tournaments_dataframe['category'] = tournaments_dataframe['category'].map(
        category_dict)

    multiIndex_relabeler(fencers_rankings_dataframe,
                         level=1, mapper=weapon_dict)
    multiIndex_relabeler(fencers_rankings_dataframe,
                         level=2, mapper=category_dict)
    multiIndex_relabeler(fencers_rankings_dataframe,
                         level=3, mapper=make_season_from_year)

    # fix up date formats
    tournaments_dataframe['start_date'] = pd.to_datetime(
        tournaments_dataframe['start_date']).dt.date
    tournaments_dataframe['end_date'] = pd.to_datetime(
        tournaments_dataframe['end_date']).dt.date
    bouts_dataframe['date'] = pd.to_datetime(bouts_dataframe['date']).dt.date

    fencers_bio_dataframe['date_accessed'] = pd.to_datetime(
        fencers_bio_dataframe['date_accessed']).dt.date

    # convert to pd categories
    categorical_data = ['weapon', 'gender', 'category']
    for cat in categorical_data:
        tournaments_dataframe[cat] = tournaments_dataframe[cat].astype(
            'category')


def get_dataframes_from_tournament_url_list(list_of_urls, fencer_cap=-1):
    print("Preparing to process tournament data...", end="")

    # PROCESS TOURNAMENTS INDIVIDUALLY
    print("Processing {} tournaments: ".format(len(list_of_urls)), end="")

    tournaments_dataframe, bouts_dataframe, fencer_ID_list = process_tournament_data_from_urls(
        list_of_urls)

    print(" Done!")

    # PROCESS INDIVIDUAL FENCER DATA

    # Takes a while if lots of fencers are not cached
    if fencer_cap == -1:
        list_to_process = fencer_ID_list
    else:
        list_to_process = fencer_ID_list[0:fencer_cap]

    fencers_bio_dataframe, fencers_rankings_dataframe = get_fencer_dataframes_from_ID_list(
        list_to_process)

    print(" Done!")

    # CLEAN UP DATAFRAMES
    print("Cleaning up dataframes...", end="")

    cleanup_dataframes(tournaments_dataframe, bouts_dataframe,
                       fencers_bio_dataframe, fencers_rankings_dataframe)
    print("Done!")
    # ---------------------------------------------------------------
    # PRINT OUTPUTS TO VERIFY DATA
    # ---------------------------------------------------------------

    # Print dataframes (or parts of them) to see output

    print(tournaments_dataframe.drop(
        columns=['timezone', 'url', 'end_date']).to_markdown())
    # print(tournaments_dataframe.info())

    bout_count = 3
    idx = random.sample(list(bouts_dataframe.index), bout_count)
    print("\nA random selection of {} bouts from list:\n".format(bout_count))
    print(bouts_dataframe.loc[idx].drop(
        columns=['opp_age', 'opp_curr_pts', 'date']).to_markdown())
    # print(bouts_dataframe.info())

    fencer_count = 2
    idx = random.sample(list(fencers_bio_dataframe.index), fencer_count)
    print("\nA random selection of {} fencers from list:\n".format(fencer_count))
    print(fencers_bio_dataframe.loc[idx].to_markdown())

    fencer_count = 2
    idx = random.sample(
        list(fencers_rankings_dataframe.index.get_level_values(0)), fencer_count)
    print("\nA random selection of {} fencers from rankings list:\n".format(fencer_count))
    print(fencers_rankings_dataframe.loc[idx])

    return tournaments_dataframe, bouts_dataframe, fencers_bio_dataframe, fencers_rankings_dataframe
