from fencers.fencer_scraping import get_fencer_info_from_ID


fencer_IDs = [43803, 52027]
for fencer_ID in fencer_IDs:
    fencer_dict = get_fencer_info_from_ID(fencer_ID)
    print(fencer_dict)