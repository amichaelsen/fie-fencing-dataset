import pandas as pd
import random
from dataframe_columns import BOUTS_DF_COLS, TOURNAMENTS_DF_COLS, FENCERS_DF_COLS
from tournaments.tournament_scraping import create_tournament_data_from_url, compile_bout_dataframe_from_tournament_data
from tournaments.tournament_data import TournamentData

list_of_urls = ['https://fie.org/competitions/2020/771',
                'https://fie.org/competitions/2021/1070',
                'https://fie.org/competitions/2021/92']

# Create dataframes to store the output data
fencers_dataframe = pd.DataFrame(columns=FENCERS_DF_COLS)
tournaments_dataframe = pd.DataFrame(columns=TOURNAMENTS_DF_COLS)
bouts_dataframe = pd.DataFrame(columns=BOUTS_DF_COLS)

fencer_ID_list = []

for tournament_url in list_of_urls:
    # process data from the event
    tournament_data = create_tournament_data_from_url(tournament_url)
    tournament_bout_dataframe = compile_bout_dataframe_from_tournament_data(
        tournament_data)
    tournament_info_dict = tournament_data.create_tournament_dict()
    tournament_fencer_ID_list = list(tournament_data.fencers_dict.keys())

    # print some info here about each tournament (# of athletes, pools, total bout count)
    print("\nTournament: {} (ID {})\n".format(
        tournament_info_dict['name'], tournament_info_dict['unique_ID']))
    print("Total Fencer Count: {}".format(len(tournament_fencer_ID_list)))
    print("Number of Bouts: {}".format(tournament_bout_dataframe.shape[1]))

    # add tournament data to overall dataframes/lists
    fencer_ID_list = list(set(fencer_ID_list+tournament_fencer_ID_list))
    bouts_dataframe = bouts_dataframe.append(tournament_bout_dataframe)
    tournaments_dataframe = tournaments_dataframe.append(
        tournament_info_dict, ignore_index=True)


def expand_weapon(wpn_str):
    weapon_dict = {'E': "Epee", "F": "Foil", "S": "Saber"}
    return weapon_dict.get(wpn_str, wpn_str)


def expand_gender(gdr_str):
    gender_dict = {"M": "Mens", "F": "Womens"}
    return gender_dict.get(gdr_str, gdr_str)


def expand_category(cat_str):
    category_dict = {"J": "Junior", "C": "Cadet",
                     "S": "Senior", "V": "Veterans"}
    return category_dict.get(cat_str, cat_str)


tournaments_dataframe['weapon'] = tournaments_dataframe['weapon'].map(
    expand_weapon)

tournaments_dataframe['gender'] = tournaments_dataframe['gender'].map(
    expand_gender)

tournaments_dataframe['category'] = tournaments_dataframe['category'].map(
    expand_category)


print(tournaments_dataframe.drop(
    columns=['timezone', 'url', 'end_date']).to_markdown())


bout_count = 10
idx = random.sample(list(bouts_dataframe.index), bout_count)
print("\nA random selection of {} bouts from list:\n".format(bout_count))
print(bouts_dataframe.loc[idx].to_markdown())
