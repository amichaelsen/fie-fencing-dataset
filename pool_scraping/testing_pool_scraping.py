from pool_scraping import get_pool_data
from pool_data import poolData
import numpy as np

# ------------------------------------
#         Test poolData class
# ------------------------------------

print("\nDOCSTRING for PoolData:\n{}".format(poolData.__doc__))

winners = np.array([[0, 1, 1], [0, 0, 0], [0, 1, 0]])
scores = np.array([[0, 4, 5], [2, 0, 3], [3, 5, 0]])

fake_pool = poolData(3, ['Alice', 'Bob', 'Charlie'], [1, 2, 3],
                     winners, scores)

print("String representation of fake pool:\n")
print(fake_pool)

# ------------------------------------
#         Test pool scraping
# ------------------------------------

test_pool = "pool_scraping/test_pool.html"
loaded_pool = get_pool_data(test_pool)
print("String representation of pool loaded from {}:\n".format(test_pool))
print(loaded_pool)


# Print results of a single match
fencer_idx = 2
opponent_idx = 4
print("Showing result from single match (fencers #{} and #{}):".format(
    fencer_idx+1, opponent_idx+1))

print("   {name1:<15} (ID {id1}) vs {name2:<15} (ID {id2})\n\
        Score:  {score1} - {score2}     Winner: {winner}\n".format(
    name1=loaded_pool.get_name_by_idx(fencer_idx), name2=loaded_pool.get_name_by_idx(opponent_idx),
    id1=loaded_pool.get_ID_by_idx(fencer_idx), id2=loaded_pool.get_ID_by_idx(opponent_idx),
    score1=loaded_pool.scores[fencer_idx][opponent_idx],
    score2=loaded_pool.scores[opponent_idx][fencer_idx],
    winner=loaded_pool.get_name_by_idx(fencer_idx) if loaded_pool.winners[fencer_idx][opponent_idx] == 1 else loaded_pool.get_name_by_idx(opponent_idx)))
