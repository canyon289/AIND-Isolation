# For Zero indexed board
BOARD_HEIGHT = 6
BOARD_WIDTH = 6
MAXIMUM_MOVES = 8

from collections import namedtuple
import math
import ipdb

#Weight are Own Move, Op_Move, Distance Weight, Center Weight
WEIGHT_NAMES = ["om", "opm", "dm", "cw"]
WEIGHTS = namedtuple("weights", ["om", "opm", "dm", "cw"])

def score_closure(weights):
#    ipdb.set_trace()
    w = WEIGHTS(*weights)

    def custom_score(game, player):
        if game.is_loser(player):
            return float("-inf")

        if game.is_winner(player):
            return float("inf")

        opp = game.get_opponent(player)
        own_moves = len(game.get_legal_moves(player))
        opp_moves = len(game.get_legal_moves(opp))
        own_moves_score, opp_moves_score = own_moves/MAXIMUM_MOVES, opp_moves/MAXIMUM_MOVES

        own_x, own_y = game.get_player_location(player)
        opp_x, opp_y = game.get_player_location(opp)

        distance = math.sqrt((own_x-opp_x)**2 + (own_y-opp_y)**2)

        #Normalize to between 0 and 1
        distance_score = distance / math.sqrt(BOARD_HEIGHT**2 + BOARD_WIDTH**2)

        # Center distance hardcoded
        center = math.sqrt((own_x-BOARD_WIDTH/2)**2 + (own_y-BOARD_HEIGHT/2)**2)

        # Normalize to between 0 and 1
        center_score = center/math.sqrt((BOARD_HEIGHT/2)**2 + (BOARD_WIDTH/2)**2)

        scores = [own_moves_score, opp_moves_score, distance_score, center_score]

        weighted_score = [score*weight for score,weight in zip(scores,w)]
        score = weighted_score[0] - sum(weighted_score[1:])
        return score

    return custom_score

