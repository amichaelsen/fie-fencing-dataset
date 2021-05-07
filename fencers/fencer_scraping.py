import requests
import json
from bs4 import BeautifulSoup


def get_fencer_info_from_ID(fencer_ID):
    """
    Takes url for athlete page and returns dict of fencer data with keys FENCERS_DF_COLS
    """
    fencer_url = "https://fie.org/athletes/"+str(fencer_ID)
    req = requests.get(fencer_url)
    soup = BeautifulSoup(req.content, 'html.parser')

    # h1 class="AthleteHero-fencerName
    name_tag = soup.find('h1', class_='AthleteHero-fencerName')
    fencer_name = name_tag.get_text()

    info_div = soup.find('div', class_="ProfileInfo")
    # info_div has 6 sub-divs for example
    #     <div class="ProfileInfo Container Container--wider">
    #         <div class="ProfileInfo-item">
    #             <span>foil</span>
    #         </div>
    #         <div class="ProfileInfo-item">
    #             <span>Rank</span><span class="ProfileInfo-rank">13</span>
    #         </div>
    #         <div class="ProfileInfo-item">
    #             <span class="ProfileInfo-label">Pts</span>  <span>93.000</span></div>
    #         <div class="ProfileInfo-item">
    #             <span class="ProfileInfo-label">Age</span>  <span>22</span></div>
    #         <div class="ProfileInfo-item">
    #             <span class="ProfileInfo-label">Hand</span>  <span>R</span></div>
    #         <div class="ProfileInfo-item ProfileInfo-item--show-md">
    #             <a class="ProfileInfo-link" href="/athletes/43803/profile" target="_blank">Download profile</a></div>
    #     </div>

    for info_item in info_div.children:
        if(info_item.get_text().startswith('foil') or info_item.get_text().startswith('epee') or info_item.get_text().startswith('saber')):
            weapon = info_item.get_text()
        elif(info_item.get_text().startswith('Pts')):
            points = float(list(info_item.children)[1].get_text())
        elif(info_item.get_text().startswith('Hand')):
            hand = list(info_item.children)[1].get_text()
        elif(info_item.get_text().startswith('Age')):
            age = list(info_item.children)[1].get_text()
        elif(info_item.get_text().startswith('Rank')):
            rank = list(info_item.children)[1].get_text()

    return {'id': fencer_ID, 'name': fencer_name, 'url': fencer_url, 'hand': hand, 'weapon': weapon, 'points': points, 'rank': rank, 'age': age}
