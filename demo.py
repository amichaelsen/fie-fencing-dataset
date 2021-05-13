import random
import time
import pandas as pd

from tournaments.tournament_scraping import create_tournament_data_from_url, compile_bout_dict_list_from_tournament_data
from tournaments.tournament_data import TournamentData
from helper.get_results import get_dataframes_from_tournament_url_list
from helper.get_results import get_url_list_from_seach
from helper.get_results import get_results_for_division
from helper.soup_scraping import get_search_params
from helper.dataframe_columns import BOUTS_DF_COLS

testing_single_tournament = False
testing_list_tournaments = False
testing_results_search = False
test_results_by_division = True

if testing_single_tournament:
    print("\n\n Reading and printing a single tournament")
    print("----------------------------------------\n\n")
    tournament_url = 'https://fie.org/competitions/2020/771'
    # tournament_url = 'https://fie.org/competitions/2016/941'
    print("Tournament URL for lookup: {}".format(tournament_url))
    has_data, tournament = create_tournament_data_from_url(tournament_url)
    print(tournament)

    bout_dict_list = compile_bout_dict_list_from_tournament_data(tournament)
    bout_dataframe = pd.DataFrame(data=bout_dict_list, columns=BOUTS_DF_COLS)

    bout_count = 10
    idx = random.sample(list(bout_dataframe.index), bout_count)
    print("A random selection of bouts from the tournament:\n".format(bout_count))
    print(bout_dataframe.loc[idx].drop(
        columns=['opp_age', 'opp_curr_pts']).to_markdown())

    time.sleep(5)

if testing_list_tournaments:
    print("\n\n Loading a list of tournaments, compiling bouts and fencer info")
    print("----------------------------------------------------------------\n\n")

    list_of_urls = ['https://fie.org/competitions/2021/1081',
                    'https://fie.org/competitions/2021/121']
    # list_of_urls = ['https://fie.org/competitions/2016/941']
    # list_of_urls = ['https://fie.org/competitions/2016/63']
    tourn_df, bout_df, fencers_bio_df, fencers_rankings_df = get_dataframes_from_tournament_url_list(
        list_of_urls=list_of_urls, use_fencer_data_cache=True, use_fencer_req_cache=True)

    print("\n\n")
    time.sleep(2)

    # Print dataframes (or parts of them) to see output

    print(tourn_df.drop(
        columns=['timezone', 'url', 'end_date']).to_markdown())
    # print(tourn_df.info())

    bout_count = 25
    if(len(list(bout_df.index)) > bout_count):
        idx = random.sample(list(bout_df.index), bout_count)
        print("\nA random selection of bouts from list:\n".format(bout_count))
        print(bout_df.loc[idx].drop(
            columns=['opp_age', 'opp_curr_pts']).to_markdown())
    else:
        print(bout_df.drop(
            columns=['opp_age', 'opp_curr_pts']).to_markdown())

    fencer_count = 5
    idx = random.sample(list(fencers_bio_df.index), fencer_count)
    print("\nA random selection of {} fencers from bio list:\n".format(fencer_count))
    print(fencers_bio_df.loc[idx].to_markdown())

    fencer_count = 2
    idx = random.sample(
        list(fencers_rankings_df.index.get_level_values(0)), fencer_count)
    print("\nA random selection of {} fencers from rankings list:\n".format(fencer_count))
    print(fencers_rankings_df.loc[idx])

if testing_results_search:

    print("\n\n Loading a list of tournaments url")
    print("----------------------------------\n\n")
    print("\n\nGetting results for Women's Foil...\n")

    # search_params = get_search_params(weapon=['f'],gender=['f'])
    # get_url_list_from_seach(search_params)

    print("\n\nGetting results for Cadet Women's Sabre...\n")

    search_params = get_search_params(weapon=['s'], gender=['f'], category='c')
    url_list = get_url_list_from_seach(search_params)

    print(len(url_list))
    print(url_list[0:100])

if test_results_by_division:
    print("\n\n Loading all results + fencer data for a division")
    print("----------------------------------------------------------------\n\n")



    weapon = 'f'
    gender = 'm'
    category = ''


    weapon_dict = {'f': "foil", 'e': 'epee', 's': 'sabre'}
    gender_dict = {'f': "womens", 'm': 'mens'}
    category_dict = {'c': 'cadet', 'j': 'junior', 's':'senior', 'v':'veteran', '':'all'}

    div_name = category_dict[category] + "_" + gender_dict[gender] + "_" + weapon_dict[weapon]

    print("Getting results for {} ...\n".format(div_name))


    tourn_df, bout_df, fencers_bio_df, fencers_rankings_df = get_results_for_division(
        weapon=[weapon], gender=[gender], category=category, max_events=10, 
        use_tournament_cache=True, use_fencer_data_cache=True, use_fencer_req_cache=True)

    print("\n\n")
    time.sleep(2)

    # Print dataframes (or parts of them) to see output

    tournament_count = 25
    if(len(list(tourn_df.index)) > tournament_count):
        idx = random.sample(list(tourn_df.index), tournament_count)
        print(tourn_df.loc[idx].drop(
            columns=['timezone', 'url', 'end_date']).to_markdown())
    else:
        print(tourn_df.drop(
            columns=['timezone', 'url', 'end_date']).to_markdown())
    # print(tourn_df.info())

    bout_count = 25
    if(len(list(bout_df.index)) > bout_count):
        idx = random.sample(list(bout_df.index), bout_count)
        print("\nA random selection of bouts from list:\n".format(bout_count))
        print(bout_df.loc[idx].drop(
            columns=['opp_age', 'opp_curr_pts']).to_markdown())
    else:
        print(bout_df.drop(
            columns=['opp_age', 'opp_curr_pts']).to_markdown())
    # print(bout_df.info())

    fencer_count = 50
    if(len(list(fencers_bio_df.index)) > fencer_count):
        idx = random.sample(list(fencers_bio_df.index), fencer_count)
        print("\nA random selection of {} fencers from bio list: (idx = {})\n".format(
            fencer_count, idx))
        print(fencers_bio_df.loc[idx].to_markdown())
    else:
        print(fencers_bio_df.to_markdown())

    fencer_count = 5
    if(len(list(set(fencers_rankings_df.index.get_level_values(0)))) > fencer_count):
        idx = random.sample(
            list(set(fencers_rankings_df.index.get_level_values(0))), fencer_count)
        print("\nA random selection of {} fencers from rankings list: (idx = {})\n".format(
            fencer_count, idx))
        print(fencers_rankings_df.loc[idx])
    else:
        print(fencers_rankings_df)
