import random
from tournaments.tournament_scraping import create_tournament_data_from_url, compile_bout_dataframe_from_tournament_data
from tournaments.tournament_data import TournamentData

list_of_urls = ['https://fie.org/competitions/2020/771']




for tournament_url in list_of_urls:
    print("Tournament URL for lookup: {}".format(tournament_url))
    tournament = create_tournament_data_from_url(tournament_url)
    print(tournament)

bout_dataframe = compile_bout_dataframe_from_tournament_data(tournament)
bout_count = 10 
idx = random.sample(list(bout_dataframe.index),bout_count)

print("A random selection of {} bouts from the tournament:\n".format(bout_count))
print(bout_dataframe.loc[idx].to_markdown())

tournament_dict = tournament.create_tournament_dict()
print(tournament_dict)