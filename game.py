"""
Chess Game
"""
from movements import *
from point import Point
from copy import deepcopy


# Strength for pieces on the board
Points = {'Pawn': 10, 'Rook': 50, 'Bishop': 30, 'Knight': 30, 'Queen': 90, 'King': 900}
    
# Directions at which the respective piece can move
PIECES_MOVING_DIRECTION = {'Queen': (front, back, right, left, diag_right_backward, diag_right_forward, diag_left_forward, diag_left_backward),
                            'Pawn': (pawn_rules, ), 
                            'Rook': (front, back, right, left),
                            'Knight': (L_front, L_back),
                            'Bishop': (diag_right_forward, diag_right_backward, diag_left_forward, diag_left_backward),
                            'King': (one_step_front, one_step_back, one_step_right, one_step_left, one_step_diag_right_forward, one_step_diag_right_backward, one_step_diag_left_backward, one_step_diag_left_forward)}
PIECES_NAMES = ['Pawn-1',
                'Pawn-2', 
                'Pawn-3', 
                'Pawn-4',  
                'Pawn-5', 
                'Pawn-6', 
                'Pawn-7', 
                'Pawn-8',
                'Rook-1',
                'Knight-1',
                'Bishop-1',
                'Queen',
                'King',
                'Bishop-2',
                'Knight-2',
                'Rook-2'
                ]
SYMBOLS = {'BPawn': '♟', 'WPawn': '♙', 'BKnight': '♞', 'WKnight':'♘', 'BBishop':'♝', 'WBishop':'♗', 'BRook':'♜', 'WRook':'♖', 'BKing':'♚', 'WKing':'♔', 'BQueen':'♛', 'WQueen':'♕'}
BLACK = 'B' 
WHITE = 'W'
EMPTY = '.'

class Piece:                   
    def __init__(self, name, pos, color): 
        """
        name: Name of the piece ('King', 'Queen', 'Bishop-1', 'Knight-1', 'Rook-2')
        pos: x, y where x denotes the row position and y denotes the column 
        color: 'B' or 'W' which denotes Black and White respectively
        """
        self.color = color 
        self.name = name
        self.num = None
        if name != 'King' and name != 'Queen':
            # num contains the number of piece 1 for Rook-1, 2 for Rook-2....
            self.name = name[:len(name) - 2]
            self.num = name[len(name)-1]
        self.pos = Point(pos[0], pos[1])
        # Init is changed to True, when the piece is initialized (Useful for two-steps in pawn initial move)
        self.init = False
        self.alive = True

    def actions(self, board): 
        """
        Returns set of all possible actions for the piece available on the board.
        """
        if self.alive:
            directions = PIECES_MOVING_DIRECTION[self.name]
            l = []
            for direction in directions:
                if direction == pawn_rules:
                    moves_available = pawn_rules(board, self.pos, self.color, self.init)
                else:
                    moves_available = direction(board, self.pos, self.color)
                if moves_available:
                    l += moves_available
            return l

    def result(self, board, action):
        """
        Returns the board that results from making piece move on the board.
        piece: Piece class Object
        action: Point class object
        """
        new_board = deepcopy(board)
        move(new_board, deepcopy(self), action)
        return new_board

    def __repr__(self): 
        """
        Representation of this class
        """
        return SYMBOLS[self.color + self.name]

    def getPiecePoints(self): 
        """
        Returns strength point for the piece
            • Positive strength if color is white
            • Negative strength if color is black
        """
        return Points[self.name] if self.color == WHITE else - Points[self.name]


def game_init(player): 
    """
    Initializes 8 * 8 board 
    """
    board = [[EMPTY for _ in range(8)] for _ in range(8)]
    if player == WHITE:
        enemy = BLACK
    else:
        enemy = WHITE
    # names are keys and piece object are values for below dictonaries
    # names are represented as Pawn-1, Rook-1, etc
    player_pieces = {}
    enemy_pieces = {}

    def pieces_insert(board, row, pieces, color):
        for i in range(8):
            obj = Piece(pieces[i], (row, i), color)
            board[row][i] = obj
            if color ==  player:
                player_pieces[pieces[i]] = obj
            else:
                enemy_pieces[pieces[i]] = obj

    # Inserting Black Pawns
    pieces_insert(board, 1, PIECES_NAMES[:8], BLACK) 
    # Inserting White Pawns
    pieces_insert(board, 6, PIECES_NAMES[:8], WHITE)
    # Inserting Black (Rooks, Bishops, Knight, Queen, King)
    pieces_insert(board, 0, PIECES_NAMES[8:], BLACK)
    # Inserting White (Rooks, Bishops, Knight, Queen, King)
    pieces_insert(board, 7, PIECES_NAMES[8:], WHITE)
    return (board, player, enemy, player_pieces, enemy_pieces)


def move(board, piece, new_pos): 
    """
    Moves the piece to new position in the board, if move is valid
    piece: Piece Class Object
    new_pos: Point class Object
    """
    if new_pos not in piece.actions(board):
        return False
    x, y = piece.pos.x, piece.pos.y 
    if board[new_pos.x][new_pos.y] != EMPTY:
        kill(board, board[new_pos.x][new_pos.y])
    if board[new_pos.x][new_pos.y] == EMPTY:
        board[piece.pos.x][piece.pos.y] = EMPTY
        board[new_pos.x][new_pos.y] = piece
        piece.pos.x = new_pos.x
        piece.pos.y = new_pos.y
    piece.init = True
    if piece.pos.x == x and piece.pos.y == y:
        return False
    return True

def kill(board, piece): 
    """
    Kills the piece, and frees the position in the board
    piece: Piece Class Object
    """
    board[piece.pos.x][piece.pos.y] = EMPTY # Making the piece pos empty
    piece.alive = False


def evaluation(board): 
    """
    Returns the sum of all the strength points of the pieces in the board
    """
    val = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] != EMPTY:
                val += board[i][j].getPiecePoints()
    return val


def all_available_black_moves(board): 
    """
    Returns available moves for all black pieces in the form of list of tuples,
    where each tuple contains the piece name and the moves available for the piece.
    """
    res = []
    for i in range(8):
        for j in range(8):
            if board[i][j] != EMPTY and board[i][j].color == BLACK:
                all_actions = (board[i][j], board[i][j].actions(board))
                res.append(all_actions)
    return res         


def all_available_white_moves(board): 
    """
    Returns available moves for all white pieces in the form of list of tuples,
    where each tuple contains the piece name and the moves available for the piece.
    """
    res = []
    for i in range(8):
        for j in range(8):
            if board[i][j] != EMPTY and board[i][j].color == WHITE:
                all_actions = (board[i][j], board[i][j].actions(board))
                res.append(all_actions)
    return res        


def terminal(board): 
    """
    Returns true if any king is dead
    """
    count = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] != EMPTY and board[i][j].name == 'King' and board[i][j].alive:
                count += 1
    return count != 2


def winner(board): 
    """
    Returns the winner of the game
    """
    if terminal(board):
        for i in range(8):
            for j in range(8):
                if board[i][j] != EMPTY and board[i][j].name == 'King' and board[i][j].alive:
                        return board[i][j].color
    

def display(state): 
    """
    Prints the board
    """
    print("-"*40)
    for row in state:
        for ele in row:
            print(ele, end=' ')
        print()
    print("-"*40)
    