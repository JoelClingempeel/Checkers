import pygame
import copy

pygame.init()
win = pygame.display.set_mode((640, 700))
pygame.display.set_caption("Mr. Bot Plays Checkers")
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 24)
keys = pygame.key.get_pressed()
MAX_DEPTH = 6
MAX_SCORE = 10  # Must be an upper bound on |heuristic|
RED = (255, 0, 0)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
my_board = [[-1, 0, -1, 0, -1, 0, -1, 0], [0, -1, 0, -1, 0, -1, 0, -1], [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1]]


def search(board):
    value = MAX_SCORE
    moves = check_moves(board, -1)
    for move in moves:
        new_value = max_value(move, -1 * MAX_SCORE, MAX_SCORE, 0)
        if new_value < value:
            value = new_value
            best = move
    return best


def min_value(board, alpha, beta, depth):
    if depth == MAX_DEPTH:
        return heuristic(board)
    value = MAX_SCORE
    moves = check_moves(board, -1)
    for move in moves:
        value = min(value, max_value(move, alpha, beta, depth + 1))
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value


def max_value(board, alpha, beta, depth):
    if depth == MAX_DEPTH:
        return heuristic(board)
    value = -1 * MAX_SCORE
    moves = check_moves(board, 1)
    for move in moves:
        value = max(value, min_value(move, alpha, beta, depth + 1))
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value


def check_moves(board, color):
    moves = []
    for i in range(8):
        for j in range(8):
            if board[i][j] * color > 0:
                new_moves = check_piece_moves(board, i, j, color)
                if new_moves == -1:
                    return check_jumps(board, color)
                else:
                    moves += new_moves
    return moves


def check_piece_moves(board, i, j, color):
    moves = []
    if board[i][j] == -2 or color == 1:  # For kings or black pieces
        if i > 0 and j > 0:
            if board[i-1][j-1] == 0:  # Determines if we can move to a given space
                board_copy = copy.deepcopy(board)  # Create a copy on which we carry out this move.
                board_copy[i-1][j-1] = board_copy[i][j]
                board_copy[i][j] = 0
                moves.append(board_copy)
            elif board[i-1][j-1] * color < 0 and i > 1 and j > 1:
                if board[i-2][j-2] == 0:  # Detects a possible jump, and if one occurs, escape from function.
                    return -1
        # More analogous cases follow.
        if i > 0 and j < 7:
            if board[i-1][j+1] == 0:
                board_copy = copy.deepcopy(board)
                board_copy[i - 1][j + 1] = board_copy[i][j]
                board_copy[i][j] = 0
                moves.append(board_copy)
            elif board[i-1][j+1] * color < 0 and i > 1 and j < 6:
                if board[i-2][j+2] == 0:  # Detects a possible jump
                    return -1
    if board[i][j] == 2 or color == -1:  # For kings or red pieces
        if i < 7 and j > 0:
            if board[i + 1][j - 1] == 0:
                board_copy = copy.deepcopy(board)
                board_copy[i + 1][j - 1] = board_copy[i][j]
                board_copy[i][j] = 0
                moves.append(board_copy)
            elif board[i + 1][j - 1] * color < 0 and i < 6 and j > 1:
                if board[i + 2][j - 2] == 0:  # Detects a possible jump
                    return -1
        if i < 7 and j < 7:
            if board[i + 1][j + 1] == 0:
                board_copy = copy.deepcopy(board)
                board_copy[i + 1][j + 1] = board_copy[i][j]
                board_copy[i][j] = 0
                moves.append(board_copy)
            elif board[i + 1][j + 1] * color < 0 and i < 6 and j < 6:
                if board[i + 2][j + 2] == 0:  # Detects a possible jump
                    return -1
    # If a jump was possible, this function would have returned -1 without getting to this point.
    return moves


def check_jumps(board, color):
    moves = []
    for i in range(8):
        for j in range(8):
            if board[i][j] * color > 0:
                new_moves = check_piece_jumps(board, i, j, color, [])
                if new_moves[0] != board:
                    moves += new_moves
    return moves


def check_piece_jumps(board, i, j, color, moves):
    can_jump = False
    if board[i][j] == -2 or color == 1:  # For kings or black pieces
        if i > 1 and j > 1:
            if board[i-1][j-1]*color < 0 and board[i-2][j-2] == 0:  # Check if a jump is possible.
                can_jump = True
                board_copy = copy.deepcopy(board)  # Execute jump on a copied board.
                board_copy[i-2][j-2] = board_copy[i][j]
                board_copy[i][j] = 0
                board_copy[i - 1][j - 1] = 0
                moves = check_piece_jumps(board_copy, i - 2, j - 2, color, moves)
        # Similarly for other directions in which one can jump
        if i > 1 and j < 6:
            if board[i-1][j+1]*color < 0 and board[i-2][j+2] == 0:
                can_jump = True
                board_copy = copy.deepcopy(board)
                board_copy[i - 2][j + 2] = board_copy[i][j]
                board_copy[i][j] = 0
                board_copy[i - 1][j + 1] = 0
                moves = check_piece_jumps(board_copy, i - 2, j + 2, color, moves)
    if board[i][j] == 2 or color == -1:  # For kings or red pieces
        if i < 6 and j > 1:
            if board[i + 1][j - 1]*color < 0 and board[i + 2][j - 2] == 0:
                can_jump = True
                board_copy = copy.deepcopy(board)
                board_copy[i + 2][j - 2] = board_copy[i][j]
                board_copy[i][j] = 0
                board_copy[i + 1][j - 1] = 0
                moves = check_piece_jumps(board_copy, i + 2, j - 2, color, moves)
        if i < 6 and j < 6:
            if board[i + 1][j + 1]*color < 0 and board[i + 2][j + 2] == 0:
                can_jump = True
                board_copy = copy.deepcopy(board)
                board_copy[i + 2][j + 2] = board_copy[i][j]
                board_copy[i][j] = 0
                board_copy[i + 1][j + 1] = 0
                moves = check_piece_jumps(board_copy, i + 2, j + 2, color, moves)
    if not can_jump:  # Reached bottom of recursion for finding iterated jumps
        moves.append(board)
    return moves


def heuristic(board):
    score = 0
    for i in range(8):
        for j in range(8):
            score += board[i][j]
    return score


def kings(board):
    for j in range(8):
        if board[0][j] == 1:
            board[0][j] = 2
    for j in range(8):
        if board[7][j] == -1:
            board[7][j] = -2
    return board


def check_win(board, color):
    game_win = True
    for i in range(8):
        for j in range(8):
            if board[i][j] * color < 0:
                game_win = False
    return game_win


def end(color):
    global done
    while not done:
        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                done = True
        win.fill(CYAN)
        if color == 1:
            win.blit(font.render("Player wins.", True, BLACK), (240, 300))
        else:
            win.blit(font.render("Mr. Bot wins.", True, RED), (240, 300))
        pygame.display.flip()


def draw_board(board, player):
    win.fill(CYAN)
    if player == 1:
        win.blit(font.render("Select a move.", True, BLACK), (240, 0))
    else:
        win.blit(font.render("Opponent has moved.", True, BLACK), (200, 0))
    for k in range(8):
        pygame.draw.line(win, BLACK, (0, 80 * k + 60), (640, 80 * k + 60))
        pygame.draw.line(win, BLACK, (80 * k, 60), (80 * k, 700))
    for i in range(8):
        for j in range(8):
            if board[i][j] < 0:
                pygame.draw.circle(win, RED, (80 * j + 40, 80 * i + 100), 30)
                if board[i][j] == -2:
                    win.blit(font.render("K", True, WHITE), (80 * j + 30, 80 * i + 80))
            if board[i][j] > 0:
                pygame.draw.circle(win, BLACK, (80 * j + 40, 80 * i + 100), 30)
                if board[i][j] == 2:
                    win.blit(font.render("K", True, WHITE), (80 * j + 30, 80 * i + 80))


turn = 1
done = False
index = 0
move_list = check_moves(my_board, 1)
num_moves = len(move_list)
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYUP:
            if turn == 1:  # Black turn (player)
                if event.key == pygame.K_RIGHT:
                    index = (index + 1) % num_moves
                if event.key == pygame.K_LEFT:
                    index = (index - 1) % num_moves
                if event.key == pygame.K_UP:
                    if check_win(move_list[index], 1):
                        end(1)
                    new_board = search(move_list[index]) # Runs AI to make a move
                    if check_win(new_board, -1):
                        end(-1)
                    my_board = kings(new_board)
                    turn = -1
            else:  # Red turn (AI)
                if event.key == pygame.K_SPACE:
                    turn = 1
                    move_list = check_moves(my_board, 1)
                    index = 0
                    num_moves = len(move_list)

    if turn == 1:
        draw_board(move_list[index], turn)
    else:
        draw_board(my_board, turn)
    pygame.display.flip()
