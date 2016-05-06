from ai.main import get_result

board=[[0 for x in range(9)] for x in range(9)];

for y in range(9):
    for x in range(9):
        if ((y in (0, 8) and x in (3, 4, 5)) or
                (x in (0, 8) and y in (3, 4, 5)) or
                (x == 4 and y in (1, 7)) or
                (y == 4 and x in (1, 7))):
                board[y][x] = 1
        elif ((x == 4 and y in (2, 3, 5, 6)) or
                (y == 4 and x in (2, 3, 5, 6))):
                board[y][x] = 2
        elif x == 4 and y == 4:
            board[4][4] = 3

score = get_result(board)
print board