import pandas as pd 

date = 'May_12_2021'
div_name = 'cadet_womens_foil'

bout_data            = pd.read_csv('output/'+date+'/'+div_name+ '_bout_data_'            +date+'.csv')
tournament_data      = pd.read_csv('output/'+date+'/'+div_name+ '_tournament_data_'      +date+'.csv')
fencer_bio_data      = pd.read_csv('output/'+date+'/'+div_name+ '_fencer_bio_data_'      +date+'.csv')
fencer_rankings_data = pd.read_csv('output/'+date+'/'+div_name+ '_fencer_rankings_data_' +date+'.csv')
