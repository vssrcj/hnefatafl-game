# from transport_models import ReturnMessage

import random

from game_checks import attacker_cell_score


def get_result(board):
    move = get_best_move(board, True)

    if move:
        score = move[0]
        from_cell = move[1]
        to_cell = move[2]
        captures = move[3]
        if captures:
            for cell in captures:
                board[cell] = 0
        from_value = board[from_cell]
        board[from_cell] = 0
        board[to_cell] = from_value
        return (move[1], move[2], move[3], 0)
    else:
        return (None, None, None, 3)


def get_best_move(board, defender):
    """ score, from cell, to cell, captures """
    check = 2 if defender else 1
    pieces = []
    king = None
    for y, row in enumerate(board):
        for x, value in enumerate(row):
            if value == check:
                pieces.append((y, x))
            elif defender and value == 3:
                king = (y, x)

    scores = []
    if king:
        move = best_move_per_piece(board, king, True, True)

        if move and move[0] == 10:
            return (-1, king, move[1], None)
        elif move:
            scores.append((move[0], king, move[1], None))

    for piece in pieces:
        move = best_move_per_piece(board, piece, defender, False)

        if move:
            scores.append((move[0], piece, move[1], move[2]))

    if scores:
        random.shuffle(scores)
        scores.sort(key=lambda x: x[0], reverse=True)

        return scores[0]
    else:
        return None


def best_move_per_piece(board, from_cell, defender, king):
    """ score, to cell, captures """
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    scores = []
    for direction in directions:
        to_y = from_cell[0] + direction[0]
        to_x = from_cell[1] + direction[1]
        value = board[to_y, to_x]
        while value == 0:
            if king:
                if king_at_edge(board, to_y, to_x):
                    return (10, (to_y, to_x), None)
                else:
                    scores.append((0, (to_y, to_x), None))
            else:
                if defender:
                    score, captures = defender_cell_score(board, to_y, to_x)
                    new_board = board.copy()
                    for yt, rowt in enumerate(captures):
                        for xt in rowt:
                            new_board[yt, xt] = 0
                    new_board[from_cell] = 0
                    new_board[to_y, to_x] = 2
                    move = get_best_move(new_board, False)
                    if move:
                        score -= move[0]
                    scores.append((score, (to_y, to_x), captures))
                else:
                    score, captures = attacker_cell_score(board, to_y, to_x)
                    scores.append((score, (to_y, to_x), None))
            to_y += direction[0]
            to_x += direction[1]
            value = board[to_y, to_x]

    if scores:
        random.shuffle(scores)
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[0]
    else:
        return None


def king_at_edge(board, row, column):
    if (row == 0 or column == 0 or
            board.max == row-1 or board.row_length(row) == column-1):
        return True
    else:
        return False


def defender_cell_score(board, row, column):
    """ Get the score

    Returns:
            captures: A list of cells that are captured
            score: The score
     """
    captures = []
    score = 0

    if board[row-1, column] == 1 and board[row-2, column] == 2:
        score += 2
        captures.append((row-1, column))
    if board[row, column+1] == 1 and board[row, column+2] == 2:
        score += 2
        captures.append((row, column+1))
    if board[row+1, column] == 1 and board[row+2, column] == 2:
        score += 2
        captures.append((row+1, column))
    if board[row, column-1] == 1 and board[row, column-2] == 2:
        score += 2
        captures.append((row, column-1))

    return score, captures
