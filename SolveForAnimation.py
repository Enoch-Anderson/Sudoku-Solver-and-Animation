from collections import defaultdict
import numpy as np
import pickle

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
        #If you want a detailed explination on how this works check here: https://www.youtube.com/watch?v=Pl7mMcBm2b8
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
        global solvedLst, solvingLst, red
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] != None: continue #This position already has a number
                possibleNums = self.possible(board, i, j)
                for num in possibleNums:
                    #add the first frame of solving to animation
                    solvedLst.append(solvedLst[-1].copy())#just adding the previous frame's solved list again
                    solvingLst.append({(i,j):''})#make the square a different color, but don't add the number yet
                    red.append(None)
                    board[i][j] = num
                    
                    #add second frame, number added to spot
                    #can't have the same (i, j) be in solvedLst and solvingLst
                    solved = solvedLst[-1].copy()
                    if (i, j) in solved:
                        del solved[(i,j)]
                    solvedLst.append(solved)
                    solvingLst.append({(i,j):str(num)})
                    red.append(None)
                    
                    #add last frame, color changed to be normal solved color
                    solved = solvedLst[-1].copy() #copying reference not the contents
                    solved[(i,j)]= str(num)
                    solvedLst.append(solved)
                    solvingLst.append({})
                    red.append(None)
                    self.DFS(board)
                    #Check if board is solved for base case
                    if self.solved(board): return #board is solved nothing else to do
                    board[i][j] = None
                
                if possibleNums == []: #handle case before backtracking happens.  Reached a point where this square has no numbers that can go in it.
                    red.append((i,j))
                    solvedLst.append(solvedLst[-1].copy())
                    solvingLst.append({})
                
                else: #we are currently in a backtrack path
                    #if we are here we are backtracking back to previous state before this one seen
                    #first frame, make the square yellow with number again
                    solved = solvedLst[-1].copy()
                    del solved[(i, j)]
                    solvedLst.append(solved)
                    solvingLst.append({(i,j):str(num)})
                    red.append(None)
                    
                    #second frame, remove number but square still yellow
                    solvedLst.append(solvedLst[-1].copy())#just adding the previous frame's solved list again
                    solvingLst.append({(i,j):''})#make the square a different color, but don't add the number yet
                    red.append(None)
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
        if self.isSolvedGreedy(board): return #return if the board is solved base case
        global solvedLst, solvingLst, initialBoard, red
        #the board has a list of possible values for every position that isn't filled yet
        i, j = self.findLowest(board)
        possibleNums = board[i][j]
        for num in possibleNums:
            #add the first frame of solving to animation
            solvedLst.append(solvedLst[-1].copy())#just adding the previous frame's solved list again
            solvingLst.append({(i,j):''})#make the square a different color, but don't add the number yet
            red.append(None)
            board[i][j] = num

            #add second frame, number added to spot
            #can't have the same (i, j) be in solvedLst and solvingLst
            solved = solvedLst[-1].copy()
            if (i, j) in solved:
                del solved[(i,j)]
            solvedLst.append(solved)
            solvingLst.append({(i,j):str(num)})
            red.append(None)

            #add last frame, color changed to be normal solved color
            solved = solvedLst[-1].copy() #copying reference not the contents
            solved[(i,j)]= str(num)
            solvedLst.append(solved)
            solvingLst.append({})
            red.append(None)
            #remove num from lists that are in same row, column and box
            removedPoints = self.greedyRemove(board, num, i, j)
            self.GreedyHelper(board) #recursive call

            if self.isSolvedGreedy(board): return
            #need to restore num back to lists we removed it from
            self.greedyAdd(board, num, removedPoints)
            board[i][j] = possibleNums
            
            #adding backtracking frames 
            if possibleNums == []: #handle case before backtracking happens.  Reached a point where this square has no numbers that can go in it.
                red.append((i,j))
                solvedLst.append(solvedLst[-1].copy())
                solvingLst.append({})
            
            else: #we are currently in a backtrack path
                #if we are here we are backtracking back to previous state before this one seen
                #first frame, make the square yellow with number again
                solved = solvedLst[-1].copy()
                del solved[(i, j)]
                solvedLst.append(solved)
                solvingLst.append({(i,j):str(num)})
                red.append(None)
                
                #second frame, remove number but square still yellow
                solvedLst.append(solvedLst[-1].copy())#just adding the previous frame's solved list again
                solvingLst.append({(i,j):''})#make the square a different color, but don't add the number yet
                red.append(None)
        return


def addInitalState(board: list[list]):
    """This function adds the inital state of the board to the elements used for the animation"""
    global solvedLst, solvingLst, initialBoard
    initialBoard = [board[i].copy() for i in range(len(board))] #copying conents, not memory address of original board
    solvedLst.append({})#empty because nothing is solved yet
    solvingLst.append({})#empty so no yellow squares yet
    red.append(None) #will hold the (i, j) on frames that need to be red for a frame
    return

def resetGlobals():
    global solvedLst, solvingLst, initialBoard, red
    initialBoard = None #just initalizing it so I can fill it later
    solvedLst = []
    solvingLst = []
    red = []
    return

if __name__ == '__main__':
    global solvedLst, solvingLst, initialBoard, red
    DFS_EASY_OUTFILE = 'Sudoku/dataForAnimation/easyDFS.txt'
    DFS_MEDIUM_OUTFILE = 'Sudoku/dataForAnimation/mediumDFS.txt'
    DFS_HARD_OUTFILE = 'Sudoku/dataForAnimation/hardDFS.txt'
    DFS_EVIL_OUTFILE = 'Sudoku/dataForAnimation/evilDFS.txt'
    GREEDY_EASY_OUTFILE = 'Sudoku/dataForAnimation/easyGreedy.txt'
    GREEDY_MEDIUM_OUTFILE = 'Sudoku/dataForAnimation/mediumGreedy.txt'
    GREEDY_HARD_OUTFILE = 'Sudoku/dataForAnimation/hardGreedy.txt'
    GREEDY_EVIL_OUTFILE = 'Sudoku/dataForAnimation/evilGreedy.txt'

    s = sudoku()
    # #get and save data for EASY DFS animation
    # resetGlobals()
    # addInitalState(s.easyBoard)
    # s.DFS(s.easyBoard)
    # #save results to a file, so it can be used in the animation
    # data = [initialBoard, solvedLst, solvingLst, red]
    # with open(DFS_EASY_OUTFILE, 'wb') as F:
    #     pickle.dump(data, F)
    #     F.close()

    # #get and save data for MEDIUM DFS animation
    # resetGlobals()
    # addInitalState(s.mediumBoard)
    # s.DFS(s.mediumBoard)
    # #save results to a file, so it can be used in the animation
    # data = [initialBoard, solvedLst, solvingLst, red]
    # with open(DFS_MEDIUM_OUTFILE, 'wb') as F:
    #     pickle.dump(data, F)
    #     F.close()

    # #get and save data for HARD DFS animation
    # resetGlobals()
    # addInitalState(s.hardBoard)
    # s.DFS(s.hardBoard)
    # #save results to a file, so it can be used in the animation
    # data = [initialBoard, solvedLst, solvingLst, red]
    # with open(DFS_HARD_OUTFILE, 'wb') as F:
    #     pickle.dump(data, F)
    #     F.close()

    # #get and save data for EVIL DFS animation
    # resetGlobals()
    # addInitalState(s.evilBoard)
    # s.DFS(s.evilBoard)
    # #save results to a file, so it can be used in the animation
    # data = [initialBoard, solvedLst, solvingLst, red]
    # with open(DFS_EVIL_OUTFILE, 'wb') as F:
    #     pickle.dump(data, F)
    #     F.close()


    # get and save data for EASY Greedy animation
    s.reset() #reset all the boards because they are currently solved
    resetGlobals()
    addInitalState(s.easyBoard)
    s.Greedy(s.easyBoard) #passing in an already solved board for testing
    #save results to a file, so it can be used in the animation
    data = [initialBoard, solvedLst, solvingLst, red]
    with open(GREEDY_EASY_OUTFILE, 'wb') as F:
        pickle.dump(data, F)
        F.close()

    # get and save data for EASY Greedy animation
    s.reset() #reset all the boards because they are currently solved
    resetGlobals()
    addInitalState(s.mediumBoard)
    s.Greedy(s.mediumBoard) #passing in an already solved board for testing
    #save results to a file, so it can be used in the animation
    data = [initialBoard, solvedLst, solvingLst, red]
    with open(GREEDY_MEDIUM_OUTFILE, 'wb') as F:
        pickle.dump(data, F)
        F.close()

    # get and save data for EASY Greedy animation
    s.reset() #reset all the boards because they are currently solved
    resetGlobals()
    addInitalState(s.hardBoard)
    s.Greedy(s.hardBoard) #passing in an already solved board for testing
    #save results to a file, so it can be used in the animation
    data = [initialBoard, solvedLst, solvingLst, red]
    with open(GREEDY_HARD_OUTFILE, 'wb') as F:
        pickle.dump(data, F)
        F.close()

    # get and save data for EASY Greedy animation
    s.reset() #reset all the boards because they are currently solved
    resetGlobals()
    addInitalState(s.evilBoard)
    s.Greedy(s.evilBoard) #passing in an already solved board for testing
    #save results to a file, so it can be used in the animation
    data = [initialBoard, solvedLst, solvingLst, red]
    with open(GREEDY_EVIL_OUTFILE, 'wb') as F:
        pickle.dump(data, F)
        F.close()
