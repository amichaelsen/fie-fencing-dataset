import pandas as pd 

TOURNAMENTS_DF_COLS = ['competition_ID', 'season', 'name', 'category', 'country',
                       'start_date', 'end_date', 'weapon', 'gender', 'timezone', 'url', 'unique_ID', 'missing_results_flag']

BOUTS_DF_COLS = ['fencer_ID', 'opp_ID', 'fencer_age', 'opp_age',
                 'fencer_score', 'opp_score',
                 'winner_ID', 'fencer_curr_pts', 'opp_curr_pts',
                 'tournament_ID', 'pool_ID', 'upset', 'date']

FENCERS_BIO_DF_COLS = ['id', 'name', 'country_code', 'country',
                       'hand', 'age', 'url', 'date_accessed']

FENCERS_RANKINGS_DF_COLS = ['id', 'weapon',
                            'category', 'season', 'rank', 'points']

FENCERS_RANKINGS_MULTI_INDEX = ['id', 'weapon', 'category', 'season']



def convert_list_to_dataframe_with_multi_index(list_of_results, column_names, index_names):
    """
    Takes a list of dict data and returns a pd.DataFrame with multiIndex from specified columns
    """
    # create dataframe from list
    dataframe = pd.DataFrame(data=list_of_results, columns=column_names)

    # construct multiIndex (sort first to group by heirarchy)
    idx_array = []
    dataframe.sort_values(by=index_names, inplace=True)
    for name in index_names:
        idx_array.append(dataframe[name])
    new_index = pd.MultiIndex.from_arrays(idx_array)

    # convert to multi index and drop columns used to create multiIndex
    dataframe.index = new_index
    dataframe = dataframe.drop(columns=index_names)

    return dataframe

def multiIndex_relabeler(dataframe, level, mapper):
    multi_index = dataframe.index 
    level_to_relabel = multi_index.levels[level]
    relabeled_level = level_to_relabel.map(mapper)
    dataframe.index = multi_index.set_levels(relabeled_level, level=level)

def make_season_from_year(year):
    return str(int(year))+"/"+str(int(year)+1)
