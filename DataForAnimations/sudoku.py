from collections import defaultdict
import numpy as np
import time

#I used one possible thing we could do is increase the board size to a 16x16 board if we want to show more examples of the board 

def forDefaultDic():
    return 0

class sudoku:
    def __init__(self) -> None:
        """This __init__ function is the constructor for the class.  It just initalizes the 3 board states."""
        self.easyBoard = [[None,None, 9,4,2,None,None,6,None],
        [None,7,None,9,None,5,3,None,2],
        [5,None,None,None,None,3,None,9,None],
        [None,None,None,8,None,1,None,2,None],
        [2,6,None,None,None,None,None,5,1],
        [None,1,8,2,None,None,4,None,None],
        [3,8,None,None,None,4,None,1,9],
        [None,9,4,None,3,None,6,8,5],
        [None,2,1,None,None,8,None,3,None]]

        self.mediumBoard = [[None,None,None,None,None,6,None,3,1],
        [2,5,7,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None],
        [7,4,None,6,9,3,2,None,None],
        [None,None,None,None,None,1,None,9,None,],
        [None,None,6,4,None,None,None,5,None],
        [3,7,None,None,1,4,9,6,None],
        [4,2,9,None,6,7,None,None,None,],
        [None,None,1,None,None,9,None,None,None,]]

        self.hardBoard = [[None,9,None,None,None,None,None,1,None],
        [5,None,1,None,None,3,None,None,6],
        [None,7,None,None,5,None,None,None,None],
        [2,None,4,None,9,None,None,6,None],
        [None,None,None,8,None,None,None,None,3],
        [None,1,None,None,None,None,None,None,None],
        [6,None,5,None,2,None,None,4,None],
        [7,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,9,2,None,None,]]

        self.evilBoard = [[8, None, None, None, None, None, None, None, None],
        [None, None, 3, 6, None, None, None, None, None],
        [None, 7, None, None, 9, None, 2, None, None],
        [None, 5, None, None, None, 7, None, None, None],
        [None, None, None, None, 4, 5, 7, None, None],
        [None, None, None, 1, None, None, None, 3, None],
        [None, None, 1, None, None, None, None, 6, 8],
        [None, None, 8, 5, None, None, None, 1, None],
        [None, 9, None, None, None, None, 4, None, None,]]


        return
    def reset(self):
        """This function resets all the board back to their initial position"""
        self.__init__()
        return
    
    def isValid(self, board):
        """This function returns true if the current state of the board is still valid, or if the final board is a valid solution"""
        #counting the occurrences of each number in each row
        seen = defaultdict(forDefaultDic)
        for i in range(len(board)):
            for j in range(len(board[0])):
                elem = board[i][j]
                if elem == None: continue #skip None, the place holder value.
                seen[f'{elem} found in row {j}'] += 1
                seen[f'{elem} found in column {i}'] += 1
                seen[f'{elem} found in box {i//3},{j//3}'] += 1
        for value in seen.values():
            if value > 1: return False
        return True

    def possible(self, board, y, x):
        """This function returns all of the possible numbers that could go in position board[y][x]"""
        output = []
        for num in range(1,10):
            good = True
            #check row
            if num in board[y]: continue #I don't update good here because using the continue statement does what I want
            #check column
            for i in range(9):
                if num == board[i][x]:
                    good = False
            #check 3x3 box
            boxY = y//3
            boxX = x//3
            for i in range(3):
                for j in range(3):
                    if num == board[i+boxY*3][j+boxX*3]:
                        good = False
            if good:
                output.append(num)
        return output

    def showBoard(self, board):
        n = np.array(board)
        print(n)
        return
    
    def solved(self, board):
        """This function returns True if the board is fully solved, otherwise False.
           The board is considered fully solved if every position has a number and
           the current state of the board is valid."""
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == None: return False
        return self.isValid(board)
    
    def DFS(self, board):
        """Solves the board using DFS brute force solution"""
        #Solution inspired by: https://www.youtube.com/watch?v=G_UYXzGuqvM
        #I didn't do everything the same becaue I thought that could be an AI violation.
        global countDFS
        countDFS += 1 #counting the number of recursive calls
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] != None: continue #This position already has a number
                possibleNums = self.possible(board, i, j)
                for num in possibleNums:
                    board[i][j] = num
                    self.DFS(board)
                    #Check if board is solved for base case
                    if self.solved(board): return #board is solved nothing else to do
                    board[i][j] = None
                return
    
    def isSolvedGreedy(self, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if type(board[i][j]) != int: return False
        return self.isValidGreedy(board)
    
    def greedyRemove(self, board, num, y, x):
        output = []
        #remove from row
        for j in range(len(board[0])):
            if type(board[y][j]) == int: continue #skip placed numbers
            if num in board[y][j]:
                output.append((y,j)) #remember these for output
                board[y][j].remove(num)
        
        #remove from column
        for i in range(len(board)):
            if type(board[i][x]) == int: continue #skip placed numbers
            if num in board[i][x]:
                output.append((i,x)) #remember these for output
                board[i][x].remove(num)
        
        #remove from box
        boxX = x//3
        boxY = y//3
        for i in range(3):
            for j in range(3):
                if type(board[i+3*boxY][j+3*boxX]) == int: continue #skip placed numbers
                if num in board[i+3*boxY][j+3*boxX]:
                    output.append(((i+3*boxY),(j+3*boxX))) #remember these for output This got really ugly but should work
                    board[i+3*boxY][j+3*boxX].remove(num)
        return output

    def greedyAdd(self, board, num, places):
        """This adds num to the lists at coords in places"""
        for place in places:
            x = place[1]
            y = place[0]
            if type(board[y][x]) != list: print("Something has gone terribly wrong.  Check greedyAdd and greedyRemove")
            board[y][x].append(num)
        return

    def isValidGreedy(self, board):
        """This function returns true if the current state of the board is still valid, or if the final board is a valid solution"""
        #If you want a detailed explination on how this works check here: https://www.youtube.com/watch?v=Pl7mMcBm2b8
        #counting the occurrences of each number in each row
        seen = defaultdict(forDefaultDic)
        for i in range(len(board)):
            for j in range(len(board[0])):
                elem = board[i][j]
                if type(elem) != int: continue #skip elemts that are a list
                seen[f'{elem} found in row {j}'] += 1
                seen[f'{elem} found in column {i}'] += 1
                seen[f'{elem} found in box {i//3},{j//3}'] += 1
        for value in seen.values():
            if value > 1: return False
        return True

    def findLowest(self, board):
        """Helper function for the greedy solver.  Returns the i, j position of the list with the fewest values"""
        breakflag = False
        for i in range(len(board)):
            for j in range(len(board[0])):
                if type(board[i][j]) != int:
                    y, x = i, j
                    breakflag = True
                    break
            if breakflag: break
        #find coords of min len
        for i in range(len(board)):
            for j in range(len(board[0])):
                if type(board[i][j]) == int: continue #skip int values
                if len(board[y][x]) > len(board[i][j]):
                    y, x = i, j
        return y, x

    def Greedy(self, board):
        # fill every empty position with a list of possible values it can hold
        for i in range(len(board)):
            for j in range(len(board[0])):
                if type(board[i][j]) == int: continue #skip over numbers already placed in board
                lst = self.possible(board, i, j)
                board[i][j] = lst
        self.GreedyHelper(board)
        return
    
    def GreedyHelper(self, board):
        global countGreedy
        countGreedy += 1
        if self.isSolvedGreedy(board): return #return if the board is solved base case
        #the board has a list of possible values for every position that isn't filled yet
        i, j = self.findLowest(board)
        possibleNums = board[i][j]
        for num in possibleNums:
            board[i][j] = num
            #remove num from lists that are in same row, column and box
            removedPoints = self.greedyRemove(board, num, i, j)
            self.GreedyHelper(board)
            if self.isSolvedGreedy(board): return
            #need to restore num back to lists we removed it from
            self.greedyAdd(board, num, removedPoints)
            board[i][j] = possibleNums
        return

global countDFS, countGreedy
countDFS = 0
countGreedy = 0
if __name__ == '__main__':
    s = sudoku()
    #preformance evaluation is below
    #calculating the time for DFS to solve each board, and number of recursive calls
    t1 = time.time()
    s.DFS(s.easyBoard)
    t2 = time.time()
    timeEasy = t2-t1
    countEasy = countDFS

    countDFS = 0
    t1 = time.time()
    s.DFS(s.mediumBoard)
    t2 = time.time()
    timeMedium = t2-t1
    countMedium = countDFS

    countDFS = 0
    t1 = time.time()
    s.DFS(s.hardBoard)
    t2 = time.time()
    timeHard = t2-t1
    countHard = countDFS

    countDFS = 0
    t1 = time.time()
    s.DFS(s.evilBoard)
    t2 = time.time()
    timeEvil = t2-t1
    countEvil = countDFS

    print('\nResults for DFS')
    print(f'Time easyBoard: {timeEasy} \t Time mediumBoard: {timeMedium} \t Time hardBoard: {timeHard} \t Time evilBoard: {timeEvil}')
    print(f'Nodes easyBoard: {countEasy} \t Nodes mediumBoard: {countMedium} \t Nodes Hard: {countHard} \t Nodes Evil: {countEvil}')
    print() #just adding a new line to make it look better

    # Calculating the time for Greedy to run, and number of recursive calls
    s.reset()
    t1 = time.time()
    s.Greedy(s.easyBoard) #passing in an already solved board for testing
    t2 = time.time()
    timeEasy = t2-t1
    countEasy = countGreedy

    countGreedy = 0
    t1 = time.time()
    s.Greedy(s.mediumBoard)
    t2 = time.time()
    timeMedium = t2-t1
    countMedium = countGreedy

    countGreedy = 0
    t1 = time.time()
    s.Greedy(s.hardBoard)
    t2 = time.time()
    timeHard = t2-t1
    countHard = countGreedy

    countGreedy = 0
    t1 = time.time()
    s.Greedy(s.evilBoard)
    t2 = time.time()
    timeEvil = t2-t1
    countEvil = countGreedy

    print('\nResults for Greedy')
    print(f'Time easyBoard: {timeEasy} \t Time mediumBoard: {timeMedium} \t Time hardBoard: {timeHard} \t Time evilBoard: {timeEvil}')
    print(f'Nodes easyBoard: {countEasy} \t Nodes mediumBoard: {countMedium} \t Nodes Hard: {countHard} \t Nodes Evil: {countEvil}')
    print() #just adding a new line to make it look better
