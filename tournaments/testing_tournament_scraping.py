import requests
import re
import json
import random
from bs4 import BeautifulSoup
from tournament_scraping import create_tournament_data_from_url


list_of_urls = ['https://fie.org/competitions/2020/771', 
                'https://fie.org/competitions/2021/1070',
                'https://fie.org/competitions/2021/92']

for tournament_url in list_of_urls:
    print("Tournament URL for lookup: {}".format(tournament_url))
    tournament = create_tournament_data_from_url(tournament_url)

    print(tournament)



