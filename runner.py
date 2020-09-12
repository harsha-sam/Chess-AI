from ai import *
import math

def minimize(board, depth, alpha, beta):
    if terminal(board) or depth == 0:
        return None, None, evaluation(board)
    minim = math.inf
    best_move = None
    best_choice =  None
    for actions in all_available_black_moves(board):
        piece = actions[0]
        for mv in actions[1]:
            (_, _, value) = maximize(piece.result(board, mv), depth - 1, alpha, beta)
            beta = min(beta, value)
            if value < minim:
                best_move = mv
                best_choice = piece
                minim = value
            if alpha >= beta:
                break
    return best_choice, best_move, minim


def maximize(board, depth, alpha, beta):
    if terminal(board) or depth == 0:
        return None, None, evaluation(board)
    maxim = -math.inf
    best_move = None
    best_choice =  None
    for actions in all_available_white_moves(board):
        piece = actions[0]
        for mv in actions[1]:
            (_, _, value) = minimize(piece.result(board, mv), depth - 1, alpha, beta)
            alpha = max(alpha, value)
            if value > maxim:
                best_move = mv
                best_choice = piece
                maxim = value
            if alpha >= beta:
                break
    return best_choice, best_move, maxim


def main():
    while True:
        print("Enter your choice:\n 'B' for Black \n 'W' for White")
        player = input("> ")
        if player == 'B' or player == 'W':
            break

    BOARD, PLAYER, ENEMY, PLAYER_PIECES, ENEMY_PIECES = game_init(player)
    print('Initializing Game !')
    display(BOARD)

    n = 0 if PLAYER == 'W' else 1
    while n < 100:
        if n % 2 == 0:
            print(f"Your Turn! ({PLAYER})")
            piece = input("Enter the piece name you wanna move:")
            choice = PLAYER_PIECES[piece] 
            print(f"Available moves for {choice.name}: {choice.actions(BOARD)}")
            x, y = map(int, input("Enter your move:").split())
            move(BOARD, choice, Point(x, y))
            win_check = winner(BOARD)
            if win_check:
                print(f"{win_check} won!")
                break
            display(BOARD)
            print(f"Evaluation:{evaluation(BOARD)}")
        else:
            print(f"Computer's Turn ! ({ENEMY})")
            if ENEMY == BLACK:
                pc, mv, _ = minimize(BOARD, 3, -math.inf, math.inf)
                move(BOARD, pc, mv)
            elif ENEMY == WHITE:
                pc, mv, _ = maximize(BOARD, 3, -math.inf, math.inf)
                move(BOARD, pc, mv)
            win_check = winner(BOARD)
            if win_check:
                print(f"{win_check} won!")
                break
            display(BOARD)
            print(f"Evaluation:{evaluation(BOARD)}")
        n += 1

if __name__ == "__main__":
    main()