""""""


def check_move(cell_from, cell_to, board):

    if not valid_move(cell_from, cell_to, board):
        return False
    score, captures = attacker_cell_score(board, cell_to[0], cell_to[1])
    for capture in captures:
        board[capture] = 0
    board[cell_from] = 0
    board[cell_to] = 1
    return True if score >= 10 else None


def valid_move(cell_from, cell_to, board):

    if cell_from[0] == cell_to[0]:      # same row
        if cell_from[1] < cell_to[1]:    # move right
            check = cell_from[1] + 1
            while check <= cell_to[1]:
                if board[cell_from[0], check] != 0:
                    return False
                check += 1
            return True

        if cell_from[1] > cell_to[1]:    # move right
            check = cell_from[1] - 1
            while check >= cell_to[1]:
                if board[cell_from[0], check] != 0:
                    return False
                check -= 1
            return True

    if cell_from[1] == cell_to[1]:      # same row
        if cell_from[0] < cell_to[0]:    # move right
            check = cell_from[0] + 1
            while check <= cell_to[0]:
                if board[check, cell_to[1]] != 0:
                    return False
                check += 1
            return True
        if cell_from[0] > cell_to[0]:    # move right
            check = cell_from[0] - 1
            while check >= cell_to[0]:
                if board[check, cell_to[1]] != 0:
                    return False
                check -= 1
            return True
    return False


def attacker_cell_score(board, y, x):
    """ Returns score, and captures """
    score = 0
    captures = []

    u = board[y-1, x]
    u2 = board[y-2, x] if u is not None else None

    r = board[y, x+1]
    r2 = board[y, x+2] if r is not None else None

    d = board[y+1, x]
    d2 = board[y+2, x] if d is not None else None

    l = board[y, x-1]
    l2 = board[y, x-2] if l is not None else None

    ur = board[y-1, x+1]
    dr = board[y+1, x+1]
    dl = board[y+1, x-1]
    ul = board[y-1, x-1]

    if u == 2 and u2 == 1:
        score += 3
        captures.append((y-1, x))
    if u == 3 and (ul is not None or ul == 1) and \
       (u2 is not None or u2 == 1) and (ur is not None or ur == 1):
        score += 10
        captures.append((y-1, x))

    if r == 2 and r2 == 1:
        score += 3
        captures.append((y, x+1))
    if r == 3 and (ur is not None or ur == 1) and \
       (r2 is not None or r2 == 1) and (dr is not None or dr == 1):
        score += 10
        captures.append((y, x+1))

    if d == 2 and d2 == 1:
        score += 3
        captures.append((y+1, x))
    if d == 3 and (dr is not None or dr == 1) and \
       (d2 is not None or d2 == 1) and (dl is not None or dl == 1):
        score += 10
        captures.append((y+1, x))

    if l == 2 and l2 == 1:
        score += 3
        captures.append((y, x-1))
    if l == 3 and (dl is not None or dl == 1) and \
       (l2 is not None or l2 == 1) and (ul is not None or ul == 2):
        score += 10
        captures.append((y, x-1))
    return score, captures
