class SudokuPuzzle:
    puzzlewidth = 9
    puzzleheight = 9
    puzzlesize = puzzlewidth * puzzleheight
    puzzle = []

    def __init__(self, puzzlestring):
        for cell in puzzlestring:
            if cell == '0' or cell == '':
                self.puzzle.append(0)
            else:
                self.puzzle.append(int(cell))

    def updatepuzzle(self, puzzlestring):
        self.puzzle = []
        for cell in puzzlestring:
            if cell == '0' or cell == '':
                self.puzzle.append(0)
            else:
                self.puzzle.append(int(cell))

    def getrowindexes(self, index):
        """
        given an index, return a list of all indexes in that row.
        """
        row = []
        rowcall = index // self.puzzlewidth

        for i in range(9):
            row.append(self.puzzlewidth * rowcall + i)
        return row

    def getrowvalues(self, index):
        """
        given an index and a puzzle to work with, return every value that exists on that row in that puzzle
        """
        row = []
        rowcall = index // self.puzzlewidth

        for i in range(9):
            row.append(self.puzzle[rowcall * self.puzzlewidth + i])
        return row

    def getcolumnindexes(self, index):
        column = []
        colcall = index % self.puzzlewidth

        for i in range(9):
            column.append(colcall + i * self.puzzlewidth)
        return column

    def getcolumnvalues(self, index):
        column = []
        colcall = index % self.puzzlewidth

        for i in range(9):
            column.append(self.puzzle[colcall + i * self.puzzlewidth])
        return column

    def getboxindexes(self, index):
        # a box being the 9 x 9 configuration in puzzles. ninette, square, box, whatever name you want.
        box = []
        boxrow = (index // self.puzzlewidth) // 3
        boxcolumn = (index % self.puzzlewidth) // 3

        for i in range(81):
            if (i // self.puzzlewidth) // 3 == boxrow and (i % self.puzzlewidth) // 3 == boxcolumn:
                box.append(i)
        return box

    def getboxvalues(self, index):
        # what a simple bit of that that i just flat out couldnt come up with.
        # so the bit inside the parenthesis is to get either the row or column.
        # divide each by 3 to deal with having the boxes being 3 by 3

        box = []
        boxrow = (index // self.puzzlewidth) // 3
        boxcolumn = (index % self.puzzlewidth) // 3
        for i in range(81):
            if (i // self.puzzlewidth) // 3 == boxrow and (i % self.puzzlewidth) // 3 == boxcolumn:
                box.append(self.puzzle[i])
        return box

    def findpossiblevalues(self, index):
        """
        for a given index, in a puzzle,
        find what could possibly go there based on what exists in the row/column/box of the cell
        """
        possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(1, 10):
            if i in self.getboxvalues(index) or i in self.getcolumnvalues(index) or i in self.getrowvalues(index):
                possibles.remove(i)
        return possibles

    def validatepuzzle(self):
        """
        make sure the puzzle is correct.
        everything filled in, no repeated values (really just no repeated values accomplishes both goals)
        """
        for i in range(81):
            row = self.getrowvalues(i)
            column = self.getcolumnvalues(i)
            box = self.getboxvalues(i)

            # convert each to a set and compare lengths.
            # since sets don't have repeats, this will point out if any conflicts exist
            if len(row) != len(set(row)) or len(column) != len(set(column)) or len(box) != len(set(box)):
                return False
            return True

    def makeallguesses(self, level):
        """
        expect results to be reported as booleans in order to keep track of how many numbers are found
        to only solve with certain levels of algorithm, fill optional parameter "level".
        options are 'easy', 'medium', or 'medium_easy' to combine techniques.
        """
        simplecellsfound = 0
        singleinferencecellsfound = 0

        while True:
            holdingpuzzle = self.puzzle[:]

            if level == 'easy':
                if self.simpleguess(self.puzzle):
                    simplecellsfound += 1

            if level == 'medium_easy':
                if self.simpleguess(self.puzzle):
                    simplecellsfound += 1
                if self.singleinferenceguess(self.puzzle):
                    singleinferencecellsfound += 1

            if level == "medium":
                if self.singleinferenceguess(self.puzzle):
                    singleinferencecellsfound += 1

            if holdingpuzzle == self.puzzle:
                return "SimpleGuesses: " + str(simplecellsfound) + "\n" + "SingleInferenceGuesses: " + str(
                    singleinferencecellsfound)

    def simpleguess(self):
        """
        makes guesses by just seeing if any cells have only 1 possibility
        just makes use of the 'findpossiblevalues' function really
        """
        for i in range(81):
            if len(self.findpossiblevalues(i)) == 1 and self.puzzle[i] == 0:
                self.puzzle[i] = self.findpossiblevalues(i)[0]
                return True
        return False

    def singleinferenceguess(self):
        """
        tries to fill in values based on a cell being the only one in a box/row/column that can actually have a value
        (only one cell has a particular possible value in a group)

        man this code is gross and long. and who really knows if it works? Update: totally works
        """

        for i in range(81):
            # all items in the row/col/box that are 0 (modified in the next section to make this the case)
            row = self.getrowindexes(i)
            column = self.getcolumnindexes(i)
            box = self.getboxindexes(i)

            # makes each list above only contain indexes of cells with no value in them (0)
            itercol = column[:]
            for index in itercol:
                if self.puzzle[index] != 0:
                    column.remove(index)

            iterbox = box[:]
            for index in iterbox:
                if self.puzzle[index] != 0:
                    box.remove(index)

            iterrow = row[:]
            for index in iterrow:
                if self.puzzle[index] != 0:
                    row.remove(index)
            ###

            # prepare lists that contain all values that each cell in the row/col/box could possibly be
            possiblerowvalues = []
            for index in row:
                possiblerowvalues.append(self.findpossiblevalues(index))

            possiblecolumnvalues = []
            for index in column:
                possiblecolumnvalues.append(self.findpossiblevalues(index))

            possibleboxvalues = []
            for index in box:
                possibleboxvalues.append(self.findpossiblevalues(index))

            # turn all the 2D lists into 1D
            possiblerowvalues = [x for sublist in possiblerowvalues for x in sublist]
            possiblecolumnvalues = [x for sublist in possiblecolumnvalues for x in sublist]
            possibleboxvalues = [x for sublist in possibleboxvalues for x in sublist]

            ###

            for value in self.findpossiblevalues(i):
                if possiblerowvalues.count(value) == 1 and self.puzzle[i] == 0:
                    self.puzzle[i] = value
                    return True
                if possiblecolumnvalues.count(value) == 1 and self.puzzle[i] == 0:
                    self.puzzle[i] = value
                    return True
                if possibleboxvalues.count(value) == 1 and self.puzzle[i] == 0:
                    self.puzzle[i] = value
                    return True
        return False

