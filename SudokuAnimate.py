import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatch
import pickle
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
import matplotlib
from playsound import playsound
import time

t1 = time.time()
# FPS = 10 #frames per second for saved animation
FPS = 10

WHITE = '#ffffff'
GRAY = '#585c5b'
RED = '#ad323d'
YELLOW = '#b09527'
BLUE = '#3772c4'
BLACK = '#000000'
GREEN = '#03915f'
SCALE = 10
ANIMATION_SPEED = 1

#read in data and put it in the variables used for the animation

DFS_EASY_INFILE = 'Sudoku/dataForAnimation/easyDFS.txt'
DFS_MEDIUM_INFILE  = 'Sudoku/dataForAnimation/mediumDFS.txt'
DFS_HARD_INFILE  = 'Sudoku/dataForAnimation/hardDFS.txt'
DFS_EVIL_INFILE  = 'Sudoku/dataForAnimation/evilDFS.txt'

GREEDY_EASY_INFILE = 'Sudoku/dataForAnimation/easyGreedy.txt'
GREEDY_MEDIUM_INFILE = 'Sudoku/dataForAnimation/mediumGreedy.txt'
GREEDY_HARD_INFILE = 'Sudoku/dataForAnimation/hardGreedy.txt'
GREEDY_EVIL_INFILE = 'Sudoku/dataForAnimation/evilGreedy.txt'


#put the filepath to the data from the board you want to animate in the ANIMATE variable
ANIMATE = 'Sudoku/dataForAnimation/easyGreedy.txt'



with open(ANIMATE, 'rb') as F:
    data = pickle.load(F)

    
    F.close()
initialBoard, solvedLst, solvingLst, red = data

# The render function will work for any size sudoku puzzle. The param 'sudoku_puzzle' is a 2D array.
def render(sudoku_puzzle):
    global fig, ax
    # ax.clear() # Resetting board, which is useful for animation with FuncAnimation
    ax.grid(True) # Set the gridlines
    
    puzzle_size = len(sudoku_puzzle)
    ax.set_xlim(0, puzzle_size) # Making 'puzzle_size' boxes for each row
    ax.set_ylim(0, puzzle_size) # Making 'puzzle_size' boxes for each column
    ax.set_xticklabels([]); ax.set_yticklabels([]) # Removing the x and y labels

    # Process 1: Thickening certain lines of the sudoku puzzle
    width = 5 
    for line in range(puzzle_size//3, puzzle_size, puzzle_size//3):
        ax.axhline(line, color="black", linewidth=width)
        ax.axvline(line, color="black", linewidth=width)

    width = width * 2
    ax.axhline(0, color="black", linewidth=width) 
    ax.axhline(puzzle_size, color="black", linewidth=width)

    ax.axvline(0, color="black", linewidth=width)
    ax.axvline(puzzle_size, color="black", linewidth=width)

    # Process 2: Get the coordinates as the key with the number as the value for 'coordinates_for_num'
    coordinates_for_num = {}
    a = 0
    for y in range(puzzle_size): #I changed from going in reverse so i, j of animated points will match the coords of the board
        b = 0
        for x in range(0, puzzle_size):
            coordinates_for_num[(x,y)] = sudoku_puzzle[a][b]
            b += 1
        a += 1

    # Process 3: For each coordinates in coordinates_for_nums.keys(), we label the box in the coordinates with the assigned number
    for coords, num in coordinates_for_num.items():
        if num: # If the value 'num' is not None...
            ax.text(coords[0]+0.5, coords[1]+0.5, f'{num}', size=24, horizontalalignment='center', verticalalignment='center', fontweight='bold', color=WHITE)
            rec = mpatch.Rectangle((coords[0],coords[1]), 1, 1, color=GRAY)
            ax.add_patch(rec)
    # fig, ax is returned to be reference in animate() implementation
    return #fig, ax

#variabgles that will be used: initialBoard, solvedLst, solvingLst, red
def animate(i):
    global fig, ax
    #reset board
    ax.clear()
    render(initialBoard) #render the original board again
    
    #making the last frame green
    if i == len(solvedLst)-1:
        solved = solvedLst[i]
        for point, num in solved.items(): #note num was already made a string earlier for convenience
            j, k = point
            ax.text(k+0.5, j+0.5, num, size=24, horizontalalignment='center', verticalalignment='center', fontweight='bold', color=WHITE)
            rec = mpatch.Rectangle((k,j), 1, 1, color=GREEN)
            ax.add_patch(rec)
            ax.set_title(f'Solved in {len(solvedLst)} ticks')
        return
    
    #not at last frame do normal operation
    # color and fill in points that have been solved
    solved = solvedLst[i]
    for point, num in solved.items(): #note num was already made a string earlier for convenience
        j, k = point
        ax.text(k+0.5, j+0.5, num, size=24, horizontalalignment='center', verticalalignment='center', fontweight='bold', color=BLACK)
        rec = mpatch.Rectangle((k,j), 1, 1, color=BLUE)
        ax.add_patch(rec)
    # color and fill in point that is getting solved
    gettingSolved = solvingLst[i]
    for point, num in gettingSolved.items(): #This loop only runs for one iteration, but it is a convenient way get what I want
        j, k = point
        ax.text(k+0.5, j+0.5, num, size=24, horizontalalignment='center', verticalalignment='center', fontweight='bold', color=BLACK)
        rec = mpatch.Rectangle((k,j), 1, 1, color=YELLOW)
        ax.add_patch(rec)
    # fil in box that should be red if it exists
    redBox = red[i]
    if redBox: #this runs if redBox != None
        j, k = redBox
        rec = mpatch.Rectangle((k,j), 1, 1, color=RED)
        ax.add_patch(rec)
    ax.set_title(f'Timetick {i}')
    return



# --- Running Animation  ---
#making it so the last frame will have all the solved numbers be green
solvedLst.append(solvedLst[-1]) #adding all then numbers for another frame

#run amimation
global fig, ax
fig, ax = plt.subplots(figsize=(SCALE, SCALE))
animation = FuncAnimation(fig, animate, frames=len(solvedLst), interval=ANIMATION_SPEED, repeat=False)
# plt.show()


#saving the animations
DFS_EASY_OUTFILE = 'Sudoku/Animations/easyDFS.mp4'
DFS_MEDIUM_OUTFILE = 'Sudoku/Animations/mediumDFS.mp4'
DFS_HARD_OUTFILE = 'Sudoku/Animations/hardDFS.mp4'
DFS_EVIL_OUTFILE = 'Sudoku/Animations/evilDFS.mp4'
GREEDY_EASY_OUTFILE = 'Sudoku/Animations/easyGreedy.mp4'
GREEDY_MEDIUM_OUTFILE = 'Sudoku/Animations/mediumGreedy.mp4'
GREEDY_HARD_OUTFILE = 'Sudoku/Animations/hardGreedy.mp4'
GREEDY_EVIL_OUTFILE = 'Sudoku/Animations/evilGreedy.mp4'

def chooseOutFile(A):
    out = ''
    if A == DFS_EASY_INFILE:
        out = DFS_EASY_OUTFILE
    elif A == DFS_MEDIUM_INFILE:
        out = DFS_MEDIUM_OUTFILE
    elif A == DFS_HARD_INFILE:
        out = DFS_HARD_OUTFILE
    elif A == DFS_EVIL_INFILE:
        out = DFS_EVIL_OUTFILE
    elif A == GREEDY_EASY_INFILE:
        out = GREEDY_EASY_OUTFILE
    elif A == GREEDY_MEDIUM_INFILE:
        out = GREEDY_MEDIUM_OUTFILE
    elif A == GREEDY_HARD_INFILE:
        out = GREEDY_HARD_OUTFILE
    elif A == GREEDY_EVIL_INFILE:
        out = GREEDY_EVIL_OUTFILE
    return out

OUTFILE = chooseOutFile(ANIMATE)
matplotlib.rcParams['animation.ffmpeg_path'] = "C:\\Users\\enoch\Downloads\\ffmpeg-5.1.2-essentials_build\\ffmpeg-5.1.2-essentials_build\\bin\\ffmpeg.exe"
writer = FFMpegWriter(fps=FPS, metadata=dict(artist='Me'), bitrate=1800)
animation.save(OUTFILE, writer=writer) 
t2 = time.time()
playsound('Sudoku\Animations\endSound.wav')#playing sound when computer is done so I know to animate and save the next puzzle board
print(f'Done in {t2-t1} seconds :)')