from get_results import process_tournament_data_from_urls, get_url_list_from_seach
from soup_scraping import get_search_params

# search_params = get_search_params(weapon=['s'], gender=['f'], category='c')
# url_list = get_url_list_from_seach(search_params)[0:2] + ['https://fie.org/competitions/2016/1301',
#                                                           'https://fie.org/competitions/2005/239', 'https://fie.org/competitions/2016/941']
# # for url in url_list:
# # single_list = [url]
# tournaments_dataframe, bouts_dataframe, fencer_ID_list = process_tournament_data_from_urls(
#     url_list)
# # print("Tournament URL: {}".format(url))
# print("Fencer ID List: {}".format(fencer_ID_list))
# print(bouts_dataframe.to_markdown())



search_params = get_search_params(weapon=['s'], gender=['f'], category='c')
url_list = get_url_list_from_seach(search_params) + ['https://fie.org/competitions/2016/1301',
                                                          'https://fie.org/competitions/2005/239', 'https://fie.org/competitions/2016/941']
for url in url_list:
    single_list = [url]
    tournaments_dataframe, bouts_dataframe, fencer_ID_list = process_tournament_data_from_urls(
        single_list)
    if 0 in fencer_ID_list:
        print("Fencer ID List: {}".format(fencer_ID_list))
        print("Tournament URL: {}".format(url))

# print("Tournament URL: {}".format(url))
