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
    def row_win(i, _player):
        return all([board[i][j] == _player for j in range(3)])

    def column_win(j, _player):
        return all([board[i][j] == _player for i in range(3)])

    def diagonal_win(_player):
        left_to_right = [(0, 0), (1, 1), (2, 2)]
        right_to_left = [(2, 0), (1, 1), (0, 2)]

        return any([
            all([board[i][j] == _player for i, j in left_to_right]),
            all([board[i][j] == _player for i, j in right_to_left])
        ])

    for _player in [X, O]:
        if any([row_win(i, _player) for i in range(3)]):
            return _player
        elif any([column_win(j, _player) for j in range(3)]):
            return _player
        elif diagonal_win(_player):
            return _player


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
    if status == X:
        return 1
    elif status == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    _max = float("-inf")
    _min = float("inf")

    if player(board) == X:
        return max_value(board, _max, _min)[1]
    else:
        return min_value(board, _max, _min)[1]


def max_value(board, _max, _min):
    """
    Returns max value nad action for the current player on the board.
    """
    move = None
    if terminal(board):
        return [utility(board), None]
    v = float('-inf')
    for action in actions(board):
        test = min_value(result(board, action), _max, _min)[0]
        _max = max(_max, test)
        if test > v:
            v = test
            move = action
        if _max >= _min:
            break
    return [v, move]


def min_value(board, _max, _min):
    move = None
    if terminal(board):
        return [utility(board), None]
    v = float('inf')
    for action in actions(board):
        test = max_value(result(board, action), _max, _min)[0]
        _min = min(_min, test)
        if test < v:
            v = test
            move = action
        if _max >= _min:
            break
    return [v, move]
