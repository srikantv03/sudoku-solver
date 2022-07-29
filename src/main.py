import numpy as np

class SudokuBoard:

    def __init__(self, puzzle: str, image=None):
        for _ in range(len(puzzle)):
            if len(puzzle) != len(puzzle[_]):
                raise Exception("Puzzle is not of square shape")

        self.puzzle = puzzle
        self.image = image
        self.sideLength = len(puzzle)

    def getPuzzle(self) -> list:
        puzzle = list()
        n = int(input())
        for i in range(n):
            row = list(map(int, input().split()))
            puzzle.append(row)
        return puzzle

    def hasBlanks(self) -> bool:
        for i in range(self.sideLength):
            for j in range(self.sideLength):
                if self.puzzle[i][j] == 0:
                    return True
        return False

    def getSquare(self, row: int, col: int):
        square = list()
        squareSide = int(np.sqrt(len(self.puzzle)))
        rowSect = int(row / squareSide)
        colSect = int(col / squareSide)
        for i in range(rowSect * squareSide, rowSect * squareSide + squareSide):
            for j in range(colSect * squareSide, colSect * squareSide + squareSide):
                square.append(self.puzzle[i][j])
        return square

    def getRow(self, row: int, col: int):
        returnArr = list()
        for i in range(self.sideLength):
            returnArr.append(self.puzzle[row][i])
        return returnArr

    def getColumn(self, row: int, col: int):
        returnArr = list()
        for i in range(len(self.puzzle)):
            returnArr.append(self.puzzle[i][col])
        return returnArr

    def makeNotes(self):
        nums = list(range(1, self.sideLength + 1))
        notes = list()
        for i in range(self.sideLength):
            notes.append([])
            for j in range(self.sideLength):
                if (self.puzzle[i][j] != 0):
                    notes[i].append([0])
                else:
                    notAllowed = list(set(self.getSquare(i, j) + self.getRow(i, j) + self.getColumn(i, j)))
                    notes[i].append(list(np.setdiff1d(nums, notAllowed)))
        return notes

    def decipherNotes(self, notes: list):
        amtFixed = 0
        for i in range(self.sideLength):
            for j in range(len(self.puzzle[0])):
                if self.puzzle[i][j] == 0:
                    squareNotes = [j for sub in self.getSquare(i, j) for j in sub]
                    rowNotes = [j for sub in self.getRow(i, j) for j in sub]
                    colNotes = [j for sub in self.getColumn(i, j) for j in sub]

                    for k in range(1, self.sideLength):
                        if squareNotes.count(k) == 1 or rowNotes.count(k) == 1 or colNotes.count(k) == 1:
                            amtFixed += 1
                            self.puzzle[i][j] = k
                            break
        if (amtFixed == 0):
            return None
        return self.puzzle

    def solve(self):
        amtFixed = 0
        notes = self.makeNotes(self.puzzle)
        for i in range(len(notes)):
            for j in range(len(notes)):
                if (len(notes[i][j]) == 1 and notes[i][j][0] != 0):
                    amtFixed += 1
                    self.puzzle[i][j] = notes[i][j][0]
        if amtFixed == 0:
            temp = self.decipherNotes(notes, self.puzzle)
            if temp is not None:
                return self.solve(temp)
            else:
                return self.puzzle
        if self.hasBlanks(self.puzzle):
            return self.solve(self.puzzle)
        else:
            return self.puzzle

    def display(self):
        for i in range(self.sideLength):
            for j in range(self.sideLength):
                print(str(self.puzzle[i][j]), end=" ")
            print('\n')



