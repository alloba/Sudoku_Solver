import tkinter

# These variables are almost pointless, to the point that they shouldn't be here, but this helps my sanity
puzzlewidth = 9
puzzleheight = 9
puzzlesize = puzzlewidth * puzzleheight
puzzle = []


def displaypuzzle(puzzlelist):
    displaystring = '---------------------------------\n'
    y = 0
    x = 0
    z = 0
    for i in range(81):
        if x == 0:
            displaystring += '|'

        displaystring += " " + str(puzzlelist[i]) + " "
        x += 1
        y += 1
        z += 1

        if x > 2:
            displaystring += '|'
            x = 0
        if y > 8:
            displaystring += '\n'
            y = 0
        if z > 26:
            displaystring += '---------------------------------\n'
            z = 0
    print(displaystring[
          :-1])  # get rid of the last character, which is a newline. its just to make it look nicer when printing


def gatherinput(filename):
    """
     take input from a file, with directory specified as a parameter.
     ideally, correct format should be "[num][space][num][space].....[num][newline] * 9"

    """

    file = open(filename)
    puzzlein = file.read()
    listify = puzzlein.replace('\t', ',').replace('\n', ',').replace(' ', ',').split(',')

    return formatpuzzlestring(listify)


def formatpuzzlestring(stringlist):


    processedpuzzle = []
    for cell in stringlist:
        if cell == '0' or cell == '':
            processedpuzzle.append(0)
        else:
            processedpuzzle.append(int(cell))
    return processedpuzzle

def getrowindexes(index):
    """
    given an index, return a list of all indexes in that row.
    """
    row = []
    rowcall = index // puzzlewidth

    for i in range(9):
        row.append(puzzlewidth * rowcall + i)
    return row


def getrowvalues(index):
    """
    given an index and a puzzle to work with, return every value that exists on that row in that puzzle
    """
    row = []
    rowcall = index // puzzlewidth

    for i in range(9):
        row.append(puzzle[rowcall * puzzlewidth + i])
    return row


def getcolumnindexes(index):
    column = []
    colcall = index % puzzlewidth

    for i in range(9):
        column.append(colcall + i * puzzlewidth)
    return column


def getcolumnvalues(index):
    column = []
    colcall = index % puzzlewidth

    for i in range(9):
        column.append(puzzle[colcall + i * puzzlewidth])
    return column


def getboxindexes(index):
    # a box being the 9 x 9 configuration in puzzles. ninette, square, box, whatever name you want.
    box = []
    boxrow = (index // puzzlewidth) // 3
    boxcolumn = (index % puzzlewidth) // 3

    for i in range(81):
        if (i // puzzlewidth) // 3 == boxrow and (i % puzzlewidth) // 3 == boxcolumn:
            box.append(i)
    return box


def getboxvalues(index):
    # what a simple bit of that that i just flat out couldnt come up with.
    # so the bit inside the parenthesis is to get either the row or column.
    # divide each by 3 to deal with having the boxes being 3 by 3

    box = []
    boxrow = (index // puzzlewidth) // 3
    boxcolumn = (index % puzzlewidth) // 3

    for i in range(81):
        if (i // puzzlewidth) // 3 == boxrow and (i % puzzlewidth) // 3 == boxcolumn:
            box.append(puzzle[i])
    return box


def findpossiblevalues(index):
    """
    for a given index, in a puzzle,
    find what could possibly go there based on what exists in the row/column/box of the cell
    """
    possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(1, 10):
        if i in getboxvalues(index) or i in getcolumnvalues(index) or i in getrowvalues(index):
            possibles.remove(i)
    return possibles


def validatepuzzle():
    """
    make sure the puzzle is correct.
    everything filled in, no repeated values (really just no repeated values accomplishes both goals)
    """
    for i in range(81):
        row = getrowvalues(i)
        column = getcolumnvalues(i)
        box = getboxvalues(i)

        # convert each to a set and compare lengths.
        # since sets don't have repeats, this will point out if any conflicts exist
        if len(row) != len(set(row)) or len(column) != len(set(column)) or len(box) != len(set(box)):
            return False
        return True


def makeallguesses(level):
    """
    expect results to be reported as booleans in order to keep track of how many numbers are found
    to only solve with certain levels of algorithm, fill optional parameter "level".
    options are 'easy', 'medium', or 'medium_easy' to combine techniques.
    """
    simplecellsfound = 0
    singleinferencecellsfound = 0

    while True:
        holdingpuzzle = puzzle[:]

        if level == 'easy':
            if simpleguess(puzzle):
                simplecellsfound += 1

        if level == 'medium_easy':
            if simpleguess(puzzle):
                simplecellsfound += 1
            if singleinferenceguess(puzzle):
                singleinferencecellsfound += 1

        if level == "medium":
            if singleinferenceguess(puzzle):
                singleinferencecellsfound += 1

        if holdingpuzzle == puzzle:
            return "SimpleGuesses: " + str(simplecellsfound) + "\n" + "SingleInferenceGuesses: " + str(
                singleinferencecellsfound)


def simpleguess():
    """
    makes guesses by just seeing if any cells have only 1 possibility
    just makes use of the 'findpossiblevalues' function really
    """
    for i in range(81):
        if len(findpossiblevalues(i)) == 1 and puzzle[i] == 0:
            puzzle[i] = findpossiblevalues(i)[0]
            return True
    return False


def singleinferenceguess():
    """
    tries to fill in values based on a cell being the only one in a box/row/column that can actually have a value
    (only one cell has a particular possible value in a group)

    man this code is gross and long. and who really knows if it works? Update: totally works
    """

    for i in range(81):
        # all items in the row/col/box that are 0 (modified in the next section to make this the case)
        row = getrowindexes(i)
        column = getcolumnindexes(i)
        box = getboxindexes(i)

        # makes each list above only contain indexes of cells with no value in them (0)
        itercol = column[:]
        for index in itercol:
            if puzzle[index] != 0:
                column.remove(index)

        iterbox = box[:]
        for index in iterbox:
            if puzzle[index] != 0:
                box.remove(index)

        iterrow = row[:]
        for index in iterrow:
            if puzzle[index] != 0:
                row.remove(index)
        ###

        # prepare lists that contain all values that each cell in the row/col/box could possibly be
        possiblerowvalues = []
        for index in row:
            possiblerowvalues.append(findpossiblevalues(index))

        possiblecolumnvalues = []
        for index in column:
            possiblecolumnvalues.append(findpossiblevalues(index))

        possibleboxvalues = []
        for index in box:
            possibleboxvalues.append(findpossiblevalues(index))

        # turn all the 2D lists into 1D
        possiblerowvalues = [x for sublist in possiblerowvalues for x in sublist]
        possiblecolumnvalues = [x for sublist in possiblecolumnvalues for x in sublist]
        possibleboxvalues = [x for sublist in possibleboxvalues for x in sublist]

        ###

        for value in findpossiblevalues(i):
            if possiblerowvalues.count(value) == 1 and puzzle[i] == 0:
                puzzle[i] = value
                return True
            if possiblecolumnvalues.count(value) == 1 and puzzle[i] == 0:
                puzzle[i] = value
                return True
            if possibleboxvalues.count(value) == 1 and puzzle[i] == 0:
                puzzle[i] = value
                return True
    return False





# Finally, the bit that executes, after all those functions.
puzzle = gatherinput("C:\\CourseWork\\AI\\Sudoku\\sudoku.txt")

# GUI Setup
window = tkinter.Tk()
window.title("Sudoku Solver")

bool_m1 = tkinter.BooleanVar(window, False)
bool_m2 = tkinter.BooleanVar(window, False)

entrylist = []
for i in range(81):
    entrylist.append(tkinter.Entry(window, width=5))
    entrylist[i].insert(0, puzzle[i])

for i in range(9):
    for j in range(9):
        entrylist[i*9 + j].grid(row=i, column=j+1)

validtext = tkinter.StringVar(window, " - ")
lbl_validmarker = tkinter.Label(window, textvariable=validtext)
lbl_validmarker.grid(row=12, column=0)


# GUI Methods
def solveStep():
    global puzzle
    puzzle = formatpuzzlestring(getEntries())

    simplebool = False
    singleinfbool = False

    if bool_m1.get() and bool_m2.get():
        simplebool = simpleguess()
        singleinfbool = singleinferenceguess()
    elif bool_m1.get():
        simplebool = simpleguess()
    elif bool_m2.get():
        singleinfbool = singleinferenceguess()

    updateEntries()
    if not simplebool and not singleinfbool:
        isValid()


# GUI Methods
def updateEntries():
    for i in range(81):
        entrylist[i].delete(0, tkinter.END)
        entrylist[i].insert(0, str(puzzle[i]))


def getEntries():
    puzzleString = []
    for entry in entrylist:
        puzzleString.append(entry.get())
    return puzzleString


def isValid():
    if validatepuzzle():
        validtext.set("Valid")
    else:
        validtext.set("Not Valid")

chkbtn_method1 = tkinter.Checkbutton(window, text="Method 1", variable=bool_m1, onvalue=True, offvalue=False)
chkbtn_method2 = tkinter.Checkbutton(window, text="Method 2", variable=bool_m2, onvalue=True, offvalue=False)
chkbtn_method1.grid( row=10, column=0)
chkbtn_method2.grid( row=11, column=0)

btn_execute = tkinter.Button(window, text="Step", command=solveStep)
btn_execute.grid(row=13, column=0)

window.mainloop()




#puzzles = gatherinput("C:\\CourseWork\\AI\\Sudoku\\sudoku_hard.txt")
#for puzzle in puzzles:
#    print(makeallguesses(puzzle, "easy"))
#    displaypuzzle(puzzle)
#
#    if validatepuzzle(puzzle):
#        print("Valid\n\n")  # the newlines are just to get it to print nicely
#    else:
#        print("Not Valid\n\n")
