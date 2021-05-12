import re
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd


from dataframe_columns import BOUTS_DF_COLS
from pools.pool_scraping import get_pool_data_from_dict
from tournaments.tournament_data import TournamentData
from soup_scraping import get_json_var_from_script


# =--------------------------------------=
# Helper Methods Methods for Tournament Scraping
# =--------------------------------------=


def create_tournament_dict_from_comp(comp):
    # comp = { "id": 4874, "competitionId": 771,... }"
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

    return tournament_dict


def create_tournament_athlete_dict_from_athlete_list(athlete_dict_list):
    """
    Takes the original page list of athlete dicts and extracts info

        Input:
        ------
        athlete_dict_list : list (of dicts)
        [  { "overallRanking": 59, "overallPoints": 27, "rank": 1, "points": 32,
           "fencer": { "id": 33614, "name": "BERTHIER Amita", "country": "SINGAPORE",
                       "date": "2000-12-15", "flag": "SG", "countryCode": "SGP", "age": 20
                      }
           }, ... ]
        Output:
        ------
        tournament_athlete_dict : dict
            {id1 : {"age" : int, "points_before_event": float}, id2 : ...}
    """
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

    return tournament_athlete_dict


# =--------------------------------------=
# Main Methods for Tournament Scraping
# =--------------------------------------=

# Entry point for get_results


def create_tournament_data_from_url(tournament_url, use_cache=True):
    """
    Takes a tournament URL and returns a TournamentData dataclass with desired information

        Input:
            tournament_url : str
                String representation of tournament url, e.g. 'https://fie.org/competitions/2020/771'

        Output:
            has_results_data : bool
                Indicates whether the tournament has results data. 
                False may indicate missing fencer IDs or no results/pool results.
            tournament : TournamentData
                A TournamentData object (see tournament_data.py) which contains general tournament
                information along with a list of poolData objects if it exists (see pool_data.py)
                and a dict with tournament specific athlete information indexed by 'id', if it exists
    """
    req = requests.get(tournament_url)
    soup = BeautifulSoup(req.content, 'html.parser')

    # each get json variables of the form window._XXXX
    pools_list = get_json_var_from_script(
        soup=soup, script_id="js-competition", var_name="window._pools ")['pools']
    comp = get_json_var_from_script(
        soup=soup, script_id="js-competition", var_name="window._competition ")
    athlete_dict_list = get_json_var_from_script(
        soup=soup, script_id="js-competition", var_name="window._athletes ")

    # PROCESS POOL DICTS INTO POOL DATA & FENCER LIST
    poolData_list = []
    for pool_dict in pools_list:
        pool_data = get_pool_data_from_dict(pool_dict)
        poolData_list.append(pool_data)

    # PROCESS TOURNAMENT & ATHLETE INFO INTO DICTS
    tournament_dict = create_tournament_dict_from_comp(comp)
    tournament_athlete_dict = create_tournament_athlete_dict_from_athlete_list(
        athlete_dict_list)

    # IF NO POOLS DATA STORED OR FENCER IDS MISSING (usually from all athletes) SKIP
    #    (return NoneType, handled in get_results.process_tournament_data_from_urls)
    if len(pools_list) == 0:
        return False, TournamentData(pools_list=[],
                                     fencers_dict={},
                                     missing_results_flag="no pools data",
                                     ** tournament_dict)
    elif 0 in list(tournament_athlete_dict.keys()):
        return False, TournamentData(pools_list=[],
                                     fencers_dict={},
                                     missing_results_flag="fencer IDs missing",
                                     ** tournament_dict)
    else:
        has_results_data = True

    # CREATE TOURNAMENT DATACLASS TO RETURN
    tournament = TournamentData(
        pools_list=poolData_list,
        fencers_dict=tournament_athlete_dict,
        **tournament_dict
    )
    return has_results_data, tournament


# Entry point for get_results
# TODO: remove dataframe.append for each row, use list instead!
def compile_bout_dict_list_from_tournament_data(tournament_data):
    """
    Takes a TournamentData Object and returns a pandas Dataframe of bouts
    """
    bout_list = []
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
                bout_list.append({'fencer_ID': fencer_ID, 'opp_ID': opponent_ID,
                                  'fencer_age': fencer_age, 'opp_age': opponent_age,
                                  'fencer_score': fencer_score, 'opp_score': opponent_score, 'winner_ID': winner_ID,
                                  'fencer_curr_pts': fencer_curr_points, 'opp_curr_pts': opponent_curr_points,
                                  'tournament_ID': tournament_ID, 'pool_ID': pool_ID, 'upset': upset, 'date': date})
    return bout_list
