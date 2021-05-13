import pandas as pd 
from helper.dataframe_columns import FENCERS_RANKINGS_DF_COLS, FENCERS_RANKINGS_MULTI_INDEX
from helper.dataframe_columns import convert_list_to_dataframe_with_multi_index

date = 'May_12_2021'
div_name = 'all_womens_foil'

bout_df            = pd.read_csv('output/'+date+'/'+div_name+ '_bout_data_'            +date+'.csv')
tournament_df      = pd.read_csv('output/'+date+'/'+div_name+ '_tournament_data_'      +date+'.csv')
fencer_bio_df      = pd.read_csv('output/'+date+'/'+div_name+ '_fencer_bio_data_'      +date+'.csv')
init_rankings_df   = pd.read_csv('output/'+date+'/'+div_name+ '_fencer_rankings_data_' +date+'.csv')

fencer_rankings_df = convert_list_to_dataframe_with_multi_index(init_rankings_df.values.tolist(), FENCERS_RANKINGS_DF_COLS, FENCERS_RANKINGS_MULTI_INDEX)

# from load_csv import tournament_df, bout_df, fencer_bio_df, fencer_rankings_df