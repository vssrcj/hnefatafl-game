MAX_SCORE = 999


def is_surrounded(u, r, d, l):
    friend_side = False
    sides_surrounded = 0

    for x in (u, r, d, l):
        if x == 1:
            sides_surrounded += 1
        elif x == 2 and not friend_side:
            sides_surrounded += 1
            friend_side = True

    return sides_surrounded == 4


def attacker_cell_score(board, cell):
    """ Returns:
            score, captures
    """
    y, x = cell
    capture_king = False
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
    if u == 3:
        if is_surrounded(u2, ur, 1, ul):
            capture_king = True
            captures.append((y-1, x))

    if r == 2 and r2 == 1:
        score += 3
        captures.append((y, x+1))
    if r == 3:
        if is_surrounded(ur, r2, dr, 1):
            capture_king = True
            captures.append((y, x+1))

    if d == 2 and d2 == 1:
        score += 3
        captures.append((y+1, x))
    if d == 3:
        if is_surrounded(1, dr, d2, dl):
            capture_king = True
            captures.append((y+1, x))

    if l == 2 and l2 == 1:
        score += 3
        captures.append((y, x-1))
    if l == 3:
        if is_surrounded(ul, 1, dl, l2):
            capture_king = True
            captures.append((y, x-1))

    return MAX_SCORE if capture_king else score, captures
