from pool_scraping import get_pool_data

test_pool = "pool_scraping/test_pool.html"

names, IDs, winners, scores = get_pool_data(test_pool)

for idx, name in enumerate(names):
    print("#{i} {name:<20} (ID {id})".format(i=idx+1, name=name, id=IDs[idx]))


# Print results of a single match 

fencer_idx = 2
opponent_idx = 4

print("{name1:<15} (ID {id1}) vs {name2:<15} (ID {id2})\n\
        Score:  {score1} - {score2}\n\
        Winner: {winner}".format(\
             name1 = names[fencer_idx], name2 = names[opponent_idx],
             id1 = IDs[fencer_idx], id2 = IDs[opponent_idx],
             score1 = scores[fencer_idx][opponent_idx], 
             score2 = scores[opponent_idx][fencer_idx], 
             winner = names[fencer_idx] if winners[fencer_idx][opponent_idx]==1 else names[opponent_idx]
             ))