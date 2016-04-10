""""""


def check_move(cell_from, cell_to, board):

    if not valid_move(cell_from, cell_to, board):

        return False
    score, captures = attacker_piece_score(board, cell_to[0], cell_to[1])
    for capture in captures:
        board[capture[0]][capture[1]] = 0
    board[cell_from[0]][cell_from[1]] = 0
    board[cell_to[0]][cell_to[1]] = 1
    return True if score >= 10 else None


def valid_move(cell_from, cell_to, board):
    if cell_from[0] == cell_to[0]:      # same row
        if cell_from[1] < cell_to[1]:    # move right
            check = cell_from[1] + 1
            while check <= cell_to[1]:
                if board[cell_from[0]][check] != 0:
                    return False
                check += 1
            return True

        if cell_from[1] > cell_to[1]:    # move right
            check = cell_from[1] - 1
            while check >= cell_to[1]:
                if board[cell_from[0]][check] != 0:
                    return False
                check -= 1
            return True

    if cell_from[1] == cell_to[1]:      # same row
        if cell_from[0] < cell_to[0]:    # move right
            check = cell_from[0] + 1
            while check <= cell_to[0]:
                if board[check][cell_to[1]] != 0:
                    return False
                check += 1
            return True
        if cell_from[0] > cell_to[0]:    # move right
            check = cell_from[0] - 1
            while check >= cell_to[0]:
                if board[check][cell_to[1]] != 0:
                    return False
                check -= 1
            return True
    return False


def get_board_value(board, row, column=None):
    if column is not None:
        y = row
        x = column
    else:
        y = row[0]
        x = row[1]
    if y < 0 or len(board) <= y or len(board[y]) <= x or x < 0:
        return None
    else:
        return board[y][x]


def attacker_piece_score(board, row, column):
    """ Returns score, and captures """
    score = 0
    captures = []

    top = get_board_value(board, row-1, column)
    if top is not None:
        top_2 = get_board_value(board, row-2, column)

    right = get_board_value(board, row, column+1)
    if right is not None:
        right_2 = get_board_value(board, row, column+2)

    bottom = get_board_value(board, row+1, column)
    if bottom is not None:
        bottom_2 = get_board_value(board, row+2, column)

    left = get_board_value(board, row, column-1)
    if left is not None:
        left_2 = get_board_value(board, row, column-2)

    top_right = get_board_value(board, row-1, column+1)

    bottom_right = get_board_value(board, row+1, column+1)

    bottom_left = get_board_value(board, row+1, column-1)

    top_left = get_board_value(board, row-1, column-1)

    if top == 2 and top_2 == 1:
        score += 3
        captures.append((row-1, column))
    if (top == 3 and
            (top_left is not None or top_left == 1) and
            (top_2 is not None or top_2 == 1) and
            (top_right is not None or top_right == 1)):
        score += 10
        captures.append((row-1, column))

    if right == 2 and right_2 == 1:
        score += 3
        captures.append((row, column+1))
    if (right == 3 and
            (top_right is not None or top_right == 1) and
            (right_2 is not None or right_2 == 1) and
            (bottom_right is not None or bottom_right == 1)):
        score += 10
        captures.append((row, column+1))

    if bottom == 2 and bottom_2 == 1:
        score += 3
        captures.append((row+1, column))
    if (bottom == 3 and
            (bottom_right is not None or bottom_right == 1) and
            (bottom_2 is not None or bottom_2 == 1) and
            (bottom_left is not None or bottom_left == 1)):
        score += 10
        captures.append((row+1, column))

    if left == 2 and left_2 == 1:
        score += 3
        captures.append((row, column-1))
    if (left == 3 and bottom_left == 1 and left_2 == 1 and
            top_left == 1):
        score += 10
        captures.append((row, column-1))
    return score, captures
