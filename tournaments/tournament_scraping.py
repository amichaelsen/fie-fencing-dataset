import re
import requests
import json
from bs4 import BeautifulSoup
from pools.pool_scraping import get_pool_data_from_dict
from tournaments.tournament_data import TournamentData
import pandas as pd
from dataframe_columns import BOUTS_DF_COLS

## =--------------------------------------=
## Helper Methods Methods for Tournament Scraping
## =--------------------------------------=


def get_pool_list_from_json_list(var_list):
    # get window._pools Data
    # -------------------------
    # CAUTION: do NOT want window._poolsMobile
    pools_var_name = "window._pools "
    # pools_string = "window._pools = [{"pools": ...dict info here...}]"
    pools_string = [text.strip() for text in var_list if
                    text.strip().startswith(pools_var_name)][0]
    # type(pools_list) = list of dict
    pools_list = json.loads(pools_string.split(" = ")[1])['pools']
    return pools_list


def get_comp_dict_from_json_list(var_list):
    # get window._competition Data
    # -------------------------
    comp_var_name = "window._competition "
    # comp_string = "window._competition = { "id": 4874, "competitionId": 771,... }"
    comp_string = [text.strip() for text in var_list if
                   text.strip().startswith(comp_var_name)][0]
    comp = json.loads(comp_string.split(" = ")[1])  # type(comp) = dict
    return comp


def get_athletes_list_from_json_list(var_list):
    # get window._athletes Data
    # -------------------------
    athl_var_name = "window._athletes "
    # athl_string = "window._athletes = [
    #   { "overallRanking": 59, "overallPoints": 27,
    #     "rank": 1, "points": 32,
    #     "fencer": { "id": 33614, "name": "BERTHIER Amita",
    #                 "country": "SINGAPORE", "date": "2000-12-15",
    #                 "flag": "SG", "countryCode": "SGP", "age": 20
    #               }
    #   }, ... ]"
    athl_string = [text.strip() for text in var_list if
                   text.strip().startswith(athl_var_name)][0]
    # type(athletes_list) = list of dicts
    athletes_list = json.loads(athl_string.split(" = ")[1])
    return athletes_list

## =--------------------------------------=
## Main Methods for Tournament Scraping
## =--------------------------------------=

## Entry point for get_results
# TODO: split into more helper functions 
def create_tournament_data_from_url(tournament_url):
    """
    Takes a tournament URL and returns a TournamentData dataclass with desired information

        Input:
            tournament_url : str
                String representation of tournament url, e.g. 'https://fie.org/competitions/2020/771'

        Output:
            tournament : TournamentData 
                A TournamentData object (see tournament_data.py) which contains general tournament 
                information along with a list of poolData objects (see pool_data.py) and a dictionary
                with tournament specific athlete information indexed by 'id' 
    """
    # 1. EXTRACT TOURNAMENT VARIABLES/RAW DATA
    # -----------------------------------------
    req = requests.get(tournament_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    script = next(soup.find('script', id="js-competition").children)
    # each variable window._XXXX is ';' separated and window._pools contains pool data.
    var_list = script.split(';')

    pools_list = get_pool_list_from_json_list(var_list)
    comp = get_comp_dict_from_json_list(var_list)
    athlete_dict_list = get_athletes_list_from_json_list(var_list)

    # 2. PROCESS POOL DICTS INTO POOL DATA & FENCER LIST
    # -----------------------------------------
    poolData_list = []
    for pool_dict in pools_list:
        pool_data = get_pool_data_from_dict(pool_dict)
        poolData_list.append(pool_data)

    # 3. PROCESS TOURNAMENT INFO INTO DICT
    # -----------------------------------------
    tournament_dict = {k: v for k, v in comp.items(
    ) if k in ['competitionId', 'season', 'name', 'category', 'country',
               'startDate', 'endDate', 'weapon', 'gender', 'timezone']}
    # rename keys for consistent naming
    tournament_dict['competition_ID'] = tournament_dict.pop('competitionId')
    tournament_dict['start_date'] = tournament_dict.pop('startDate')
    tournament_dict['end_date'] = tournament_dict.pop('endDate')

    # create url and unique_id for tournament_dict
    tournament_dict['url'] = "https://fie.org/competitions/" + \
        str(tournament_dict['season'])+"/" + \
        str(tournament_dict['competition_ID'])

    tournament_dict['unique_ID'] = str(
        tournament_dict['season'])+'-'+str(tournament_dict['competition_ID'])

    # 4. PROCESS FENCERS INTO A DICT
    # -----------------------------------------
    tournament_athlete_dict = {}
    for athlete_dict in athlete_dict_list:
        if athlete_dict['overallPoints']:
            points = athlete_dict['overallPoints']
        else:
            points = 0
        id = athlete_dict['fencer']['id']
        age = athlete_dict['fencer']['age']
        tournament_athlete_dict[id] = {
            "age": age, "points_before_event": points}

    tournament = TournamentData(
        pools_list=poolData_list,
        fencers_dict=tournament_athlete_dict,
        **tournament_dict
    )
    return tournament


## Entry point for get_results
#TODO: remove dataframe.append for each row, use list instead! 
def compile_bout_dataframe_from_tournament_data(tournament_data):
    """
    Takes a TournamentData Object and returns a pandas Dataframe of bouts 
    """
    bout_dataframe = pd.DataFrame(columns=BOUTS_DF_COLS)

    tournament_ID = tournament_data.unique_ID

    for pool in tournament_data.pools_list:
        pool_ID = pool.pool_ID
        date = tournament_data.start_date
        for i in range(0, pool.pool_size):
            fencer_ID = pool.fencer_IDs[i]
            fencer_age = tournament_data.fencers_dict[fencer_ID]['age']
            fencer_curr_points = tournament_data.fencers_dict[fencer_ID]['points_before_event']
            for j in range(i+1, pool.pool_size):
                # gather bout data
                opponent_ID = pool.fencer_IDs[j]
                opponent_age = tournament_data.fencers_dict[opponent_ID]['age']
                opponent_curr_points = tournament_data.fencers_dict[opponent_ID]['points_before_event']
                fencer_score = pool.scores[i][j]
                opponent_score = pool.scores[j][i]
                winner_ID = fencer_ID if pool.winners[i][j] == 1 else opponent_ID
                upset = True if ((opponent_curr_points > fencer_curr_points) and winner_ID == fencer_ID or (
                    opponent_curr_points < fencer_curr_points) and winner_ID == opponent_ID) else False

                # add bout entry as row in dataframe
                bout_dataframe = bout_dataframe.append({'fencer_ID': fencer_ID, 'opp_ID': opponent_ID,
                                                        'fencer_age': fencer_age, 'opp_age': opponent_age,
                                                        'fencer_score': fencer_score, 'opp_score': opponent_score, 'winner_ID': winner_ID,
                                                        'fencer_curr_pts': fencer_curr_points, 'opp_curr_pts': opponent_curr_points,
                                                        'tournament_ID': tournament_ID, 'pool_ID': pool_ID, 'upset': upset, 'date': date}, ignore_index=True)
    return bout_dataframe
