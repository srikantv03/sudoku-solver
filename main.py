import numpy as np

def hasBlanks(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] == 0:
                return True
    return False

def getPuzzle():
    puzzle = list()
    n = int(input())
    for i in range(n):
        row = list(map(int, input().split()))
        puzzle.append(row)
    return puzzle

def getSquare(row, col, puzzle):
    square = list()
    squareSide = int(np.sqrt(len(puzzle)))
    rowSect = int(row/squareSide)
    colSect = int(col/squareSide)
    for i in range(rowSect * squareSide, rowSect * squareSide + squareSide):
        for j in range(colSect * squareSide, colSect * squareSide + squareSide):
            square.append(puzzle[i][j])
    return square

def getRow(row, col, puzzle):
    returnArr = list()
    for i in range(len(puzzle)):
        returnArr.append(puzzle[row][i])
    return returnArr

def getColumn(row, col, puzzle):
    returnArr = list()
    for i in range(len(puzzle)):
        returnArr.append(puzzle[i][col])
    return returnArr


def makeNotes(puzzle):
    nums = range(1, len(puzzle) + 1)
    notes = list()
    for i in range(len(puzzle)):
        notes.append([])
        for j in range(len(puzzle)):
            if (puzzle[i][j] != 0):
                notes[i].append([0])
            else:
                notAllowed = list(set(getSquare(i, j, puzzle) + getRow(i, j, puzzle) + getColumn(i, j, puzzle)))
                notes[i].append(list(np.setdiff1d(nums, notAllowed)))
    return notes

def solve(puzzle):
    amtFixed = 0
    notes = makeNotes(puzzle)
    for i in range(len(notes)):
        for j in range(len(notes)):
            if(len(notes[i][j]) == 1 and notes[i][j][0] != 0):
                amtFixed += 1
                puzzle[i][j] = notes[i][j][0]
    if amtFixed == 0:
        return puzzle
    if hasBlanks(puzzle):
        return(solve(puzzle))
    else:
        return puzzle

def display(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            print(str(puzzle[i][j]), end= " ")
        print('\n')

puzzle = getPuzzle()

display(solve(puzzle))




