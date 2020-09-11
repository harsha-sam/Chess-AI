"""
Chess Player
"""
from movements import *
from point import Point
from copy import deepcopy

class Piece:
    
    Points = {'Pawn': 10, 'Rook': 50, 'Bishop': 30, 'Knight': 30, 'Queen': 90, 'King': 900}

    PIECES_MOVING_DIRECTION = {'Queen': (front, back, right, left, diag_right_backward, diag_right_forward, diag_left_forward, diag_left_backward),
                                'BPawn': (one_step_front, one_step_diag_right_forward, one_step_diag_left_forward),
                                'WPawn': (one_step_back, one_step_diag_right_backward, one_step_diag_left_backward),
                                'Rook': (front, back, right, left),
                                'Knight': (L_front, L_back),
                                'Bishop': (diag_right_forward, diag_right_backward, diag_left_forward, diag_left_backward),
                                'King': (one_step_front, one_step_back, one_step_right, one_step_left, one_step_diag_right_forward, one_step_diag_right_backward, one_step_diag_left_backward, one_step_diag_left_forward)}
                               
    def __init__(self, name, pos, color):
        self.color = color
        self.name = name
        self.pos = Point(pos[0], pos[1])
        self.alive = True

    def actions(self, board):
        """
        Returns set of all possible actions for the piece available on the board.
        """
        name = self.name
        if name == 'Pawn':
            name = self.color + name
        directions = Piece.PIECES_MOVING_DIRECTION[name]
        l = []
        for direction in directions:
            moves_available = direction(board, self.pos, self.color)
            if moves_available:
                l += moves_available
        return l

    def __repr__(self):
        if self.color == 'W':
            return f'{self.name[0].upper()} pos:{self.pos} alive:{self.alive}'
        return f'{self.name[0].lower()} pos:{self.pos} alive:{self.alive}'

    def getPiecePoints(self):
        return Piece.Points[self.name] if self.color == 'W' else - Piece.Points[self.name]


def move(board, piece, new_pos):
    if new_pos in piece.actions(board):
        if board[new_pos.x][new_pos.y] != Game.EMPTY:
            kill(board, board[new_pos.x][new_pos.y])
        if board[new_pos.x][new_pos.y] == Game.EMPTY:
            board[piece.pos.x][piece.pos.y] = Game.EMPTY
            board[new_pos.x][new_pos.y] = piece
            piece.pos.x = new_pos.x
            piece.pos.y = new_pos.y

def kill(board, piece):
    board[piece.pos.x][piece.pos.y] = Game.EMPTY
    piece.alive = False


class Game:
    BLACK = 'B'
    WHITE = 'W'
    EMPTY = '.'
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
    TURN = WHITE

    def __init__(self, player):  
        self.player = player
        if self.player == Game.WHITE:
            self.enemy = Game.BLACK
        else:
            self.enemy = Game.WHITE
        self.board = [[Game.EMPTY for j in range(8)] for i in range(8)]
        self.black_pieces = {}
        self.white_pieces = {}

    def inital_starting_state(self):
        """
        Returns starting state of the board.
        """
        def pieces_insert(board, row, pieces, color):
            for i in range(8):
                name = pieces[i]
                if name != 'King' and name != 'Queen':
                    name = name[:len(name) - 2]
                obj = Piece(name, (row, i), color)
                board[row][i] = obj
                if color == Game.BLACK:
                    self.black_pieces[pieces[i]] = obj
                else:
                    self.white_pieces[pieces[i]] = obj

        # Inserting Black Pawns
        pieces_insert(self.board, 1, Game.PIECES_NAMES[:8], Game.BLACK) 
        # Inserting White Pawns
        pieces_insert(self.board, 6, Game.PIECES_NAMES[:8], Game.WHITE)
        # Inserting Black (Rooks, Bishops, Knight, Queen, King)
        pieces_insert(self.board, 0, Game.PIECES_NAMES[8:], Game.BLACK)
        # Inserting White (Rooks, Bishops, Knight, Queen, King)
        pieces_insert(self.board, 7, Game.PIECES_NAMES[8:], Game.WHITE)
        # Swapping Black king and Queen positions
        self.board[0][3], self.board[0][4] =  self.board[0][4], self.board[0][3]
        self.board[0][3].pos, self.board[0][4].pos = self.board[0][4].pos, self.board[0][3].pos
        return self.board

    def evaluation(self):
        val = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != Game.EMPTY:
                    val += self.board[i][j].getPiecePoints()
        return val


    def player(self):
        """
        Returns player who has the next turn on a board.
        """
        if Game.TURN == Game.WHITE:
            return Game.BLACK
        return Game.WHITE


    def result(self, piece, action):
        """
        Returns the board that results from making move on the board.
        """
        new_board = deepcopy(self.board)
        move(new_board, deepcopy(piece), action)
        return new_board

    def terminal(self):
        pass

    def utility(self):
        pass


def display(state):
    for row in state:
        print(row)
    

# game = Game('W')
# print('Initializing Game !')
# game.inital_starting_state()
# display(game.board)
# print(f"Eval:{game.evaluation()}")
# print('----------------------------------------------')
# print('Black_pieces:')
# print(game.black_pieces)
# print('----------------------------------------------')
# print('White_pieces:')
# print(game.white_pieces)
# print('----------------------------------------------')
# p3 = game.black_pieces['Pawn-3']
# p4 = game.black_pieces['Pawn-4']
# all_actions = p4.actions(game.board)
# print(f'available actions: {all_actions}')
# for actions in all_actions:
#     display(game.result(p4, actions))
#     print('----------------------------------------------')
# print(p4.pos)
# move(game.board, game.black_pieces['Pawn-4'], Point(2, 3))
# print("done")
# display(game.board)
# move(game.board, game.black_pieces['Pawn-3'], Point(2, 3))
# display(game.board)
# move(game.board, game.white_pieces['Pawn-4'], Point(5, 3))
# move(game.board, game.white_pieces['Queen'], Point(2, 3))
# display(game.board)
# print(game.evaluation())