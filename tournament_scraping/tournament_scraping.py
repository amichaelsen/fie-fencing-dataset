import re
import requests
import json
from bs4 import BeautifulSoup
# <script id="js-competition">


def get_pool_list_from_url(tournament_url):
    req = requests.get(tournament_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    # the <script id="js-competition"> tag contains the pool data
    script = next(soup.find('script', id="js-competition").children)
    # each variable window._XXXX is ';' separated and window._pools 
    # contains pool data. Caution: do NOT want window._poolsMobile
    pools_string = [text.strip() for text in script.split(
        ';') if text.strip().startswith('window._pools ')][0]
    # pools_string = "window._pools = [{...dict info here...}]"
    # split to get value, then extract dictionary 
    pool_list = json.loads(pools_string.split(" = ")[1])['pools']
    return pool_list



