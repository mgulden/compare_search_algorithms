from maze_dataset import MazeDataset, MazeDatasetConfig
from maze_dataset.generation import LatticeMazeGenerators
from maze_dataset.maze.lattice_maze import AsciiChars
import numpy as np
import heapq
from collections import deque
import time
import random
import matplotlib.pyplot as plt

class MazeSymbols:
    START:int=-1
    END:int=-1
    OPEN:int=0
    WALL:int=1

class Maze():
    def __init__(self,ary,start,end):
        self.maze_cells = ary
        pass
    maze_cells:np.array
    start:tuple[int,int]
    end:tuple[int,int]

def generate_maze(grid_num:int=5):
    """Returns 3d npArray that contains generates maze definitions
    #1st dimesion: mazes
    #2nd dimension: rows
    #3rd dimesnison: cols
    Values: '0' for empty cells, '1' for walls,
            'S' for start cells, 'E' for end cells
    """
    cfg: MazeDatasetConfig = MazeDatasetConfig(
        name="Mazes", # name is only for you to keep track of things
        grid_n=grid_num, # number of rows/columns in the lattice
        n_mazes=1, # number of mazes to generate
        maze_ctor=LatticeMazeGenerators.gen_dfs, # algorithm to generate the maze
        maze_ctor_kwargs=dict(do_forks=True), # additional parameters to pass to the maze generation algorithm
    )

    #For maze generation we use made-dataset module: ref:https://arxiv.org/abs/2309.01049
    dataset: MazeDataset = MazeDataset.from_config(cfg)
    m = dataset[0]
    strMaze = m.as_ascii(show_solution=False)

    ary = np.zeros((grid_num,grid_num),dtype=int)
    aryMazeRows = strMaze.split(sep="\n")
    for rowIndex,row in enumerate(aryMazeRows):
        for colIndex,cell in enumerate(row):
            if cell==AsciiChars.END:
                ary[rowIndex,colIndex] = MazeSymbols.OPEN
                end = (rowIndex,colIndex)
            elif cell==AsciiChars.START:
                ary[rowIndex,colIndex] = MazeSymbols.OPEN
                start = (rowIndex,colIndex)
            elif cell==AsciiChars.WALL:
                ary[rowIndex,colIndex] = MazeSymbols.WALL
            elif cell==AsciiChars.OPEN  or cell==AsciiChars.PATH:
                ary[rowIndex,colIndex] = MazeSymbols.OPEN
                
    return Maze(ary,start,end)

res = generate_maze(5)

a=1