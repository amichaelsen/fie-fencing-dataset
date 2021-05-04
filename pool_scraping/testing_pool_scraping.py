from pool_scraping import get_pool_data

test_pool = "pool_scraping/test_pool.html"

names, ids, winners, scores = get_pool_data(test_pool)


# Print entire pools table
print("\nLoaded and parsed pool data from: {}\n".format(test_pool))
print("Data from entire pool:\n")
print("                                    |", end="")
for i in range(1, len(list(names))+1):
    print(" # {} |".format(i), end="")
print("\n-------------------------------------------------------------------------------")

for idx, name in enumerate(names):
    print("#{i} {name:<20} (ID {id})  |".format(
        i=idx+1, name=name, id=ids[idx]), end="")
    for j in range(0, len(list(names))):
        if(j == idx):
            print(" --- |", end="")
        else:
            victory_indicator = "V" if winners[idx][j] == 1 else "D"
            print(" {vw}/{sc} |".format(vw=victory_indicator,
                  sc=scores[idx][j]), end="")
    print("")
print("\n")


# Print results of a single match
fencer_idx = 2
opponent_idx = 4
print("Showing result from single match (fencers {} and {}):".format(
    fencer_idx, opponent_idx))

print("   {name1:<15} (ID {id1}) vs {name2:<15} (ID {id2})\n\
        Score:  {score1} - {score2}     Winner: {winner}".format(
    name1=names[fencer_idx], name2=names[opponent_idx],
    id1=ids[fencer_idx], id2=ids[opponent_idx],
    score1=scores[fencer_idx][opponent_idx],
    score2=scores[opponent_idx][fencer_idx],
    winner=names[fencer_idx] if winners[fencer_idx][opponent_idx] == 1 else names[opponent_idx]
))
print("")
