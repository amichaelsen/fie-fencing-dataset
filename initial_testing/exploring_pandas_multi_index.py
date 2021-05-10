from fencers.fencer_scraping import convert_list_to_dataframe_with_multi_index

print("\n Testing pandas multi-indexing\n")

fencer_list_of_results = [{"weapon": "Epee", "category": "Cadet", "season": "2020", "rank": 2, "points": 50},
                          {"weapon": "Foil", "category": "Cadet",
                           "season": "2020", "rank": 3, "points": 24},
                          {"weapon": "Foil", "category": "Cadet",
                           "season": "2019", "rank": 5, "points": 25},
                          {"weapon": "Foil", "category": "Cadet",
                           "season": "2021", "rank": 7, "points": 27},
                          {"weapon": "Epee", "category": "Junior", "season": "2020", "rank": 4, "points": 32}, ]
fencer_column_names = ["weapon", "category", "season", 'rank', 'points']

fencer_idx_names = ["weapon", "category", "season"]

fencer_ranking_df = convert_list_to_dataframe_with_multi_index(
    fencer_list_of_results, fencer_column_names, fencer_idx_names)

print(fencer_ranking_df)

# create dataframe from list
all_list_of_results = [{"id": 123, "weapon": "Epee", "category": "Cadet", "season": "2020", "rank": 2, "points": 50},
                       {"id": 124, "weapon": "Foil", "category": "Cadet",
                        "season": "2020", "rank": 3, "points": 24},
                       {"id": 123, "weapon": "Foil", "category": "Cadet",
                        "season": "2019", "rank": 5, "points": 25},
                       {"id": 124, "weapon": "Foil", "category": "Cadet",
                        "season": "2020", "rank": 7, "points": 27},
                       {"id": 123, "weapon": "Epee", "category": "Cadet",
                        "season": "2020", "rank": 2, "points": 50},
                       {"id": 124, "weapon": "Foil", "category": "Cadet",
                        "season": "2021", "rank": 3, "points": 24},
                       {"id": 123, "weapon": "Foil", "category": "Junior",
                        "season": "2020", "rank": 5, "points": 25},
                       {"id": 124, "weapon": "Foil", "category": "Cadet",
                        "season": "2021", "rank": 7, "points": 27},
                       {"id": 125, "weapon": "Epee", "category": "Junior", "season": "2020", "rank": 4, "points": 32}, ]
all_column_names = ["id", "weapon", "category", "season", 'rank', 'points']

all_idx_names = ["id", "weapon", "category", "season"]

all_ranking_df = convert_list_to_dataframe_with_multi_index(
    all_list_of_results, all_column_names, all_idx_names)

print(all_ranking_df)