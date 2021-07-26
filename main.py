def getPuzzle():
    puzzle = list()
    n = int(input())
    for i in range(n):
        row = list(map(int, input().split()))
        puzzle.append(row)
    return puzzle

# def getSquare(row, col, puzzle):
#
# def getRow(row, col, puzzle):
#
# def getColumn(row, col, puzzle):
#     for i in range(len(puzzle)):


print(getPuzzle())