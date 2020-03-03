import numpy as np
import pandas as pd

column_list = [str(j) for j in range(1, 33)] + ['Winner']


def num_to_grid(num):
    row = (num - 1) // 4
    num -= 4*row
    if row % 2 == 0:
        col = 2*num - 1
    else:
        col = 2*(num - 1)
    return row, col


def grid_to_num(row, col):
    return 4*row + col//2 + 1


def find_jumped_spot(start, end):
    row1, col1 = num_to_grid(start)
    row2, col2 = num_to_grid(end)
    row3 = row1 + (row2 - row1)//2
    col3 = col1 + (col2 - col1)//2
    return grid_to_num(row3, col3)


def maybe_useful(board, turn, winner):
    if turn == -1:
        board = board[::-1]
        for k in range(32):
            board[k] = -1 * board[k]
        return board + [-1 * winner]
    else:
       return board + [winner]


def parse_game(move_list, winner):
    global column_list
    board_list = []
    turn = 1
    board = [1 for i in range(12)] + [0 for j in range(8)] + [-1 for k in range(12)]
    for move in move_list:
        if '.' in move:  # Not a move - just numbering
            continue
        if '-' in move:  # Regular move
            move = move.replace('-', ' ').split()
            for i in range(2):
                move[i] = int(move[i])
            board[move[1] - 1] = board[move[0] - 1] # This and the next line move the piece.
            board[move[0] - 1] = 0
            if (move[1] >= 29 and board[move[1] - 1] == 1) or (move[1] <= 4 and board[move[1] - 1] == -1):
                board[move[1] - 1] *= 2  # Piece has been kinged.
            board_list.append(board + [winner])
            # show_board(board)
            turn *= -1
        else:  # Jump
            move = move.replace('x', ' ').split()
            for i in range(len(move)):
                move[i] = int(move[i])
            for j in range(len(move) - 1):  # Remove jumped pieces.
                board[find_jumped_spot(move[j], move[j + 1]) - 1] = 0
            board[move[len(move) - 1] - 1] = board[move[0] - 1]  # This and the next line move the piece.
            board[move[0] - 1] = 0
            if (move[len(move) - 1] >= 29 and board[move[len(move) - 1] - 1] == 1) or \
                    (move[len(move) - 1] <= 4 and board[move[len(move) - 1] - 1] == -1):
                board[move[len(move) - 1] - 1] *= 2  # Piece has been kinged.
            board_list.append(board + [winner])
            # show_board(board)
            turn *= -1
    # show_board(board)
    # If we flip around every other board, do that here.
    game_df = pd.DataFrame(board_list, columns=column_list)
    return game_df


output_df = pd.DataFrame([], columns=column_list)
raw_data = open('checkers_games_raw.txt')
moves = ""
for line in raw_data:
    if line[0] == '[':
        if moves == "":
            continue
        elif '{' in moves:
            moves = ""
            continue
        else:
            moves = moves.replace('\n', ' ').split()
            outcome = moves.pop()
            outcome = outcome.replace('-', ' ').split()[0]
            if outcome != '1/2':
                output_df = output_df.append(parse_game(moves, 2*int(outcome) - 1))
            moves = ""
        continue
    moves += line
raw_data.close()
output_df.to_csv('checkers_games_processed.csv')