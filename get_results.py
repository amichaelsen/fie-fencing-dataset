import pandas as pd
import random
from dataframe_columns import BOUTS_DF_COLS, TOURNAMENTS_DF_COLS, FENCERS_DF_COLS
from tournaments.tournament_scraping import create_tournament_data_from_url, compile_bout_dataframe_from_tournament_data
from tournaments.tournament_data import TournamentData
from fencers.fencer_scraping import get_fencer_info_from_ID

def get_dataframes_from_tournament_url_list(list_of_urls):
    # ---------------------------------------------------------------
    # INITIALIZE DATAFRAMES AND URLS
    # ---------------------------------------------------------------

    print("Preparing to process tournament data...", end="")
    # list_of_urls = ['https://fie.org/competitions/2020/771']#,
    # #                'https://fie.org/competitions/2021/1070']
    #                 #,'https://fie.org/competitions/2021/92']

    # Create dataframes to store the output data
    fencers_dataframe = pd.DataFrame(columns=FENCERS_DF_COLS)
    tournaments_dataframe = pd.DataFrame(columns=TOURNAMENTS_DF_COLS)
    bouts_dataframe = pd.DataFrame(columns=BOUTS_DF_COLS)

    # temporary list to store IDs before looking up fencer data
    fencer_ID_list = []
    print(" Done!")


    # ---------------------------------------------------------------
    # PROCESS TOURNAMENTS INDIVIDUALLY
    # ---------------------------------------------------------------
    print("Processing {} tournaments: ".format(len(list_of_urls)), end="")

    for idx, tournament_url in enumerate(list_of_urls):
        # process data from the event
        tournament_data = create_tournament_data_from_url(tournament_url)
        tournament_bout_dataframe = compile_bout_dataframe_from_tournament_data(
            tournament_data)
        tournament_info_dict = tournament_data.create_tournament_dict()
        tournament_fencer_ID_list = list(tournament_data.fencers_dict.keys())

        # # print some info here about each tournament (# of athletes, pools, total bout count)
        # print("\nTournament: {} (ID {})\n".format(
        #    tournament_info_dict['name'], tournament_info_dict['unique_ID']))
        # print("Total Fencer Count: {}".format(len(tournament_fencer_ID_list)))
        # print("Number of Bouts: {}".format(tournament_bout_dataframe.shape[1]))

        # add tournament data to overall dataframes/lists
        fencer_ID_list = list(set(fencer_ID_list+tournament_fencer_ID_list))
        bouts_dataframe = bouts_dataframe.append(tournament_bout_dataframe)
        tournaments_dataframe = tournaments_dataframe.append(
            tournament_info_dict, ignore_index=True)
        print("\rProcessing {} tournaments: {} tournaments done... ".format(len(list_of_urls), idx+1), end="")


    print(" Done!")
    # ---------------------------------------------------------------
    # PROCESS INDIVIDUAL FENCER DATA
    # ---------------------------------------------------------------
    ## THIS PART IS COSTLY!!

    fencer_count_cap = 5
    print("Processing {} fencers: ".format(len(fencer_ID_list[0:fencer_count_cap])), end="")

    for idx, fencer_ID in enumerate(fencer_ID_list[0:fencer_count_cap]):
        fencer_info_dict = get_fencer_info_from_ID(fencer_ID)
        fencers_dataframe = fencers_dataframe.append(fencer_info_dict, ignore_index=True)
        print("\rProcessing {} fencers: {} done... ".format(len(fencer_ID_list[0:fencer_count_cap]),idx+1), end="", flush=True)

    print(" Done!")

    # ---------------------------------------------------------------
    # CLEAN UP DATAFRAMES
    # ---------------------------------------------------------------
    print("Cleaning up dataframes...", end="")


    # expand labels for 'weapon', 'gender' and 'category' in the tournament dataframe
    weapon_dict = {'E': "Epee", "F": "Foil", "S": "Sabre"}
    gender_dict = {"M": "Mens", "F": "Womens"}
    category_dict = {"J": "Junior", "C": "Cadet",
                    "S": "Senior", "V": "Veterans"}

    tournaments_dataframe['weapon'] = tournaments_dataframe['weapon'].map(
        weapon_dict)
    tournaments_dataframe['gender'] = tournaments_dataframe['gender'].map(
        gender_dict)
    tournaments_dataframe['category'] = tournaments_dataframe['category'].map(
        category_dict)

    tournaments_dataframe['start_date'] = pd.to_datetime(
        tournaments_dataframe['start_date'])
    tournaments_dataframe['end_date'] = pd.to_datetime(
        tournaments_dataframe['end_date'])
    bouts_dataframe['date'] = pd.to_datetime(bouts_dataframe['date'])

    categorical_data = ['weapon', 'gender', 'category']
    for cat in categorical_data:
        tournaments_dataframe[cat] = tournaments_dataframe[cat].astype('category')

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
    print(bouts_dataframe.loc[idx].to_markdown())
    # print(bouts_dataframe.info())


    fencer_count = 2
    idx = random.sample(list(fencers_dataframe.index), fencer_count)
    print("\nA random selection of {} fencers from list:\n".format(fencer_count))
    print(fencers_dataframe.loc[idx].to_markdown())

    return tournaments_dataframe, bouts_dataframe, fencers_dataframe
