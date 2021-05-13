import requests
import json
from bs4 import BeautifulSoup

from helper.soup_scraping import get_json_var_from_script

url = 'https://fie.org/competitions'
# making request without any checkboxes

search_url = 'https://fie.org/competitions/search'

page_num = 1 
# 'm' = Mens 's' = Sabre '-1' = all seasons
search_params = {"name": "", "status": "passed",
                 "gender": ["w"], "weapon": ["s"],
                 "type": ["i"], "season": "-1", "level": "",
                 "competitionCategory": "", "fromDate": "",
                 "toDate": "", "fetchPage": page_num }

req = requests.post(search_url, data=search_params)

print("\nRequest Status Code: {}\n".format(req.status_code))

json = req.json()

print(type(json))
print(json.keys())

print("Total Events Found: {}".format(json['totalFound']))

print("Page Size: {}    Pages Needed: {}".format(json['pageSize'], json['totalFound']//json['pageSize']))

print("First Tournament: {}".format(json['items'][0]))


