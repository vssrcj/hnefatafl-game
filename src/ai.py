import random
import copy

from game_utils import attacker_cell_score, MAX_SCORE


def ai_move(board):
    """ Returns:
            has AI won, origin, destination, captures
    """
    move = get_best_move(board, is_defender=True)

    if move:
        score, origin, destination, captures = move

        return (True if score == MAX_SCORE else False,
                origin, destination, captures)
    else:
        return (True, None, None, None)


def get_best_move(board, is_defender):
    """ Returns:
            score, origin, destination, captures
    """
    check = 2 if is_defender else 1
    pieces = []
    king = None
    for y, row in enumerate(board):
        for x, value in enumerate(row):
            if value == check:
                pieces.append((y, x))
            elif is_defender and value == 3:
                king = (y, x)

    scores = []
    if king:
        move = best_move_per_piece(
            board, origin=king, is_defender=True, is_king=True)

        if move:
            score, destination, captures = move

            if score == MAX_SCORE:
                return score, king, destination, captures
            else:
                scores.append((score, king, destination, captures))

    for piece in pieces:
        move = best_move_per_piece(
            board, origin=piece, is_defender=is_defender, is_king=False)

        if move:
            score, destination, captures = move

            scores.append((score, piece, destination, captures))
    if scores:
        random.shuffle(scores)
        scores.sort(key=lambda x: x[0], reverse=True)

        return scores[0]
    else:
        return None


def best_move_per_piece(board, origin, is_defender, is_king):
    """ Returns:
            score, destination, captures
    """
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    scores = []

    for direction in directions:
        check = copy.deepcopy(origin)
        while True:
            check = (check[0] + direction[0], check[1] + direction[1])

            if board[check] != 0:
                break

            if is_king:
                if king_at_edge(board, cell=check):
                    return (MAX_SCORE, check, [])
                else:
                    scores.append((0, check, []))
            else:
                if is_defender:
                    score, captures = defender_cell_score(board, cell=check)
                    new_board = board.copy()
                    for capture in captures:
                        new_board[capture] = 0
                    new_board[origin] = 0
                    new_board[check] = 2
                    move = get_best_move(board=new_board, is_defender=False)
                    if move:
                        score -= move[0]
                    scores.append((score, check, captures))
                else:
                    score, captures = attacker_cell_score(board, cell=check)
                    scores.append((score, check, []))

    if scores:
        random.shuffle(scores)
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[0]
    else:
        return None


def king_at_edge(board, cell):
    row, column = cell
    if (board[row+1, column] is None or
        board[row-1, column] is None or
        board[row, column+1] is None or
       board[row, column-1] is None):
            return True
    else:
        return False


def defender_cell_score(board, cell):
    """ Returns:
            captures: A list of cells that are captured
            score: The score
    """
    captures = []
    score = 0
    row, column = cell

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
