from dataframe_columns import convert_list_to_dataframe_with_multi_index
from dataframe_columns import multiIndex_relabeler
print("\n Testing pandas multi-indexing\n")

fencer_list_of_results = [{"weapon": "E", "category": "C", "season": "2020", "rank": 2, "points": 50},
                          {"weapon": "F", "category": "C",
                           "season": "2020", "rank": 3, "points": 24},
                          {"weapon": "F", "category": "C",
                           "season": "2019", "rank": 5, "points": 25},
                          {"weapon": "F", "category": "C",
                           "season": "2021", "rank": 7, "points": 27},
                          {"weapon": "E", "category": "J", "season": "2020", "rank": 4, "points": 32}, ]
fencer_column_names = ["weapon", "category", "season", 'rank', 'points']

fencer_idx_names = ["weapon", "category", "season"]

fencer_ranking_df = convert_list_to_dataframe_with_multi_index(
    fencer_list_of_results, fencer_column_names, fencer_idx_names)

print(fencer_ranking_df)

# create dataframe from list
all_list_of_results = [{"id": 123, "weapon": "E", "category": "C", "season": "2020", "rank": 2, "points": 50},
                       {"id": 124, "weapon": "F", "category": "C",
                        "season": "2020", "rank": 3, "points": 24},
                       {"id": 123, "weapon": "F", "category": "C",
                        "season": "2019", "rank": 5, "points": 25},
                       {"id": 124, "weapon": "F", "category": "C",
                        "season": "2020", "rank": 7, "points": 27},
                       {"id": 123, "weapon": "E", "category": "C",
                        "season": "2020", "rank": 2, "points": 50},
                       {"id": 124, "weapon": "F", "category": "C",
                        "season": "2021", "rank": 3, "points": 24},
                       {"id": 123, "weapon": "F", "category": "J",
                        "season": "2020", "rank": 5, "points": 25},
                       {"id": 124, "weapon": "F", "category": "C",
                        "season": "2021", "rank": 7, "points": 27},
                       {"id": 125, "weapon": "E", "category": "J", "season": "2020", "rank": 4, "points": 32}, ]
all_column_names = ["id", "weapon", "category", "season", 'rank', 'points']

all_idx_names = ["id", "weapon", "category", "season"]

all_ranking_df = convert_list_to_dataframe_with_multi_index(
    all_list_of_results, all_column_names, all_idx_names)

print(all_ranking_df)


# testing relabeling in the dataframe multiindex

print("\n\nTest relabeling keys for multindex\n\n")
print(all_ranking_df)

weapon_dict = {"E": "Epee", "F": "Foil"}
category_dict = {"C": "Cadet", "J": "Junior"}




index = all_ranking_df.index
# print(index)

# new_index = all_ranking_df.index.map(weapon_dict)

# print(new_index)
# print(index.levels[1])
# print(index.levels[1].map(weapon_dict))
new_index = index.levels[1].map(weapon_dict)

all_ranking_df.index = index.set_levels(new_index, level=1)
# maybe easier to do the relabeling before getting to a dataframe?
print(all_ranking_df)


multiIndex_relabeler(all_ranking_df, 2, category_dict)
print(all_ranking_df)

multiIndex_relabeler(all_ranking_df, 3, make_season_from_year)
print(all_ranking_df)
