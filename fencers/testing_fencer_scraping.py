from fencers.fencer_scraping import get_fencer_data_lists_from_ID_list
from dataframe_columns import FENCERS_BIO_DF_COLS, FENCERS_RANKINGS_DF_COLS, FENCERS_RANKINGS_MULTI_INDEX
import time
import pandas as pd
from dataframe_columns import convert_list_to_dataframe_with_multi_index

# print("\n Loading fencer data without cache!\n")

# fencer_IDs = [43803, 43803, 52027, 46080] # the last one does not have a nationality tag in her page
# for fencer_ID in fencer_IDs:
#     print("")
#     fencer_dict = get_fencer_info_from_ID(fencer_ID, use_cache=False)
#     print(fencer_dict)
#     print("")
#     time.sleep(0.5)

# time.sleep(3)

# print("\n Loading fencer data with cache!\n")

# # the last one does not have a nationality tag in her page
# fencer_IDs = [43803, 43803, 52027, 46080]
# for fencer_ID in fencer_IDs:
#     print("")
#     fencer_dict = get_fencer_info_from_ID(fencer_ID)
#     print(fencer_dict)
#     print("")


fencer_IDs = [46080, 12054]
# fencer_IDs = [37080]
fencers_bio_list, fencers_rankings_list = get_fencer_data_lists_from_ID_list(
    fencer_IDs, use_cache=False)

fencers_bio_dataframe = pd.DataFrame(
    data=fencers_bio_list, columns=FENCERS_BIO_DF_COLS)
fencers_rankings_dataframe = convert_list_to_dataframe_with_multi_index(
    list_of_data=fencers_rankings_list,
    column_names=FENCERS_RANKINGS_DF_COLS, index_names=FENCERS_RANKINGS_MULTI_INDEX)

print(fencers_bio_dataframe)

print(fencers_rankings_dataframe)
