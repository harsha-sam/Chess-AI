"""
Chess Game
"""
from movements import *
from point import Point
from copy import deepcopy

class Piece:
    
    # Strength for pieces on the board
    Points = {'Pawn': 10, 'Rook': 50, 'Bishop': 30, 'Knight': 30, 'Queen': 90, 'King': 900}

    # Directions at which the respective piece can move
    PIECES_MOVING_DIRECTION = {'Queen': (front, back, right, left, diag_right_backward, diag_right_forward, diag_left_forward, diag_left_backward),
                                'Pawn': (pawn_rules, ), 
                                'Rook': (front, back, right, left),
                                'Knight': (L_front, L_back),
                                'Bishop': (diag_right_forward, diag_right_backward, diag_left_forward, diag_left_backward),
                                'King': (one_step_front, one_step_back, one_step_right, one_step_left, one_step_diag_right_forward, one_step_diag_right_backward, one_step_diag_left_backward, one_step_diag_left_forward)}
                               
    def __init__(self, name, pos, color):
        """
        name: Name of the piece ('King', 'Queen', 'Bishop', 'Knight', 'Rook')
        pos: x, y where x denotes the row position and y denotes the column 
        color: 'B' or 'W' which denotes Black and White respectively
        """
        self.color = color
        self.name = name
        self.pos = Point(pos[0], pos[1])
        self.alive = True

    def actions(self, board):
        """
        Returns set of all possible actions for the piece available on the board.
        """
        directions = Piece.PIECES_MOVING_DIRECTION[self.name]
        l = []
        for direction in directions:
            print(direction)
            moves_available = direction(board, self.pos, self.color)
            if moves_available:
                l += moves_available
        return l

    def __repr__(self):
        """
        Representation of this class
        """
        if self.color == 'W':
            return f'{self.name[0].upper()}'
        return f'{self.name[0].lower()}'

    def getPiecePoints(self):
        """
        Returns strength point for the piece
            • Positive strength if color is white
            • Negative strength if color is black
        """
        return Piece.Points[self.name] if self.color == 'W' else - Piece.Points[self.name]


class Game:
    # Class Variables
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
        self.player_pieces = {}
        self.enemy_pieces = {}

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
                if color ==  self.player:
                    self.player_pieces[pieces[i]] = obj
                else:
                    self.enemy_pieces[pieces[i]] = obj

        # Inserting Black Pawns
        pieces_insert(self.board, 1, Game.PIECES_NAMES[:8], Game.BLACK) 
        # Inserting White Pawns
        pieces_insert(self.board, 6, Game.PIECES_NAMES[:8], Game.WHITE)
        # Inserting Black (Rooks, Bishops, Knight, Queen, King)
        pieces_insert(self.board, 0, Game.PIECES_NAMES[8:], Game.BLACK)
        # Inserting White (Rooks, Bishops, Knight, Queen, King)
        pieces_insert(self.board, 7, Game.PIECES_NAMES[8:], Game.WHITE)
        return self.board

    def evaluation(self):
        """
        Returns the sum of all the strength points of the pieces in the board
        """
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
        Returns the board that results from making piece move on the board.
        piece: Piece class Object
        action: Point class object
        """
        new_board = deepcopy(self.board)
        move(new_board, deepcopy(piece), action)
        return new_board

    def terminal(self):
        if not self.enemy_pieces['King'].alive:
            return f'You ({self.player}) Won !'
        if not self.player_pieces['King'].alive:
            return f'Computer ({self.enemy}) Won !'

  
def move(board, piece, new_pos):
    """
    Moves the piece to new position in the board, if move is valid
    piece: Piece Class Object
    new_pos: Point class Object
    """
    if new_pos in piece.actions(board):
        if board[new_pos.x][new_pos.y] != Game.EMPTY:
            kill(board, board[new_pos.x][new_pos.y])
        if board[new_pos.x][new_pos.y] == Game.EMPTY:
            board[piece.pos.x][piece.pos.y] = Game.EMPTY
            board[new_pos.x][new_pos.y] = piece
            piece.pos.x = new_pos.x
            piece.pos.y = new_pos.y
    else:
        print("Invalid Move")


def kill(board, piece):
    """
    Kills the piece, and frees the position in the board
    board: board attribute from Game class
    piece: Piece Class Object
    """
    print(f"Killing {piece.name} at {piece.pos}")
    board[piece.pos.x][piece.pos.y] = Game.EMPTY # Making the piece pos empty
    piece.alive = False
    print("Done !")

    
def display(state):
    for row in state:
        for ele in row:
            print(ele, end=' ')
        print()
    
def main():
    while True:
        print("Enter your choice:\n 'B' for Black \n 'W' for White")
        human = input("> ")
        if human == 'B' or human == 'W':
            break

    AI = 'B' if human == 'W' else 'W'

    game = Game(human)
    print('Initializing Game !')
    game.inital_starting_state()
    display(game.board)
    n = 0 if human == 'W' else 1
    while n < 100:
        if n % 2 == 0:
            print(f"Your Turn! ({human})")
            game.TURN = human
            piece = input("Enter the piece name you wanna move:")
            choice = game.player_pieces[piece] 
            print(f"Available moves for {choice.name}: {choice.actions(game.board)}")
            x, y= map(int, input("Enter your move:").split())
            move(game.board, choice, Point(x, y))
            display(game.board)
            print(f"Evaluation:{game.evaluation()}")
        else:
            print(f"Computer's Turn ! ({AI})")
            game.TURN = AI
            piece = input("Enter the piece name you wanna move:")
            choice = game.enemy_pieces[piece]
            print(f"Available moves for {choice.name}: {choice.actions(game.board)}")
            x, y= map(int, input("Enter your move:").split())
            move(game.board, choice, Point(x, y))
            display(game.board)
            print(f"Evaluation:{game.evaluation()}")
        n += 1

if __name__ == "__main__":
    main()
