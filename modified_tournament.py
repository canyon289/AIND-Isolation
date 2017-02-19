import itertools
import pickle

from tournament import modified_main

own_moves = [3, 2, 1]
op_moves = [1, .8, .6, 0]
center_weights = [1, .6, .2, 0]
distance_weights = [1, .6, .2, 0]

weights = list(itertools.product(own_moves, op_moves, center_weights, distance_weights))
#weights = list(itertools.product(own_moves[:1], op_moves[:1], center_weights[:1], distance_weights[:1]))
#weights = list(itertools.product(own_moves[:2], op_moves[:2]))
print("Number of combinations: {0}".format(len(weights)))
weight_win = modified_main(weights)
with open("output.p", 'wb') as f:
    pickle.dump(weight_win,f)