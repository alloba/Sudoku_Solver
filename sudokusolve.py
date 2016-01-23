import tkinter
from puzzlecontainer import SudokuPuzzle
from tkinter import filedialog

def gatherinput(filename):
    """
     take input from a file, with directory specified as a parameter.
     ideally, correct format should be "[num][space][num][space].....[num][newline] * 9"

    """
    try:
        file = open(filename)
        puzzlein = file.read()
    except FileNotFoundError:
        puzzlein = "," * 81
    listify = puzzlein.replace('\t', ',').replace('\n', ',').replace(' ', ',').split(',')

    return listify

try:
    puzzle = SudokuPuzzle(gatherinput("C:\\CourseWork\\AI\\Sudoku\\sudoku.txt"))
except FileNotFoundError:
    puzzle = SudokuPuzzle()
puzzleprevstep = puzzle.puzzle[:]


# GUI Methods
def solveStep(junkvar=0):  # try to solve one step in the puzzle, and display an update.
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


def updateEntries():
    for i in range(81):
        if puzzle.puzzle[i] != puzzleprevstep[i]:
            entrylist[i].delete(0, tkinter.END)
            entrylist[i].insert(0, str(puzzle.puzzle[i]))
            entrylist[i].config(bg="red")  # to show that something has been filled in here

def setEntries():
    for i in range(81):
        entrylist[i].delete(0, tkinter.END)
        entrylist[i].insert(0, str(puzzle.puzzle[i]))

def getEntries():
    puzzleString = []
    for entry in entrylist:
        puzzleString.append(entry.get())
    return puzzleString


def isValid():
    if puzzle.validatepuzzle():
        validtext.set("Solved")
    else:
        validtext.set("Not Solved")


def openfile():
    filename = filedialog.askopenfilename(parent=window)
    try:
        global puzzleprevstep
        puzzle.updatepuzzle(gatherinput(filename))
        puzzleprevstep = puzzle.puzzle[:]
        setEntries()
        for entry in entrylist:
            entry.config(bg="white")
    except (FileNotFoundError, UnicodeDecodeError, ValueError) as e:
        return

# GUI Setup
window = tkinter.Tk()
window.resizable(width=0, height=0)
window.title("Sudoku Solver")

# these bools are for the checkboxes that select methods
bool_m1 = tkinter.BooleanVar(window, True)
bool_m2 = tkinter.BooleanVar(window, False)

# all the boxes that display the puzzle, put into a group to make it display better
entrygroup = tkinter.LabelFrame(window, text="")
entrygroup.grid(row=0, column=0, rowspan=9, columnspan=9, padx=40)
entrylist = []
for i in range(81):
    entrylist.append(tkinter.Entry(entrygroup, width=3, justify=tkinter.CENTER))
    entrylist[i].insert(0, puzzle.puzzle[i])

for i in range(9):
    for j in range(9):
        entrylist[i*9 + j].grid(row=i, column=j+1)


validtext = tkinter.StringVar(window, "              ")
lbl_validmarker = tkinter.Label(window, textvariable=validtext)
lbl_validmarker.grid(row=9, column=2)

lbl_solutionsdisplay = tkinter.Label(window, text="Found:")
lbl_solutionsdisplay.grid(row=10, column=0, sticky="W")

solutionsfound = tkinter.IntVar(window, 0)
lbl_solutionsfound = tkinter.Label(window, textvariable=solutionsfound)
lbl_solutionsfound.grid(row=10, column=1, sticky="W")

chkbtn_method1 = tkinter.Checkbutton(window, text="Method 1", variable=bool_m1, onvalue=True, offvalue=False)
chkbtn_method2 = tkinter.Checkbutton(window, text="Method 2", variable=bool_m2, onvalue=True, offvalue=False)
chkbtn_method1.grid(row=9, column=0)
chkbtn_method2.grid(row=9, column=1)

btn_execute = tkinter.Button(window, text="Step", command=solveStep)
btn_execute.grid(row=9, column=8)

menubar = tkinter.Menu(window)
menubar.add_command(label="Open New Puzzle", command=openfile)

window.bind('<Return>', solveStep)
window.config(menu=menubar)
window.mainloop()

