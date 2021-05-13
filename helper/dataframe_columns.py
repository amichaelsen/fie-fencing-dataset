import pandas as pd

# unique_ID is constructed from season (YYYY) and competition_ID e.g. '2020-771'
# season = the year that the event took place
TOURNAMENTS_DF_COLS = ['competition_ID', 'season', 'name', 'category', 'country',
                       'start_date', 'end_date', 'weapon', 'gender', 'timezone',
                       'url', 'unique_ID', 'missing_results_flag']

# XX_curr_pts is the athlete's points in the division *at the time of the event*
# XX_a is the athlete's age *at the time of the event*
# upset records an upset, if neither fencer has points upset is False
# tournament_ID is the 'unique_ID' for the tournament the bout came from
# date is the date of the bout, approximated by the start date of the tournament
BOUTS_DF_COLS = ['fencer_ID', 'opp_ID', 'fencer_age', 'opp_age',
                 'fencer_score', 'opp_score', 'winner_ID', 'fencer_curr_pts',
                 'opp_curr_pts', 'tournament_ID', 'pool_ID', 'upset', 'date']

# country_code is three letter code for a fencer's country
# country is the full name of the fencer's country
# url is for the athlete's bio page on fie.org
# date_accessed records *when* the fencer's data was collected,
# stored because age, points, and ranking (in particular) may change
FENCERS_BIO_DF_COLS = ['id', 'name', 'country_code', 'country',
                       'hand', 'age', 'url', 'date_accessed']

FENCERS_RANKINGS_DF_COLS = ['id', 'weapon', 'category',
                            'season', 'rank', 'points']

# these fields are used to create a pandas multiIndex (heirachy as ordered)
FENCERS_RANKINGS_MULTI_INDEX = ['id', 'weapon', 'category', 'season']


def convert_list_to_dataframe_with_multi_index(list_of_data, column_names, index_names):
    """Creates dataframe with multiIndex (using index_names) from list_of_data"""
    # create dataframe from list
    dataframe = pd.DataFrame(data=list_of_data, columns=column_names)

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


def convert_dataframe_index_to_multi_index(dataframe, index_names):
    """Converts dataframe index to multiIndex using specified columns"""
    dataframe.sort_values(by=index_names, inplace=True)
    list_data = dataframe.values.tolist()
    columns = dataframe.columns
    dataframe = convert_list_to_dataframe_with_multi_index(
        list_of_data=list_data, column_names=columns, index_names=index_names)

    return dataframe


def relabel_multiIndex(dataframe, level, mapper):
    """Relabels multiIndex at specified level using mapper (e.g. dict)"""
    multi_index = dataframe.index
    level_to_relabel = multi_index.levels[level]
    relabeled_level = level_to_relabel.map(mapper)
    dataframe.index = multi_index.set_levels(relabeled_level, level=level)


def make_season_from_year(year):
    """Given start year from season return season string (e.g. '2015/2016')"""
    return str(int(year))+"/"+str(int(year)+1)
