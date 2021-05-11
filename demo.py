import random
import time

from tournaments.tournament_scraping import create_tournament_data_from_url, compile_bout_dataframe_from_tournament_data
from tournaments.tournament_data import TournamentData
from get_results import get_dataframes_from_tournament_url_list


print("\n\n Reading and printing a single tournament")
print(     "----------------------------------------\n\n")
tournament_url = 'https://fie.org/competitions/2020/771'
print("Tournament URL for lookup: {}".format(tournament_url))
tournament = create_tournament_data_from_url(tournament_url)
print(tournament)

bout_dataframe = compile_bout_dataframe_from_tournament_data(tournament)

bout_count = 1
idx = random.sample(list(bout_dataframe.index), bout_count)
print("A random bout from the tournament:\n".format(bout_count))
print(bout_dataframe.loc[idx].drop(columns=['opp_age','opp_curr_pts','date']).to_markdown())

time.sleep(5)


print("\n\n Loading a list of tournaments, compiling bouts and fencer info")
print(     "----------------------------------------------------------------\n\n")

list_of_urls = ['https://fie.org/competitions/2021/1081']
tourn_df, bout_df, fencers_bio_df, fencers_rankings_df = get_dataframes_from_tournament_url_list(list_of_urls)


print("\n\n")
time.sleep(2)

 # Print dataframes (or parts of them) to see output

print(tourn_df.drop(
    columns=['timezone', 'url', 'end_date']).to_markdown())
# print(tourn_df.info())

bout_count = 5
idx = random.sample(list(bout_df.index), bout_count)
print("\nA random selection of {} bouts from list:\n".format(bout_count))
print(bout_df.loc[idx].drop(
    columns=['opp_age', 'opp_curr_pts']).to_markdown())
# print(bout_df.info())

fencer_count = 5
idx = random.sample(list(fencers_bio_df.index), fencer_count)
print("\nA random selection of {} fencers from bio list:\n".format(fencer_count))
print(fencers_bio_df.loc[idx].to_markdown())

fencer_count = 2
idx = random.sample(
    list(fencers_rankings_df.index.get_level_values(0)), fencer_count)
print("\nA random selection of {} fencers from rankings list:\n".format(fencer_count))
print(fencers_rankings_df.loc[idx])

