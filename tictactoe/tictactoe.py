"""
Tic Tac Toe Player
"""

import math

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
    xCount = 0
    oCount = 0

    for row in board:
        for square in row:
            if square == X:
                xCount += 1
            elif square == O:
                oCount += 1

    if xCount > oCount:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == EMPTY:
                actions.add((row, col))
    
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    try:
        new_board = [[EMPTY, EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY]]
        for i in range(len(board)):
            for j in range(len(board)):
                new_board[i][j] = board[i][j]
        
        new_board[action[0]][action[1]] = player(board)
        
        return new_board
    except:
        print('Invalid Action')
        raise IndexError

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]:
        return board[1][1]

    for r in range(len(board)):
        if board[r][0] == board[r][1] == board[r][2]:
            return board[r][0]

        if board[0][r] == board[1][r] == board[2][r]:
            return board[0][r]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    for row in board:
        if EMPTY in row:
            if utility(board) == 0:
                return False
    return True                
                

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0

def minimax(board):
    '''
    Returns the optimal action for the current player on the board.
    '''
    if terminal(board):
        return None
    else:
        move = None
        if player(board) == X:
            v = float('-inf')
            for action in actions(board):
                v_new = minValue(result(board, action))
                if v_new > v:
                    if v_new == 1:
                        return action
                    v = v_new
                    move = action
        else:
            v = float('inf')
            for action in actions(board):
                v_new = maxValue(result(board, action))
                if v_new < v:
                    if v_new == -1:
                        return action
                    v = v_new
                    move = action
        return move

def maxValue(board):
    '''
    maximize the value v
    '''
    if terminal(board):
        return utility(board)

    v = float('-inf')

    for action in actions(board):
        v = max(v, minValue(result(board, action)))            

    return v    

def minValue(board):
    '''
    minimize the value v
    '''
    if terminal(board):
        return utility(board)

    v = float('inf')

    for action in actions(board):
        v = min(v, maxValue(result(board, action)))            

    return v