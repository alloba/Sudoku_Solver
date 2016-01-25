import tkinter, os, sys
from puzzlecontainer import SudokuPuzzle
from tkinter import filedialog


def gatherinput(filedirectory):
    """
     take input from a file, with directory specified as a parameter.
     ideally, correct format should be "[num][space][num][space].....[num][newline] * 9"

    """
    global filename
    filename = filedirectory
    try:
        file = open(filename)
        puzzlein = file.read()
    except FileNotFoundError:
        puzzlein = "," * 81
    listify = puzzlein.replace('\t', ',').replace('\n', ',').replace(' ', ',').split(',')

    return listify

try:
    filename = os.getcwd() + "\\puzzle.txt"
    print(filename)
    puzzle = SudokuPuzzle(gatherinput(filename))
except FileNotFoundError:
    puzzle = SudokuPuzzle()

puzzleprevstep = puzzle.puzzle[:]

# GUI Methods
def solveStep(junkvar=0):  # try to solve one step in the puzzle, and display an update.

    global puzzle
    global puzzleprevstep

    puzzle.updatepuzzle(getEntries())
    puzzleprevstep = puzzle.puzzle[:]
    updateEntries()


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

    if simplebool or singleinfbool:
        solutionsfound.set(solutionsfound.get() + 1)

    if not simplebool and not singleinfbool:
        isValid()

    updateEntries()


def updateEntries():
    for i in range(81):
        if puzzle.puzzle[i] != puzzleprevstep[i]:
            entrylist[i].delete(0, tkinter.END)
            if puzzle.puzzle[i] == 0:
                entrylist[i].insert(0, "")
            else:
                entrylist[i].insert(0, str(puzzle.puzzle[i]))

            entrylist[i].config(bg="red")  # to show that something has been filled in here

def resetwindow():
    global puzzle, puzzleprevstep, filename
    puzzle.updatepuzzle(gatherinput(filename))
    puzzleprevstep = puzzle.puzzle[:]

    validtext.set("")
    solutionsfound.set(0)
    for i in range(81):
        entrylist[i].delete(0, tkinter.END)
        if puzzle.puzzle[i] == 0:
            entrylist[i].insert(0, "")
        else:
            entrylist[i].insert(0, str(puzzle.puzzle[i]))

        entrylist[i].config(bg="white")


def getEntries():
    puzzleString = []
    for entry in entrylist:
        if entry.get() == "":
            puzzleString.append("0")
        else:
            puzzleString.append(entry.get())
    return puzzleString


def isValid():
    if puzzle.validatepuzzle():
        validtext.set("Solved")
    else:
        validtext.set("Not Solved")


def openfile():
    global puzzleprevstep, filename, puzzle

    filename = filedialog.askopenfilename(parent=window)

    try:
        puzzle.updatepuzzle(gatherinput(filename))
        puzzleprevstep = puzzle.puzzle[:]
        resetwindow()
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
for i in range(9):
    for j in range(9):
        entrylist.append(tkinter.Entry(entrygroup, width=3, justify=tkinter.CENTER))
        entrylist[i*9 + j].insert(0, puzzle.puzzle[i*9 + j])

for i in range(9):
    for j in range(9):
        entrylist[i*9 + j].grid(row=i, column=j+1)


#Hard-coded black lines to separate boxes on the puzzle. beest solution i could come up with...
tkinter.Frame(entrygroup,bg="black",width=2,height=375).place(x=0,  y=10,anchor=tkinter.E)
tkinter.Frame(entrygroup,bg="black",width=2,height=375).place(x=200,y=10,anchor=tkinter.E)
tkinter.Frame(entrygroup,bg="black",width=375,height=2).place(x=10, y=171,anchor=tkinter.N)
tkinter.Frame(entrygroup,bg="black",width=375,height=2).place(x=10, y=-2,anchor=tkinter.N)

tkinter.Frame(entrygroup,bg="black",width=2,height=375).place(x=68,y=10,anchor=tkinter.E)
tkinter.Frame(entrygroup,bg="black",width=2,height=375).place(x=133,y=10,anchor=tkinter.E)
tkinter.Frame(entrygroup,bg="black",width=375,height=2).place(x=10,y=57,anchor=tkinter.N)
tkinter.Frame(entrygroup,bg="black",width=375,height=2).place(x=10,y=113,anchor=tkinter.N)
###



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

btn_reset = tkinter.Button(window, text="Reset", command = resetwindow)
btn_reset.grid(row=10, column=8)

menubar = tkinter.Menu(window)
menubar.add_command(label="Open New Puzzle", command=openfile)
#TODO: Add menu button to display instructions/help
# call resetwindow once to get rid of all the 0's from the initial loading.
resetwindow()

window.bind('<Return>', solveStep)
window.config(menu=menubar)
window.mainloop()

