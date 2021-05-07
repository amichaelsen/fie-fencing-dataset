TOURNAMENTS_DF_COLS = ['competition_ID', 'season', 'name', 'category', 'country',
                       'start_date', 'end_date', 'weapon', 'gender', 'timezone', 'url', 'unique_ID']

BOUTS_DF_COLS = ['fencer_ID', 'opp_ID', 'fencer_age', 'opp_age',
                 'fencer_score', 'opp_score',
                 'winner_ID', 'fencer_curr_pts', 'opp_curr_pts',
                 'tournament_ID', 'pool_ID', 'upset']

FENCERS_BIO_DF_COLS      = ['id', 'name', 'nationality', 'hand', 'age', 'url','date_accessed']

FENCERS_RANKINGS_DF_COLS = ['id', 'weapon', 'category', 'season', 'rank', 'points']

FENCERS_RANKINGS_MULTI_INDEX = ['id', 'weapon', 'category', 'season']