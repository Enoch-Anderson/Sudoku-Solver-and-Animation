from memory_profiler import memory_usage
from time import sleep
from sudoku import sudoku
import psutil
import os

s = sudoku()

TIME_STEP = 0.001

#calculate the memory used for DFS
def base():
    """This function runs and does nothing, to calculate how much memory Python is using just as overhead"""
    return
def DFSeasy():
    s.DFS(s.easyBoard)
    return
def DFSmedium():
    s.DFS(s.mediumBoard)
    return
def DFShard():
    s.DFS(s.hardBoard)
    return
def DFSevil():
    s.DFS(s.evilBoard)
def greedyEasy():
    s.Greedy(s.easyBoard)
    return
def greedyMedium():
    s.Greedy(s.mediumBoard)
    return
def greedyHard():
    s.Greedy(s.hardBoard)
    return
def greedyEvil():
    s.Greedy(s.evilBoard)
    return


if __name__ == '__main__':
    #calculate base memory used by python, so we can just compare the differnece in memory used by the function
    base = max(memory_usage(base, TIME_STEP))

    #get memory for easy, medium, and evil for DFS
    memory = memory_usage(DFSeasy, TIME_STEP)
    easy = max(memory) - base
    memory = memory_usage(DFSmedium, TIME_STEP)
    medium = max(memory) - base
    memory = memory_usage(DFShard, TIME_STEP)
    hard = max(memory) - base
    memory = memory_usage(DFSevil, TIME_STEP)
    evil = max(memory) - base
    print('\nMemory useage for DFS')
    print(f'easy: {easy} \t medium: {medium} \t hard: {hard} \t evil: {evil}')

    #get memory for easy, medium, and evil for Greedy
    memory = memory_usage(greedyEasy, TIME_STEP)
    easy = max(memory) - base
    memory = memory_usage(greedyMedium, TIME_STEP)
    medium = max(memory) - base
    memory = memory_usage(greedyHard, TIME_STEP)
    hard = max(memory) - base
    memory = memory_usage(greedyEvil, TIME_STEP)
    evil = max(memory) - base
    print('\nMemory useage for Greedy')
    print(f'easy: {easy} \t medium: {medium} \t hard: {hard} \t evil: {evil}')




