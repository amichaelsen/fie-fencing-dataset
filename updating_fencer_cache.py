from os import path, stat
import json
import requests
from bs4 import BeautifulSoup
from fencers.fencer_scraping import get_fencer_nationality_data
from progress.bar import Bar

def clear_nationality_entries():
    cache_filename = 'fencers/fencer_cache.txt'
    with open(cache_filename) as read_file:
        cached_data = json.load(read_file)
        for key, value in Bar(' Updating fencer nationalities').iter(list(cached_data.items())):
            fencer_dict = value.copy() 
            if 'nationality' in list(value.keys()):
                fencer_url = "https://fie.org/athletes/"+str(key)
                req = requests.get(fencer_url)
                soup = BeautifulSoup(req.content, 'html.parser')
                country_code, country_name = get_fencer_nationality_data(soup)
                fencer_dict.pop('nationality')
                fencer_dict['country_code'] = country_code
                fencer_dict['country'] = country_name
                cached_data[key] = fencer_dict
        with open(cache_filename, 'w') as write_file:
            json.dump(cached_data, write_file)

clear_nationality_entries()