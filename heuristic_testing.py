BOARD_HEIGHT = 7
BOARD_WIDTH = 7
from collections import namedtuple
from math import sqrt

#Weight are Own Move, Op_Move, Distance Weight, Center Weight
WEIGHTS = namedtuple("weights", ["om", "opm", "dm", "cw"])

def custom_score(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opp = game.get_opponent(player)
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(opp))
    own_x, own_y = game.get_player_location(player)
    opp_x, opp_y = game.get_player_location(opp)

    distance = math.sqrt((own_x-opp_x)**2 + (own_y-opp_y)**2)

    #Normalize to zero
    distance_score

    # Center distance hardcoded
    center = math.sqrt((own_x-BOARD_WIDTH/2)**2 + (own_y-BOARD_HEIGHT/2)**2)

    # Normalize to between 0 and 1
    center_score = distance/math.sqrt((BOARD_HEIGHT/2)**2 + (BOARD_WEIGHT/2)**2

    score = sum(score*weight for score,weight in zip(scores,
    score = w.own
    return score

