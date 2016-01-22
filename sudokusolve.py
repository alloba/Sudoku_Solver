import tkinter
from puzzlecontainer import SudokuPuzzle

def gatherinput(filename):
    """
     take input from a file, with directory specified as a parameter.
     ideally, correct format should be "[num][space][num][space].....[num][newline] * 9"

    """

    file = open(filename)
    puzzlein = file.read()
    listify = puzzlein.replace('\t', ',').replace('\n', ',').replace(' ', ',').split(',')

    return listify


# Finally, the bit that executes, after all those functions.
puzzle = SudokuPuzzle(gatherinput("C:\\CourseWork\\AI\\Sudoku\\sudoku.txt"))
puzzleprevstep = puzzle.puzzle[:]

# GUI Setup
window = tkinter.Tk()
window.title("Sudoku Solver")

bool_m1 = tkinter.BooleanVar(window, False)
bool_m2 = tkinter.BooleanVar(window, False)

entrylist = []
for i in range(81):
    entrylist.append(tkinter.Entry(window, width=5))
    entrylist[i].insert(0, puzzle.puzzle[i])

for i in range(9):
    for j in range(9):
        entrylist[i*9 + j].grid(row=i, column=j+1)

validtext = tkinter.StringVar(window, " - ")
lbl_validmarker = tkinter.Label(window, textvariable=validtext)
lbl_validmarker.grid(row=13, column=0)

lbl_solutionsdisplay = tkinter.Label(window, text="Found: ")
lbl_solutionsdisplay.grid(row=12, column=0)

solutionsfound = tkinter.IntVar(window, 0)
lbl_solutionsfound = tkinter.Label(window, textvariable=solutionsfound)
lbl_solutionsfound.grid(row=12, column=1)

# GUI Methods
def solveStep():
    puzzle.updatepuzzle(getEntries())

    simplebool = False
    singleinfbool = False

    if bool_m1.get() and bool_m2.get():
        simplebool = puzzle.simpleguess()
        if not simplebool:
            singleinfbool = puzzle.singleinferenceguess()

    elif bool_m1.get():
        simplebool = puzzle.simpleguess()

    elif bool_m2.get():
        singleinfbool = puzzle.singleinferenceguess()

    updateEntries()

    if simplebool or singleinfbool:
        solutionsfound.set(solutionsfound.get() + 1)

    if not simplebool and not singleinfbool:
        isValid()


# GUI Methods
def updateEntries():
    for i in range(81):
        if puzzle.puzzle[i] != puzzleprevstep[i]:
            entrylist[i].delete(0, tkinter.END)
            entrylist[i].insert(0, str(puzzle.puzzle[i]))
            entrylist[i].config(bg="red")


def getEntries():
    puzzleString = []
    for entry in entrylist:
        puzzleString.append(entry.get())
    return puzzleString


def isValid():
    if puzzle.validatepuzzle():
        validtext.set("Valid")
    else:
        validtext.set("Not Valid")

chkbtn_method1 = tkinter.Checkbutton(window, text="Method 1", variable=bool_m1, onvalue=True, offvalue=False)
chkbtn_method2 = tkinter.Checkbutton(window, text="Method 2", variable=bool_m2, onvalue=True, offvalue=False)
chkbtn_method1.grid( row=10, column=0)
chkbtn_method2.grid( row=11, column=0)

btn_execute = tkinter.Button(window, text="Step", command=solveStep)
btn_execute.grid(row=0, column=0)

window.mainloop()

