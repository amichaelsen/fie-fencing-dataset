import requests
import json
from bs4 import BeautifulSoup
from progress.bar import Bar

from helper.soup_scraping import get_json_var_from_script
from helper.caching_methods import save_dict_to_cache


def construct_country_flag_code():
    flag_to_country_code = {}
    print("Fetching country flag codes...")
    for weapon in ['f', 'e', 's']:
        for gender in ['m', 'f']:
            page_params = {"country": "",
                           "gender": gender,
                           "fetchPage": 1,
                           "isSearch": False,
                           "isTeam": False,
                           "level": "s",
                           "name": "",
                           "season": "2021",
                           "type": "i",
                           "weapon": weapon}
            more_fencers = True
            print("\n  weapon: {} gender: {}".format(weapon, gender))
            while more_fencers:
                print("\r    fetching page: {}".format(
                    page_params['fetchPage']), end="")
                req = requests.post(
                    'https://fie.org/athletes', data=page_params)
                athlete_list = req.json()['allAthletes']
                if len(athlete_list) == 0:
                    more_fencers = False
                for athlete in athlete_list:
                    flag_to_country_code[athlete['flag']] = athlete['country']
                page_params['fetchPage'] = page_params['fetchPage'] + 1
    print("\n Country codes found: {}".format(len(flag_to_country_code)))
    print(flag_to_country_code)
    with open('fencers/flag_to_country_code.txt', 'w') as write_file:
        json.dump(flag_to_country_code, write_file)


def construct_country_code_to_name():
    country_code_to_name = {}
    print("Fetching country codes...")
    req = requests.get('https://fie.org/athletes')
    soup = BeautifulSoup(req.content, 'html.parser')
    country_var_name = "window._countries "
    country_list = get_json_var_from_script(
        soup=soup, script_id="js-athletes", var_name=country_var_name)
    for country in country_list:
        key = country['id']
        value = country['name']
        country_code_to_name[key] = value

    print(len(country_list))
    print(country_list[0])
    print(country_code_to_name)
    with open('fencers/country_code_to_name.txt', 'w') as write_file:
        json.dump(country_code_to_name, write_file)



def get_fencer_country_code(soup):
    # get flag code

    # convert flag code to country using pre-made dict

    # if not in dict, return two letter flag icon code?
    return

# construct_country_flag_code()
# construct_country_code_to_name()


# Testing that all flags have a country code and name value
with open('fencers/flag_to_country_code.txt') as flag_file:
    with open('fencers/country_code_to_name.txt') as country_file:
        flag_data = json.load(flag_file)
        country_data = json.load(country_file)
        for k,v in flag_data.items():
            if v not in list(country_data.keys()):
                print("Country flag-code not found in country name dict")
                print("Country flag: {}\nCountry Code: {}".format(k,v))