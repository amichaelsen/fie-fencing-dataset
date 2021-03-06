from helper.get_results import process_tournament_data_from_urls, get_url_list_from_seach
from helper.soup_scraping import get_search_params


# ## Diagnosing how many tournaments have 'id: 0' for fencers, and if *all* id's are zero or only some
# search_params = get_search_params(weapon=['f'], gender=['m'], category='j')
# url_list = get_url_list_from_seach(search_params) 
# short_list = url_list[0:50]
# for url in short_list:
#     single_list = [url]
#     tournaments_dataframe, bouts_dataframe, fencer_ID_list = process_tournament_data_from_urls(
#         single_list)
#     if 0 in fencer_ID_list:
#         print("Fencer ID List: {}".format(fencer_ID_list))
#         print("Tournament URL: {}".format(url))
# # Test Results: (ran for both s,f,c and s,f,j)
# # The following tournaments had missing fencer IDs: 
# #       https://fie.org/competitions/2016/941 (all fencer ids missing)


## Testing tournament return NoneType to avoid fencer Id = 0 
search_params = get_search_params(weapon=['s'], gender=['f'], category='c')
url_list = get_url_list_from_seach(search_params)[0:50] + ['https://fie.org/competitions/2016/1301',
                                                          'https://fie.org/competitions/2005/239', 'https://fie.org/competitions/2016/941']
tournaments_dataframe, bouts_dataframe, fencer_ID_list = process_tournament_data_from_urls(
    url_list)
print("Fencer ID List: {}".format(fencer_ID_list))
print(bouts_dataframe.to_markdown())

