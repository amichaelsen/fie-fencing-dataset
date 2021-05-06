import re
import requests
import json
from bs4 import BeautifulSoup
from pools.pool_scraping import get_pool_data_from_dict
from tournament_data import tournamentData

# deprecated because processing of tournament will take place entirely in this file!
# remove once done with other processing...


def get_pool_list_from_url(tournament_url):
    req = requests.get(tournament_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    # the <script id="js-competition"> tag contains the pool data
    script = next(soup.find('script', id="js-competition").children)
    # each variable window._XXXX is ';' separated and window._pools
    # contains pool data. Caution: do NOT want window._poolsMobile
    pools_string = [text.strip() for text in script.split(
        ';') if text.strip().startswith('window._pools ')][0]
    # pools_string = "window._pools = [{...dict info here...}]"
    # split to get value, then extract dictionary
    pool_list = json.loads(pools_string.split(" = ")[1])['pools']
    return pool_list


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


def process_tournament_from_url(tournament_url):
    """
    DOCSTRING TO GO HERE

        Input:

        Output:
            bout_dataframe
            fencer_dict
            tournament_info (**dict?** dataframe row?)
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
               'startDate', 'endDate', 'weapon', 'gender', 'level', 'timezone']}
    # rename keys for consistent naming
    tournament_dict['competition_id'] = tournament_dict.pop('competitionId')
    tournament_dict['start_date'] = tournament_dict.pop('startDate')
    tournament_dict['end_date'] = tournament_dict.pop('endDate')

    # create url and unique_id for tournament_dict
    tournament_dict['url'] = "https://fie.org/competitions/" + \
        str(tournament_dict['season'])+"/" + \
        str(tournament_dict['competition_id'])

    tournament_dict['unique_ID'] = str(
        tournament_dict['season'])+'-'+str(tournament_dict['competition_id'])

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

    tournament = tournamentData(
        pools_list=poolData_list,
        fencers_dict=tournament_athlete_dict,
        **tournament_dict
    )
    return tournament
