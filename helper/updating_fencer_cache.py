from os import path, stat
import json
import requests
from bs4 import BeautifulSoup
from fencers.fencer_scraping import get_fencer_nationality_data, get_req_content
from progress.bar import Bar

def clear_nationality_entries():
    cache_filename = 'fencers/fencer_cache.txt'
    with open(cache_filename) as read_file:
        cached_data = json.load(read_file)
        counter = 1 
        for key, value in Bar(' Updating fencer nationalities').iter(list(cached_data.items())):
            if 'nationality' in list(value.keys()):
                fencer_dict = value.copy() 
                fencer_url = "https://fie.org/athletes/"+str(key)
                content = get_req_content(int(key))
                soup = BeautifulSoup(content, 'html.parser')
                try:
                    country_code, country_name = get_fencer_nationality_data(soup)
                except:
                    print("\n -->Could not load country data for fencer: {}".format(key))
                fencer_dict.pop('nationality')
                fencer_dict['country_code'] = country_code
                fencer_dict['country'] = country_name
                cached_data[key] = fencer_dict
                counter += 1
            if counter % 50 == 0:
                print("\n updated {} fencer nationalities in {}".format(counter, cache_filename))
                with open(cache_filename, 'w') as write_file:
                    json.dump(cached_data, write_file)
        with open(cache_filename, 'w') as write_file:
            json.dump(cached_data, write_file)

clear_nationality_entries()