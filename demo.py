import random
from tournaments.tournament_scraping import create_tournament_data_from_url, compile_bout_dataframe_from_tournament_data
from tournaments.tournament_data import TournamentData
from get_results import get_dataframes_from_tournament_url_list


print("\n\n Reading and printing a single tournament\n\n")
tournament_url = 'https://fie.org/competitions/2020/771'
print("Tournament URL for lookup: {}".format(tournament_url))
tournament = create_tournament_data_from_url(tournament_url)
print(tournament)

bout_dataframe = compile_bout_dataframe_from_tournament_data(tournament)

bout_count = 1
idx = random.sample(list(bout_dataframe.index), bout_count)
print("A random bout from the tournament:\n".format(bout_count))
print(bout_dataframe.loc[idx].drop(columns=['opp_age','opp_curr_pts','date']).to_markdown())




print("\n\n Loading a list of tournaments, compiling bouts and fencer info\n\n")
list_of_urls = ['https://fie.org/competitions/2021/1081']
tourn_df, bout_df, fencers_bio_df, fencers_rankings_df = get_dataframes_from_tournament_url_list(list_of_urls)


print("\n\nPRINTING RESUTS FROM get_dataframes_from_tournament_url_list:\n\n")
print("---"*40+'\n\n')

print(tourn_df.to_markdown())
print("\n"*2)

print(bout_df.to_markdown())
print("\n"*2)


print(fencers_bio_df.to_markdown())
print("\n"*2)


print(fencers_rankings_df)
print("\n"*2)

print(fencers_rankings_df.index.get_level_values(1))
print("\n"*2)
