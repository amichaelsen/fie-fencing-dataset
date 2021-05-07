from fencers.fencer_scraping import get_fencer_info_from_ID
import time 


print("\n Loading fencer data without cache!\n")

fencer_IDs = [43803, 43803, 52027, 46080] # the last one does not have a nationality tag in her page 
for fencer_ID in fencer_IDs:
    print("")
    fencer_dict = get_fencer_info_from_ID(fencer_ID, use_cache=False)
    print(fencer_dict)
    print("")
    time.sleep(0.5)

time.sleep(3)

print("\n Loading fencer data with cache!\n")

# the last one does not have a nationality tag in her page
fencer_IDs = [43803, 43803, 52027, 46080]
for fencer_ID in fencer_IDs:
    print("")
    fencer_dict = get_fencer_info_from_ID(fencer_ID)
    print(fencer_dict)
    print("")
