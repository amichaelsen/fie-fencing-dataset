import requests
import re
import json
import random
from bs4 import BeautifulSoup
from tournament_scraping import create_tournament_data_from_url, compile_bout_dataframe_from_tournament_data
from tournament_data import TournamentData

list_of_urls = ['https://fie.org/competitions/2020/771', 
                'https://fie.org/competitions/2021/1070',
                'https://fie.org/competitions/2021/92']

for tournament_url in list_of_urls:
    print("Tournament URL for lookup: {}".format(tournament_url))
    tournament = create_tournament_data_from_url(tournament_url)

    print(tournament)

bout_dataframe = compile_bout_dataframe_from_tournament_data(tournament)

print(bout_dataframe.to_markdown())

tournament_dict = tournament.create_tournament_dict()
print(tournament_dict)