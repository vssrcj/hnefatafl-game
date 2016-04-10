# from transport_models import ReturnMessage

import random
import copy
from game_checks import get_board_value, attacker_piece_score


def get_result(board):
    move = get_best_move(board, True)

    if move:
        print move
        score = move[0]
        from_cell = move[1]
        to_cell = move[2]
        captures = move[3]
        result = score == -1
        if captures:
            for cell in captures:
                board[cell[0]][cell[1]] = 0
        from_value = board[from_cell[0]][from_cell[1]]
        board[from_cell[0]][from_cell[1]] = 0
        board[to_cell[0]][to_cell[1]] = from_value
        return result
    else:
        return True


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
        move = best_move_per_piece(board, king[0], king[1], True, True)

        if move and move[0] == 10:
            return (-1, king, move[1], None)
        elif move:
            scores.append((move[0], king, move[1], None))

    for piece in pieces:
        move = best_move_per_piece(board, piece[0], piece[1], defender, False)

        if move:
            scores.append((move[0], piece, move[1], move[2]))
    print pieces
    if scores:
        random.shuffle(scores)
        scores.sort(key=lambda x: x[0], reverse=True)

        return scores[0]
    else:
        return None


def best_move_per_piece(board, row, column, defender, king):
    """ score, to cell, captures """
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    scores = []
    for direction in directions:
        y = row + direction[0]
        x = column + direction[1]
        value = get_board_value(board, y, x)
        while value == 0:
            if king:
                if king_at_edge(board, y, x):
                    return (10, (y, x), None)
                else:
                    scores.append((0, (y, x), None))
            else:
                if defender:
                    score, captures = defender_piece_score(board, y, x)
                    new_board = copy.deepcopy(board)
                    for yt, rowt in enumerate(captures):
                        for xt in rowt:
                            new_board[yt][xt] = 0
                    new_board[y][x] = 0
                    new_board[y][x] = 2
                    #move = get_best_move(new_board, False)
                    #if move:
                    #    score -= move[0]
                    scores.append((score, (y, x), captures))
                else:
                    score, captures = attacker_piece_score(board, y, x)
                    scores.append((score, (y, x), None))
            y += direction[0]
            x += direction[1]
            value = get_board_value(board, y, x)

    if scores:
        random.shuffle(scores)
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[0]
    else:
        return None


def king_at_edge(board, row, column):
    if (row == 0 or column == 0 or
            len(board) == row-1 or len(board[row]) == column-1):
        return True
    else:
        return False


def defender_piece_score(board, row, column):
    """ Get the score

    Returns:
            captures: A list of cells that are captured
            score: The score
     """
    captures = []
    score = 0

    if (get_board_value(board, row-1, column) == 1 and
            get_board_value(board, row-2, column) == 2):
        score += 2
        captures.append((row-1, column))
    if (get_board_value(board, row, column+1) == 1 and
            get_board_value(board, row, column+2) == 2):
        score += 2
        captures.append((row, column+1))
    if (get_board_value(board, row+1, column) == 1 and
            get_board_value(board, row+2, column) == 2):
        score += 2
        captures.append((row+1, column))
    if (get_board_value(board, row, column-1) == 1 and
            get_board_value(board, row, column-2) == 2):
        score += 2
        captures.append((row, column-1))

    return score, captures
