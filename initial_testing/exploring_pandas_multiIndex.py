import requests
import json
from datetime import date, datetime
from os import path, stat
from bs4 import BeautifulSoup
import pandas as pd

import tabulate



def test_multi_index_by_div():

    iterables = [["Foil", "Epee", "Sabre"],
                 ["Cadet", "Junior", "Senior", "Veteran"],
                 ["2021", "2020", "2019"]]
    index = pd.MultiIndex.from_product(
        iterables, names=["Weapon", "Category", "Season"])
    # print(index)
    gen_ranking_dataframe = pd.DataFrame(
        columns=['rank', 'points'], index=index)
    # add a fake data point
    gen_ranking_dataframe.loc[('Foil', 'Senior', '2020'), :] = (2, 50)
    # print(gen_ranking_dataframe)

    # iterables = [["Foil", "Epee", "Sabre"],
    #  ["Cadet", "Junior", "Senior", "Veteran"],
    #  ["2021", "2020", "2019"]]
    # index = pd.MultiIndex.from_product(
    #    iterables, names=["Weapon", "Category", "Season"])
    # print(index)
    iterables1 = [["Foil"],
                  ["Cadet"],
                  ["2021", "2020"]]
    index1 = pd.MultiIndex.from_product(
        iterables1, names=["Weapon", "Category", "Season"])
    ranking_dataframe1 = pd.DataFrame(columns=['rank', 'points'], index=index1)
    print(ranking_dataframe1)

    # add a fake data point
    ranking_dataframe1.loc[('Foil', 'Cadet', '2020'), :] = (2, 50)
    ranking_dataframe1.loc[('Foil', 'Cadet', '2021'), :] = (10, 7.5)
    print(ranking_dataframe1)

    iterables2 = [["Epee"],
                  ["Cadet"],
                  ["2021", "2020", "2019"]]
    index2 = pd.MultiIndex.from_tuples([], names=["Weapon", "Category", "Season"])
    ranking_dataframe2 = pd.DataFrame(columns=['rank', 'points'], index=index2)
    print(ranking_dataframe2)

    # add a fake data point
    ranking_dataframe2.loc[('Epee', 'Cadet', '2021'), :] = (1, 72)
    ranking_dataframe2.loc[('Epee', 'Cadet', '2020'), :] = (2, 57)
    ranking_dataframe2.loc[('Epee', 'Cadet', '2019'), :] = (3, 46)
    ranking_dataframe2.loc[('Sabre', 'Junior', '2021'), :] = (15, 2)
    print(ranking_dataframe2)

    print("print all dataframes at the end")
    print(ranking_dataframe1)
    print(ranking_dataframe2)

    # combine these dataframes? 
    comb_ranking_dataframe = pd.concat([ranking_dataframe1,ranking_dataframe2], keys =["id1","id2"])
    print(comb_ranking_dataframe)
    return 


test_multi_index_by_div()