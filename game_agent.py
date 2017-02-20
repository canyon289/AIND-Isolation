"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
from collections import defaultdict
import math
import ipdb


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

INF = 1000000
NEG_INF = -1 * INF
BOARD_HEIGHT = 6
BOARD_WIDTH = 6
MAXIMUM_MOVES = 8


def custom_score_original(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    score = float(len(game.get_legal_moves(player)))
    
    return score
    
def custom_score(game, player):
    #Weights from Cross Validation
    w = (3,1,1,0)
    
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
    
class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate successors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if len(legal_moves) == 0:
                move = (-1,-1)

            if self.iterative is True:
                # Some crazy high number
                maximum_depth = 100000
                for depth in range(1, maximum_depth):
                    self.search_depth = depth
                    utility, move = getattr(self, self.method)(game, depth)
            else:
                utility, move = getattr(self, self.method)(game, self.search_depth)
            return move

        except Timeout:
            # Handle any actions required at timeout, if necessary
            #self.search_depth = maximum_depth
            # Return the best move from the last completed search iteration
            try:
                return move
            except UnboundLocalError:
                return legal_moves[0]


    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if depth == 0:
            return self.score(game, self), None

        else:

            if maximizing_player is True:
                level_function = max

            if maximizing_player is False:
                level_function = min

            legal_moves = game.get_legal_moves()

            if len(legal_moves) == 0:
                return 0, (-1, -1)

            utility_list = []
            for move in legal_moves:
                next_game_state = game.forecast_move(move)
                node_score, _ = self.minimax(next_game_state, depth-1, maximizing_player=(not maximizing_player))
                utility_list.append((node_score, move))
                utility, move = level_function(utility_list, key=lambda x: x[0])
            return utility, move

    def alphabeta(self, game, depth, alpha=NEG_INF, beta=INF, maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        best_move = (-1, -1)
        best_score = NEG_INF

        legal_moves = game.get_legal_moves()

        for move in legal_moves:
            next_game_state = game.forecast_move(move)
            v = self.min_value(next_game_state, depth-1, best_score, beta)
            if v > best_score:
                best_move = move
                best_score = v
        return best_score, best_move

    def max_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if depth == 0:
            return self.score(game, self)

        legal_moves = game.get_legal_moves()

        if len(legal_moves) == 0:
            return float("-inf")

        v = NEG_INF
        for move in legal_moves:
            next_game_state = game.forecast_move(move)
            node_utility = self.min_value(next_game_state, depth-1, alpha, beta)
            # V is the best value the node as seen so far
            v = max(node_utility, v)
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if depth == 0:
            return self.score(game, self)

        legal_moves = game.get_legal_moves()

        if len(legal_moves) == 0:
            return float("inf")

        v = INF
        for move in legal_moves:
            next_game_state = game.forecast_move(move)
            node_utility = self.max_value(next_game_state, depth-1, alpha, beta)

            v = min(node_utility, v)
            if v <= alpha:
                return v

            beta = min(beta, v)
        return v
