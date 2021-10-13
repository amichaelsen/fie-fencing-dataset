import pandas as pd
from datetime import date
from os import path, makedirs

from helper.get_results import get_results_for_division

save_results = True 

weapon = 'f'
gender = 'f'
category = ''


weapon_dict = {'f': "foil", 'e': 'epee', 's': 'sabre'}
gender_dict = {'f': "womens", 'm': 'mens'}
category_dict = {'c': 'cadet', 'j': 'junior', 's':'senior', 'v':'veteran', '':'all'}

div_name = category_dict[category] + "_" + gender_dict[gender] + "_" + weapon_dict[weapon]

print("\n\n Loading all results + fencer data for {}".format(" ".join(div_name.split("_"))))
print("----------------------------------------------------------------------\n\n")


tourn_df, bout_df, fencers_bio_df, fencers_rankings_df = get_results_for_division(
    weapon=[weapon], gender=[gender], category=category, 
    use_tournament_cache=True, use_fencer_data_cache=True, use_fencer_req_cache=True)

if save_results:

    date_string = date.today().strftime("%b_%d_%Y")
    directory = 'output/'+date_string+"/"

    if not path.exists(directory):
        makedirs(directory)

    name_list = ['tournament_data', 'bout_data', 'fencer_bio_data', 'fencer_rankings_data']
    for idx, df in enumerate([tourn_df, bout_df, fencers_bio_df]):
        name = name_list[idx]
        file_name = div_name + "_" + name + "_" + date_string + ".csv"
        df.to_csv(directory+file_name, index=False)
    
    name = 'fencer_rankings_data'
    file_name = div_name + "_" + name + "_" + date_string + ".csv"
    fencers_rankings_df.to_csv(directory+file_name)

else: # store in a temp cache just in case! 
    date_string = date.today().strftime("%b_%d_%Y")
    directory = 'temp_cache/'+date_string+"/"

    if not path.exists(directory):
        makedirs(directory)

    name_list = ['tournament_data', 'bout_data', 'fencer_bio_data', 'fencer_rankings_data']
    for idx, df in enumerate([tourn_df, bout_df, fencers_bio_df]):
        name = name_list[idx]
        file_name = div_name + "_" + name + "_" + date_string + ".csv"
        df.to_csv(directory+file_name, index=False)
    
    name = 'fencer_rankings_data'
    file_name = div_name + "_" + name + "_" + date_string + ".csv"
    fencers_rankings_df.to_csv(directory+file_name)