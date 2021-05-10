import json 
from bs4 import BeautifulSoup

def get_json_var_from_script(soup, script_id, var_name):
    # each variable window._XXXX is ';' separated
    script = next(soup.find('script', id=script_id).children)
    var_list = script.split(';')

    # get var_name Data (may be list or dict)
    var_string = [text.strip() for text in var_list if
                     text.strip().startswith(var_name)][0]
    json_variable = json.loads(tabOpp_string.split(" = ")[1])
    return json_variable
    
