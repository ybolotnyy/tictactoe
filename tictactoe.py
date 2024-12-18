"""
Tic Tac Toe Player
"""
import copy
import math
import operator

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X

    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    if x_count > o_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY]


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board = copy.deepcopy(board)
    i, j = action

    if board[i][j] is None:
        board[i][j] = player(board)
        return board
    else:
        raise RuntimeError("Already used move!")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    def row_win(i, player):
        return all([board[i][j] == player for j in range(3)])

    def column_win(j, player):
        return all([board[i][j] == player for i in range(3)])

    def diagonal_win(player):
        left_to_right = [(0, 0), (1, 1), (2, 2)]
        right_to_left = [(2, 0), (1, 1), (0, 2)]

        return any([
            all([board[i][j] == player for i, j in left_to_right]),
            all([board[i][j] == player for i, j in right_to_left])
        ])

    for player in [X, O]:
        if any([row_win(i, player) for i in range(3)]):
            return player
        elif any([column_win(j, player) for j in range(3)]):
            return player
        elif diagonal_win(player):
            return player


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    board_filled = sum(line.count(None) for line in board) == 0
    if board_filled:
        return True
    else:
        if winner(board) is None:
            return False
        else:
            return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    status = winner(board)
    if status == "X":
        return 1
    elif status == "O":
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    Max = float("-inf")
    Min = float("inf")

    if player(board) == X:
        return Max_Value(board, Max, Min)[1]
    else:
        return Min_Value(board, Max, Min)[1]


def Max_Value(board, Max, Min):
    move = None
    if terminal(board):
        return [utility(board), None];
    v = float('-inf')
    for action in actions(board):
        test = Min_Value(result(board, action), Max, Min)[0]
        Max = max(Max, test)
        if test > v:
            v = test
            move = action
        if Max >= Min:
            break
    return [v, move]

def Min_Value(board, Max, Min):
    move = None
    if terminal(board):
        return [utility(board), None];
    v = float('inf')
    for action in actions(board):
        test = Max_Value(result(board, action), Max, Min)[0]
        Min = min(Min, test)
        if test < v:
            v = test
            move = action
        if Max >= Min:
            break
    return [v, move]