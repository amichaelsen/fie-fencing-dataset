import json
from bs4 import BeautifulSoup


def get_json_var_from_script(soup, script_id, var_name):
    # each variable window._XXXX is ';' separated
    # print(soup)
    # print(script_id)
    # print(var_name)
    # print(soup.find('script', id=script_id))
    # print(len(list(soup.find('script', id=script_id))))
    try: 
        script = next(soup.find('script', id=script_id).children)
    except:
        print("Could not find script with id \'{}\' from soup {}".format(script_id,soup))
        return ""
    
    var_list = script.split(';')
    # get var_name Data (may be list or dict)
    try:
        var_string = [text.strip() for text in var_list if
                    text.strip().startswith(var_name)][0]
        json_variable = json.loads(var_string.split(" = ")[1])
    except:
        print("Error exctracting variable {} from list {}".format(var_name, var_list))
    return json_variable


def get_search_params(weapon=[], gender=[], category="", page=1):
    return {"name": "", "status": "passed",
            "gender": gender, "weapon": weapon,
            "type": ["i"], "season": "-1", "level": category,
            "competitionCategory": "", "fromDate": "",
            "toDate": "", "fetchPage": page}
