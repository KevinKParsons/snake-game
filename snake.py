# Program:
# snake.py
# Snake Video Game with Autopilot Algorithm
#
# Description:
# This python program recreates the common video game concept, Snake. The objective of the game is to steer
# the snake towards the randomly placed food while avoiding running into the walls or any part of the snake.
# The game gets progressively more difficult as the snake grows because free space becomes increasingly
# limited. The program runs a path finding and decision making algorithm that plays the game automatically
# without user input. The autopilot  algorithm consists of several components, including a path finding
# algorithm and a contiguous free space finding algorithm.
#
# Algorithm:
# - Find path from snake head to food
# - If Path to food is found:
#   - Create future game board where snake has just completed the proposed path then recursively check 9
#       moves ahead to verify if snake will be safe by taking this path.
#        - Snake is safe if there is at least the minimum required contiguous free space.
#          Required minimum free space is a function of snake length.
#        - Snake is safe if it can pathfind to tail.
#   - If snake will be in a safe position after completing path to food:
#        - Take path.
#   - Else if snake will not be safe after completing path to food:
#        - Coil towards closest prioritized corner.
#        - Search through prioritized neighbor list to see which neighbors are free and then recursively
#        check 9 moves ahead to verify if snake is still safe.
#        - If safe neighboring tile is found:
#            - Take path.
#        - Else if no safe neighboring tile is found:
#            - Game Over!
# - Else if path to food is not found:
#   - Coil towards closest prioritized corner (See above).
# - If snake length == 256:
#   - Win!


# -------- Imports -------- #
from tkinter import Tk, Canvas, Label, Button, Frame, StringVar, N, W, S, E, CENTER
import datetime
from win32api import GetSystemMetrics  # Used to detect monitor setup
import time
import math
import random
import logging

RUNNING = 'running'  # Game is running
STOPPED = 'stopped'  # Game is stopped
FOOD = 'food'  # Tile state
SNAKE = 'snake'  # Tile state
FREE = 'free'  # Tile state
WALL = 'wall'  # Tile state (Manually placed walls)
HEAD = 'head'  # Tile visual
BODY = 'body'  # Tile visual
FILLER_LEFT = 'fillerLeft'  # Tile visual
FILLER_TOP = 'fillerTop'  # Tile visual
FILLER_RIGHT = 'fillerRight'  # Tile visual
FILLER_BOTTOM = 'fillerBottom'  # Tile visual
TAIL = 'tail'  # Tile visual
HIGHLIGHT = 'highlight'  # Tile visual
DEBUG_PATH_1 = 'debugPath1'  # Tile visual
DEBUG_PATH_2 = 'debugPath2'  # Tile visual
DEBUG_SPACE_1 = 'debugSpace1'  # Tile visual
DEBUG_SPACE_2 = 'debugSpace2'  # Tile visual
DEBUG_START = 'debugStart'  # Tile visual
DEBUG_END = 'debugEnd'  # Tile visual
PROJECTED_SNAKE = 'projectedSnake'  # Tile visual
PATH_TO_FOOD = 'PathToFood'  # Flag - Pathing Method
PATH_TO_TAIL = 'PathToTail'  # Flag - Pathing Method
SAFE = 'Safe'
NOT_SAFE = 'notSafe'
PATH = 'path'
NO_PATH = 'noPath'
PASS = 'pass'
FAILED = 'failed'
GRID_SIZE = 25
S = 'S'  # Object sizes on grid
M = 'M'
ML = 'ML'
L = 'L'
XL = 'XL'
SHAPE_LIBRARY = {
    'highlight': {
        'color': 'yellow',
        'outlineColor': 'black',
        'outlineWidth': 1,
        'size': S,
        'type': 'rectangle'
    },
    'debugPath1': {
        'color': 'deep sky blue',
        'outlineColor': 'black',
        'outlineWidth': 1,
        'size': S,
        'type': 'circle'
    },
    'debugPath2': {
        'color': 'light blue',
        'outlineColor': 'black',
        'outlineWidth': 1,
        'size': S,
        'type': 'circle'
    },
    'debugSpace1': {
        'color': 'MediumPurple3',
        'outlineColor': 'black',
        'outlineWidth': 1,
        'size': S,
        'type': 'circle'
    },
    'debugSpace2': {
        'color': 'MediumPurple1',
        'outlineColor': 'black',
        'outlineWidth': 1,
        'size': S,
        'type': 'circle'
    },
    'debugStart': {
        'color': 'Green3',
        'outlineColor': 'black',
        'outlineWidth': 3,
        'size': XL,
        'type': 'rectangleOutline'
    },
    'debugEnd': {
        'color': 'red',
        'outlineColor': 'black',
        'outlineWidth': 3,
        'size': XL,
        'type': 'rectangleOutline'
    },
    'head': {
        'color': 'SteelBlue1',
        'outlineColor': 'gray30',
        'outlineWidth': 1,
        'size': L,
        'type': 'rectangle'
    },
    'tail': {
        'color': 'gray30',
        'outlineColor': 'gray30',
        'outlineWidth': 1,
        'size': L,
        'type': 'rectangle'
    },
    'body': {
        'color': 'gray30',
        'outlineColor': 'gray30',
        'outlineWidth': 1,
        'size': L,
        'type': 'rectangle'
    },
    'fillerLeft': {
        'color': 'gray30',
        'outlineColor': 'gray30',
        'outlineWidth': 1,
        'size': L,
        'type': 'filler'
    },
    'fillerTop': {
        'color': 'gray30',
        'outlineColor': 'gray30',
        'outlineWidth': 1,
        'size': L,
        'type': 'filler'
    },
    'fillerRight': {
        'color': 'gray30',
        'outlineColor': 'gray30',
        'outlineWidth': 1,
        'size': L,
        'type': 'filler'
    },
    'fillerBottom': {
        'color': 'gray30',
        'outlineColor': 'gray30',
        'outlineWidth': 1,
        'size': L,
        'type': 'filler'
    },
    'projectedSnake': {
        'color': 'SkyBlue',
        'outlineColor': 'black',
        'outlineWidth': 1,
        'size': M,
        'type': 'rectangle'
    },
    'food': {
        'color': 'green3',
        'outlineColor': 'black',
        'outlineWidth': 1,
        'size': ML,
        'type': 'rectangle'
    },
    'wall': {
        'color': 'black',
        'outlineColor': 'black',
        'outlineWidth': 1,
        'size': L,
        'type': 'rectangle'
    }
}


# Logger
_LOGGER = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)  # Print debug and higher
# logging.basicConfig(level=logging.ERROR)  # Print debug and higher


class clsTile:
    def __init__(self, main, x, y):
        self.main = main
        self.x = x  # Tile x coordinate
        self.y = y  # Tile y coordinate
        self.quadrant = None  # Tile grid quadrant
        self.directionPriority = []  # Tile direction priority given tile location
        self.dist = None  # Tile distance holding variable
        self.prev = None  # Tile prev path holding variable
        self.state = {}  # Tile state holding variable
        for i in range(0, 10):
            self.state[i] = FREE  # Tile state for board
        self.setDirectionPriority()  # Get direction priority list given tile location
        self.seqNeighbors = []  # Populated during finishSetup() after all tiles created
        self.freeSpaceAfterMove = None  # Used to store free space after moving
        self.canvas = mainApp.w  # Tile canvas object
        self.xShape = self.x  # Tile canvas coordinate
        self.yShape = mainApp.canvasHeight - self.y  # Canvas y and material y coord system differ
        self.shapeCoords = {}  # Shape coordinates for shape objects
        for sizeClass, size in [(S, 6), (M, 8), (ML, 14), (L, 18), (XL, 48)]:
            self.shapeCoords[sizeClass] = self.xShape - 1 - size / 2, \
                                          self.yShape - 0 - size / 2, \
                                          self.xShape - 0 + size / 2, \
                                          self.yShape + 1 + size / 2  # 1px offsets to center shapes
        self.shape = {
            HIGHLIGHT: None,
            DEBUG_PATH_1: None,
            DEBUG_PATH_2: None,
            DEBUG_SPACE_1: None,
            DEBUG_SPACE_2: None,
            DEBUG_START: None,
            DEBUG_END: None,
            HEAD: None,
            TAIL: None,
            BODY: None,
            FILLER_LEFT: None,
            FILLER_TOP: None,
            FILLER_RIGHT: None,
            FILLER_BOTTOM: None,
            PROJECTED_SNAKE: None,
            FOOD: None,
            WALL: None
        }  # Dict of tiles shape objects on canvas

    def drawShape(self, shape):
        self.delShape(shape)
        if SHAPE_LIBRARY[shape]['type'] == 'filler':
            L, B, R, T = self.shapeCoords[SHAPE_LIBRARY[shape]['size']]
            if shape == FILLER_LEFT:
                L -= 12  # Adjust filler shapeCoords to the left one half tile
                R -= 12
            elif shape == FILLER_TOP:
                B -= 12
                T -= 12
            elif shape == FILLER_RIGHT:
                L += 12
                R += 12
            elif shape == FILLER_BOTTOM:
                B += 12
                T += 12
            self.shape[shape] = self.canvas.create_rectangle(L, B, R, T, fill=SHAPE_LIBRARY[shape]['color'],
                                                             outline=SHAPE_LIBRARY[shape]['outlineColor'],
                                                             width=SHAPE_LIBRARY[shape]['outlineWidth'])
        elif SHAPE_LIBRARY[shape]['type'] == 'rectangle':
            self.shape[shape] = self.canvas.create_rectangle(*self.shapeCoords[SHAPE_LIBRARY[shape]['size']],
                                                             fill=SHAPE_LIBRARY[shape]['color'],
                                                             outline=SHAPE_LIBRARY[shape]['outlineColor'],
                                                             width=SHAPE_LIBRARY[shape]['outlineWidth'])
        elif SHAPE_LIBRARY[shape]['type'] == 'circle':
            self.shape[shape] = self.canvas.create_oval(*self.shapeCoords[SHAPE_LIBRARY[shape]['size']],
                                                        fill=SHAPE_LIBRARY[shape]['color'],
                                                        outline=SHAPE_LIBRARY[shape]['outlineColor'],
                                                        width=SHAPE_LIBRARY[shape]['outlineWidth'])
        elif SHAPE_LIBRARY[shape]['type'] == 'rectangleOutline':
            self.shape[shape] = self.canvas.create_rectangle(*self.shapeCoords[SHAPE_LIBRARY[shape]['size']],
                                                             outline=SHAPE_LIBRARY[shape]['color'],
                                                             width=SHAPE_LIBRARY[shape]['outlineWidth'])

    def delShape(self, shape):  # Delete tiles shape by given type
        if self.shape[shape] is not None:
            self.canvas.delete(self.shape[shape])
            self.shape[shape] = None

    def getNeighborByDir(self, direction):  # Return neighbor tile by direction
        xMod, yMod = 0, 0
        if direction == 'U':
            xMod, yMod = 0, GRID_SIZE
        elif direction == 'D':
            xMod, yMod = 0, -GRID_SIZE
        elif direction == 'L':
            xMod, yMod = -GRID_SIZE, 0
        elif direction == 'R':
            xMod, yMod = GRID_SIZE, 0
        for tile in mainApp.Tiles:
            if (tile.x, tile.y) == (self.x + xMod, self.y + yMod):
                return tile
        return None

    def getSeqNeighbors(self):  # Return prioritized neighboring tile list
        neighborsList = [self.getNeighborByDir(self.directionPriority[0]),
                         self.getNeighborByDir(self.directionPriority[1]),
                         self.getNeighborByDir(self.directionPriority[2]),
                         self.getNeighborByDir(self.directionPriority[3])]
        return [tile for tile in neighborsList if tile is not None]  # Return list with 'None's removed

    def getFreeSeqNeighbors(self, board):  # Return prioritized FREE neighboring tile list
        return [tile for tile in self.seqNeighbors if tile.state[board] == FREE]

    def setDirectionPriority(self):
        if 8 * GRID_SIZE < self.x < 16 * GRID_SIZE and 8 * GRID_SIZE < self.y < 16 * GRID_SIZE:
            self.quadrant = 1   # Quadrant 1, Top Right
            self.directionPriority = ['U', 'R', 'L', 'D']
        elif 0 * GRID_SIZE < self.x < 8 * GRID_SIZE and 8 * 25 < self.y < 16 * GRID_SIZE:
            self.quadrant = 2   # Quadrant 2, Top Left
            self.directionPriority = ['U', 'L', 'R', 'D']
        elif 0 * GRID_SIZE < self.x < 8 * GRID_SIZE and 0 * GRID_SIZE < self.y < 8 * GRID_SIZE:
            self.quadrant = 3   # Quadrant 3, Bottom Left
            self.directionPriority = ['D', 'L', 'R', 'U']
        elif 8 * GRID_SIZE < self.x < 16 * GRID_SIZE and 0 * 25 < self.y < 8 * GRID_SIZE:
            self.quadrant = 4   # Quadrant 4, Bottom Right
            self.directionPriority = ['D', 'R', 'L', 'U']

    def flyToEndDistance(self, end):
        return math.sqrt(math.pow(self.x - end.x, 2) + math.pow(self.y - end.y, 2))


class clsPathfind:
    def __init__(self):
        self.tile = None
        self.frontier = []  # List of tiles to explore tiles to explore next
        self.explored = []  # List of tiles already explored
        self.solution = []  # Resulting optimized path

    def solve(self, start, end, board, method):  # Pathfind from start to end using given board and method
        self.reset()
        self.frontier.append(start)
        start.dist = 0  # Initialize pathfind start distance to 0
        if mainApp.oVisualDebug:
            mainApp.labelBoard_text.set('%s' % board)
        else:
            mainApp.labelBoard_text.set('-')

        if method == PATH_TO_FOOD:
            mainApp.labelAlgo_text.set('Pathfind to Food')
        if method == PATH_TO_TAIL:
            mainApp.labelAlgo_text.set('Pathfind to Tail')

        # Show the relevant board for visual debug
        if mainApp.oVisualDebug:
            start.drawShape(DEBUG_START)
            end.drawShape(DEBUG_END)
            if board != 0:
                mainApp.showProjectedBoard(board)

        # Creates a dict of board's snake's neighbors and their associated reverse snake index.
        # If any of these tiles gets explored and the path dist to the tile > rev index, then this tile
        # will be tail by time reached. Must check board's snake neighbors instead of snake, because snake
        # tiles are not FREE and wont be explored. Effectively looks for safety by path to tail or path to
        # what will be tail by the time head reaches that tile.
        if method == PATH_TO_TAIL:
            willBePassedFutureTailNodes = {}
            willBePassedFutureTailNodes.clear()
            for tile in mainApp.snake[board]:
                for neighbor in tile.seqNeighbors:
                    willBePassedFutureTailNodes[neighbor] = \
                        len(mainApp.snake[board]) - mainApp.snake[board].index(tile)

        while True:
            # If all tiles explored, return solution
            if len(self.frontier) == 0:
                if mainApp.oVisualDebug:
                    mainApp.deleteAllDebugVisuals()
                return NO_PATH, []

            # Sort tile list and choose first tile
            self.frontier.sort(key=lambda x: x.dist)  # Sort list in place for shortest dist first
            self.tile = self.frontier.pop(0)  # Select first tile and remove it from list

            # If reached tail or a part of snake body that will be tail by the time head is there and method
            # is PATH_TO_TAIL then return solution
            if method == PATH_TO_TAIL and self.tile in willBePassedFutureTailNodes.values() \
                    and self.tile.dist >= willBePassedFutureTailNodes[self.tile]:
                if mainApp.oVisualDebug:
                    mainApp.hideProjectedBoard()
                    mainApp.deleteAllDebugVisuals()
                raise ValueError('This never fires')
                return PATH_TO_TAIL, self.reverseTraceSolution(start, self.tile).copy()  # Use copy of list

            # If reached tail then return solution
            if method == PATH_TO_TAIL and self.tile == end:
                if mainApp.oVisualDebug:
                    mainApp.hideProjectedBoard()
                    mainApp.deleteAllDebugVisuals()
                return PATH_TO_TAIL, self.reverseTraceSolution(start, end).copy()  # Use copy of list

            # Draw visuals if they are enabled
            if mainApp.oVisualDebug:
                self.tile.drawShape(DEBUG_PATH_1)
                mainApp.root.update_idletasks()
                time.sleep(0.001)

            # If reached food tile and method is PATH_TO_FOOD then return solution
            if method == PATH_TO_FOOD and self.tile == end:
                if mainApp.oVisualDebug:
                    mainApp.hideProjectedBoard()
                    mainApp.deleteAllDebugVisuals()
                return PATH_TO_FOOD, self.reverseTraceSolution(start, end).copy()  # Use copy of list

            # Explore neighbors of selected tile
            for neighbor in self.tile.getFreeSeqNeighbors(board):  # Analyze FREE neighboring nodes
                if neighbor not in self.explored:
                    self.frontier.append(neighbor)
                    self.explored.append(neighbor)  # No neighbor node explored twice
                    if mainApp.oVisualDebug:
                        neighbor.drawShape(DEBUG_PATH_2)
                    if neighbor.dist > self.tile.dist + 1:
                        neighbor.dist = self.tile.dist + 1
                        neighbor.prev = self.tile

    def reverseTraceSolution(self, start, end):
        tile = end
        while tile != start:
            self.solution.insert(0, tile)
            tile = tile.prev
        return self.solution  # First element in self.solution is first step tile, not start tile

    def reset(self):
        for tile in mainApp.Tiles:  # Re-initialize all tiles.dist to large distance
            tile.dist = 999
        self.frontier.clear()
        self.explored.clear()
        self.solution.clear()


class clsFreeSpace:
    def __init__(self):
        self.tile = None
        self.frontier = []  # List of tiles to explore tiles to explore next
        self.explored = []  # List of tiles already explored

    def solve(self, start, board):  # Return size of contiguous free space around start with given board
        self.reset()
        self.frontier.append(start)

        if mainApp.oVisualDebug:
            mainApp.labelBoard_text.set('%s' % board)
        else:
            mainApp.labelBoard_text.set('-')

        mainApp.labelAlgo_text.set('Free Space')

        # Show the relevant board for visual debug
        if mainApp.oVisualDebug:
            mainApp.showProjectedBoard(board)

        while True:
            # If explored all tiles, return solution
            if len(self.frontier) == 0:
                if mainApp.oVisualDebug:
                    mainApp.hideProjectedBoard()
                    mainApp.deleteAllDebugVisuals()
                return len(self.explored)  # Return count of tiles explored

            # Select tile to explore
            self.tile = self.frontier.pop(0)  # Select first tile and remove from list

            # Draw visuals if they are enabled
            if mainApp.oVisualDebug:
                self.tile.drawShape(DEBUG_SPACE_1)
                mainApp.root.update_idletasks()
                time.sleep(0.001)

            # Explore neighbors of selected tile
            for neighbor in self.tile.getFreeSeqNeighbors(board):  # Explore FREE neighboring nodes
                if neighbor not in self.explored:
                    self.explored.append(neighbor)  # No neighbor node explored twice
                    self.frontier.append(neighbor)
                    if mainApp.oVisualDebug:
                        neighbor.drawShape(DEBUG_SPACE_2)

    def reset(self):
        self.frontier.clear()
        self.explored.clear()


class clsMainApp:
    def __init__(self, root):
        print('\nRunning...')
        self.root = root
        self.cycleTime = 50  # Core loop time (ms)
        self.iteration = 0  # Iteration count
        self.queueStop = False  # Queue stop request
        self.queueReset = False  # Queue reset request
        self.setPause = False  # Set pause state
        self.oVisualDebug = False  # Frozen working copy of visualDebugSetting
        self.visualDebugSetting = False  # Toggle for turning on debugging visuals
        self.pauseForBoards = True  # Toggle for pausing when future boards displayed
        self.showCurrentBoardEveryIter = False  # Toggle to show current board at end of every iteration
        self.iterationStartTime = None  # Timestamp of current iteration start
        self.mode = None
        self.messagePop = None
        self.runStatus = STOPPED
        self.pathfind = clsPathfind()
        self.freeSpace = clsFreeSpace()
        self.Tiles = []
        self.snakeLength = 2  # Initial snake length
        self.snake = {}  # Dict of snakes for each board (0-9), each with list of snake tiles
        for i in range(0, 10):  # Snake[0] = Current Board's snake list of tile objects, head first
            self.snake[i] = []  # Snake[0][0] = Current snake head tile object
        self.head = None
        self.tail = None
        self.food = None
        self.freeSpaceForEachMove = {}

        # Window Setup
        self.root.title("Snake")
        self.root.configure(bg='white')
        self.appWidth = 800  # Overall window width
        self.appHeight = 800  # Overall window height
        self.canvasWidth = 400  # Canvas Width
        self.canvasHeight = 400  # Canvas Height
        self.combinedSW = GetSystemMetrics(78)  # Combined multi-monitor width
        self.sw = root.winfo_screenwidth()  # Single monitor width
        self.sh = root.winfo_screenheight()
        if self.combinedSW < 2600:
            self.screenType = 'Single'  # Single screen
            self.root.geometry('+%d+%d' % (self.sw - self.appWidth - 800,
                                           self.sh - self.appHeight - 300))
        else:
            self.screenType = 'Dual'  # Dual screen
            self.root.geometry('+%d+%d' % (self.sw - self.appWidth + 1500,
                                           self.sh - self.appHeight - 180))

        # Frames
        topFrame = Frame(root, bg='#4682B4', padx=20, pady=20)
        middleFrame = Frame(root, bg='white', padx=20, pady=20)
        bottomFrame = Frame(root, bg='#4682B4', padx=20, pady=20)
        topFrame.pack(fill='x'), middleFrame.pack(expand=1, fill='both'), bottomFrame.pack(fill='both')

        # Top Frame Widgets
        self.labelSnakeTitle = Label(
            topFrame, text='Length', width=10, borderwidth=1, relief="solid", pady=4)
        self.labelSnake_text = StringVar()
        self.labelSnake_text.set('-')
        self.labelSnake = Label(
            topFrame, textvariable=self.labelSnake_text, borderwidth=1, relief="solid", pady=4,
                                font=("Courier", 26), bg="white")

        self.labelBoardTitle = Label(
            topFrame, text='Board', width=10, borderwidth=1, relief="solid", pady=4)
        self.labelBoard_text = StringVar()
        self.labelBoard_text.set('-')
        self.labelBoard = Label(topFrame, textvariable=self.labelBoard_text, borderwidth=1,
                                relief="solid", pady=4, font=("Courier", 26), bg="white")

        self.labelMessageTitle = Label(
            topFrame, text='Algorithm', width=38, borderwidth=1, relief="solid", pady=4)
        self.labelMessage_text = StringVar()
        self.labelMessage_text.set('-')
        self.labelMessage = Label(topFrame, textvariable=self.labelMessage_text, borderwidth=1,
                                  relief="solid", pady=4, bg="white")

        self.labelAlgoTitle = Label(
            topFrame, text='Pathing', width=40, borderwidth=1, relief="solid", pady=4)
        self.labelAlgo_text = StringVar()
        self.labelAlgo_text.set('-')
        self.labelAlgo = Label(topFrame, textvariable=self.labelAlgo_text, borderwidth=1,
                               relief="solid", pady=4, bg="white")

        # Middle Frame Widgets
        self.w = Canvas(middleFrame, width=self.canvasWidth, height=self.canvasHeight, bg='white',
                        borderwidth=2, highlightthickness=1, relief='groove')

        # Create grid lines
        for i in range(0, self.canvasWidth, 25):
            self.w.create_line([(i, 0), (i, self.canvasHeight)], tag='grid_line', fill='grey85')
        for i in range(0, self.canvasHeight, 25):
            self.w.create_line([(0, i), (self.canvasWidth, i)], tag='grid_line', fill='grey85')

        # Bottom Frame Widgets
        self.startButton = Button(bottomFrame, text='Start', command=self.start, width=11,
                                  borderwidth=1, relief="ridge", bg='white')
        self.resetButton = Button(bottomFrame, text='Reset', command=self.requestReset, width=11,
                                  borderwidth=1, relief="ridge", bg='white')
        self.pauseButton = Button(bottomFrame, text='Pause', command=self.togglePause, width=11,
                                  borderwidth=1, relief="ridge", bg='white')
        self.skipButton = Button(bottomFrame, text='Skip', command=self.skipAhead, width=11,
                                 borderwidth=1, relief="ridge", bg='white')
        self.visualsButton = Button(bottomFrame, text='Visuals', command=self.toggleVisuals, width=11,
                                    borderwidth=1, relief="ridge", bg='white')
        self.fastButton = Button(bottomFrame, text='Fast', command=self.setFastSpeed, width=11,
                                 borderwidth=1, relief="ridge", bg='white')
        self.normalButton = Button(bottomFrame, text='Normal', command=self.setNormalSpeed, width=11,
                                   borderwidth=1, relief="ridge", bg='white')
        self.slowButton = Button(bottomFrame, text='Slow', command=self.setSlowSpeed, width=11,
                                 borderwidth=1, relief="ridge", bg='white')
        self.crawlButton = Button(bottomFrame, text='Crawl', command=self.setCrawlSpeed, width=11,
                                  borderwidth=1, relief="ridge", bg='white')

        self.labelSnakeTitle.grid(row=1, column=1, pady=(0, 0), sticky=W + E + S + N)
        self.labelSnake.grid(row=2, column=1, rowspan=3, pady=(0, 0), sticky=W + E + S + N)
        self.labelBoardTitle.grid(row=1, column=2, pady=(0, 0), sticky=W + E + S + N)
        self.labelBoard.grid(row=2, column=2, rowspan=3, pady=(0, 0), sticky=W + E + S + N)
        self.labelMessageTitle.grid(row=1, column=3, pady=(0, 0), sticky=W + E + S + N)
        self.labelMessage.grid(row=2, column=3, pady=(0, 0), sticky=W + E + S + N)
        self.labelAlgoTitle.grid(row=3, column=3, pady=(0, 0), sticky=W + E + S + N)
        self.labelAlgo.grid(row=4, column=3, pady=(0, 0), sticky=W + E + S + N)

        topFrame.columnconfigure(0, weight=1)
        topFrame.columnconfigure(4, weight=1)

        self.w.pack(expand=1)

        self.startButton.grid(row=0, column=1, sticky=W + E)
        self.resetButton.grid(row=0, column=2, sticky=W + E)
        self.pauseButton.grid(row=0, column=3, sticky=W + E)
        self.skipButton.grid(row=0, column=4, sticky=W + E)
        self.visualsButton.grid(row=0, column=5, sticky=W + E)
        self.fastButton.grid(row=1, column=1, sticky=W + E)
        self.normalButton.grid(row=1, column=2, sticky=W + E)
        self.slowButton.grid(row=1, column=3, sticky=W + E)
        self.crawlButton.grid(row=1, column=4, sticky=W + E)

        bottomFrame.columnconfigure(0, weight=1)
        bottomFrame.columnconfigure(6, weight=1)

        self.root.update_idletasks()  # Update window geometry

    def finishSetup(self):  # Run finishSetup after initializing mainApp
        self.createTiles()
        self.setTileNeighbors()
        self.setNormalSpeed()

    def createTiles(self):  # Create each tile object, append to Tiles
        for i in range(13, self.canvasWidth, 25):
            for j in range(13, self.canvasHeight, 25):
                self.Tiles.append(clsTile(self, i, j))

    def setTileNeighbors(self):  # Create a list seq neighbors for each tile
        for tile in self.Tiles:
            tile.seqNeighbors = tile.getSeqNeighbors()

    def initializeSnake(self):  # Init snake to random location then move
        start = mainApp.Tiles[random.randint(0, 255)]  # Random initial starting location
        self.moveHead(start)  # Initialize snake[] with first tile
        self.moveHead(random.choice(start.getFreeSeqNeighbors(0)))  # Move in random FREE direction
        self.markTail()  # Mark last tile in snake[] as tail

    def skipAhead(self):
        self.snakeLength = self.snakeLength + 60

    def start(self):
        if self.runStatus == STOPPED and not self.setPause:
            mainApp.reset()
            self.runStatus = RUNNING
            self.run()

    def messageUpdate(self, printMsg, labelMsg, labelColor):
        print(printMsg)
        self.labelMessage_text.set(labelMsg)
        self.labelMessage.configure(bg=labelColor)

    def reset(self):
        self.setPause = False  # Reset buttons if they are set
        self.pauseButton.configure(bg='white')
        self.visualDebugSetting = False  # Reset buttons if they are set
        self.visualsButton.configure(bg='white')

        for i in range(0, 10):
            self.snake[i].clear()  # Clear Snake list for all boards
        self.snakeLength = 2
        self.iteration = 0

        for tile in self.Tiles:
            for i in range(0, 10):
                tile.state[i] = FREE
            tile.delShape(HIGHLIGHT)
            tile.delShape(HEAD)
            tile.delShape(BODY)
            tile.delShape(TAIL)
            tile.delShape(WALL)
            tile.delShape(FILLER_LEFT)
            tile.delShape(FILLER_TOP)
            tile.delShape(FILLER_RIGHT)
            tile.delShape(FILLER_BOTTOM)

        self.initializeSnake()
        self.spawnFood()  # Initial food location
        if mainApp.messagePop is not None:
            mainApp.messagePop.place_forget()

    def toggleVisuals(self):
        if self.visualDebugSetting:
            self.visualDebugSetting = False
            self.visualsButton.configure(bg='white')
        else:
            self.visualDebugSetting = True
            self.visualsButton.configure(bg='gray70')

    def togglePause(self):
        if self.setPause:
            self.setPause = False
            self.pauseButton.configure(bg='white')
            self.showProjectedBoard(0)
            self.hideProjectedBoard()
            self.root.after(50, self.run)
        else:
            self.setPause = True
            self.queueStop = True
            self.pauseButton.configure(bg='gray70')

    def requestReset(self):
        if self.runStatus == RUNNING:
            self.queueStop = True
            self.queueReset = True
        else:
            self.reset()

    def setFastSpeed(self):
        self.cycleTime = 10
        self.fastButton.configure(bg='gray70')
        self.normalButton.configure(bg='white')
        self.slowButton.configure(bg='white')
        self.crawlButton.configure(bg='white')

    def setNormalSpeed(self):
        self.cycleTime = 50
        self.fastButton.configure(bg='white')
        self.normalButton.configure(bg='gray70')
        self.slowButton.configure(bg='white')
        self.crawlButton.configure(bg='white')

    def setSlowSpeed(self):
        self.cycleTime = 150
        self.fastButton.configure(bg='white')
        self.normalButton.configure(bg='white')
        self.slowButton.configure(bg='gray70')
        self.crawlButton.configure(bg='white')

    def setCrawlSpeed(self):
        self.cycleTime = 500
        self.fastButton.configure(bg='white')
        self.normalButton.configure(bg='white')
        self.slowButton.configure(bg='white')
        self.crawlButton.configure(bg='gray70')

    def highlightPathSolution(self, solution):
        self.delHighlightPathSolution()
        for tile in solution[:-1]:  # Highlight solution except the last tile which is food
            tile.drawShape(HIGHLIGHT)

    def delHighlightPathSolution(self):
        for tile in self.Tiles:
            tile.delShape(HIGHLIGHT)

    def showProjectedBoard(self, board):  # Show projected snake visuals
        for tile in self.Tiles:
            if tile.state[board] == SNAKE:
                tile.drawShape(PROJECTED_SNAKE)  # Draw shapes for PROJECTED_SNAKE

    def hideProjectedBoard(self):
        for tile in self.Tiles:
            tile.delShape(PROJECTED_SNAKE)  # Remove all shapes for PROJECTED_SNAKE

    def deleteAllDebugVisuals(self):
        for tile in self.Tiles:
            tile.delShape(DEBUG_PATH_1)
            tile.delShape(DEBUG_PATH_2)
            tile.delShape(DEBUG_SPACE_1)
            tile.delShape(DEBUG_SPACE_2)
            tile.delShape(DEBUG_START)
            tile.delShape(DEBUG_END)

    def moveHead(self, newHead):
        if len(self.snake[0]) > 0:
            self.snake[0][0].delShape(HEAD)
            self.snake[0][0].drawShape(BODY)
        self.snake[0].insert(0, newHead)  # Add new head tile to start of snake []
        newHead.state[0] = SNAKE

        if len(self.snake[0]) > 1:
            if newHead.x > self.snake[0][1].x:
                newHead.drawShape(FILLER_LEFT)  # Determine which dir head came from and draw filler
            elif newHead.x < self.snake[0][1].x:
                newHead.drawShape(FILLER_RIGHT)
            elif newHead.y > self.snake[0][1].y:
                newHead.drawShape(FILLER_BOTTOM)
            elif newHead.y < self.snake[0][1].y:
                newHead.drawShape(FILLER_TOP)

        newHead.drawShape(HEAD)  # Mark snake head color

    def checkTail(self):
        if len(self.snake[0]) > self.snakeLength:
            self.snake[0][-1].delShape(TAIL)
            self.snake[0][-1].state[0] = FREE
            del self.snake[0][-1]
            self.snake[0][-1].delShape(FILLER_LEFT)
            self.snake[0][-1].delShape(FILLER_RIGHT)
            self.snake[0][-1].delShape(FILLER_BOTTOM)
            self.snake[0][-1].delShape(FILLER_TOP)
            self.markTail()

    def markTail(self):
        # Tail should be marked with tail shape, but state set to FREE state because it is valid for
        # the head to move to the tail space because the tail will move away at same time. This also
        # enables valid pathfinding to tail as it can only explore FREE tail tiles. Do not mark tail
        # as FREE if snakeLength == 2 or else snake can reverse through tail, which is not valid.
        if self.snakeLength > 2:
            self.snake[0][-1].state[0] = FREE  # Mark tail as FREE, except when short enough to reverse
        self.snake[0][-1].delShape(BODY)
        self.snake[0][-1].drawShape(TAIL)

    def checkFood(self):
        if self.snake[0][0] == self.food:
            self.snakeLength += 1
            self.labelSnake_text.set('%i' % self.snakeLength)
            self.spawnFood()

    def spawnFood(self):
        while True:
            tile = self.Tiles[random.randint(0, len(self.Tiles) - 1)]  # Pick a random tile in Tiles
            if tile.state[0] == FREE and tile not in self.snake:  # Don't pick FREE tail tile
                if self.food is not None:
                    self.food.delShape(FOOD)
                tile.drawShape(FOOD)
                self.food = tile
                break

    def checkSafety(self, board):
        tailSafe = self.checkPathToTail(board)
        freeSpaceSafe = self.checkFreeSpace(board)
        if tailSafe == SAFE or freeSpaceSafe == SAFE:
            return SAFE
        else:
            return NOT_SAFE

    def checkPathToTail(self, board):  # Note that tail must be marked as FREE for pathfinding
        tailPathStatus, tailPath = self.pathfind.solve(
            self.snake[board][0], self.snake[board][-1], board, PATH_TO_TAIL)
        if tailPathStatus == NO_PATH:
            print('[Safety Check][Check Path To Tail][Board %i] - Did Not Find Path to Tail' % board)
            return NOT_SAFE
        elif tailPathStatus == PATH_TO_TAIL:
            print('[Safety Check][Check Path To Tail][Board %i] - Did Find Path to Tail' % board)
            return SAFE
        else:
            print('Debug: %s' % tailPathStatus)
            raise ValueError('Invalid Value Found Here')  # Raise error if invalid values

    def checkFreeSpace(self, board):
        # Important to have a large margin on minFreeSpace late in the game because the snake can
        # possibly orphan off a large portion of the free space and be unable to utilize it.
        freeSpace = mainApp.freeSpace.solve(self.snake[board][0], board)
        reqFreeSpace = int(self.snakeLength * 1.5)
        if freeSpace >= reqFreeSpace:
            print('[Safety Check][Check Free Space][Board %i] - Enough Free Space: %i / %i'
                  % (board, freeSpace, reqFreeSpace))
            return SAFE
        else:
            print('[Safety Check][Check Free Space][Board %i] - Not Enough Free Space: %i / %i'
                  % (board, freeSpace, reqFreeSpace))
            return NOT_SAFE

    def generateBoard(self, board, projectedSnake):
        self.clearBoard(board)  # Marks every tile as FREE on board
        for tile in mainApp.Tiles:
            if tile.state[0] == WALL:
                tile.state[board] = WALL
        for tile in projectedSnake:
            tile.state[board] = SNAKE
        projectedSnake[-1].state[board] = FREE  # Mark tail as free since it is FREE for current move

    def clearBoard(self, board):
        for tile in self.Tiles:
            tile.state[board] = FREE

    @staticmethod
    def getProjectedSnake(projectedPath, currentSnake):  # Creates projected snake from projected path
        combinedPath = projectedPath + currentSnake
        return combinedPath[:mainApp.snakeLength]  # Return snakeLength elements of combined path

    def checkGameEndConditions(self):
        if len(self.snake) >= 256:
            _LOGGER.debug('Win!')
            self.messagePop = Label(self.w, text='Win!', width=30, bg='Green', fg='white',
                                    wraplength=300, borderwidth=1, relief="solid", font=('Helvetica', 16))
            self.messagePop.place(relx=0.5, rely=0.85, anchor=CENTER)
            self.queueStop = True

        if len(self.snake[0][0].getFreeSeqNeighbors(0)) == 0:
            _LOGGER.debug('Game Over!')
            self.messagePop = Label(self.w, text='Game Over!', width=30, bg='Green', fg='white',
                                    wraplength=300, borderwidth=1, relief="solid", font=('Helvetica', 16))
            self.messagePop.place(relx=0.5, rely=0.85, anchor=CENTER)
            self.queueStop = True

    def recursivePrioritizedNeighborsCheck(self, board):
        if board == 8:
            return PASS, self.snake[1][0]  # Break out of recursion and return next move's head
        freeSeqNeighbors = self.snake[board][0].getFreeSeqNeighbors(board)
        for tile in freeSeqNeighbors:
            self.snake[board + 1] = self.getProjectedSnake([tile], self.snake[board])
            self.generateBoard(board + 1, self.snake[board + 1])
            if self.checkSafety(board + 1) in [SAFE]:
                return self.recursivePrioritizedNeighborsCheck(board + 1)
        return FAILED, None

    def cornerCoilByMaintainingFreeSpaceGuessing(self):
        # Corner coil as long as >80% of best free space maintained
        print('No Guaranteed Safe Moves Found! Proceeding by best guess anyways.')
        self.messageUpdate('[Move Method] - Corner coil while preserving max space',
                           'Corner coil while preserving max space', '#FF6565')

        self.checkGameEndConditions()  # Game over if no more possible moves

        # Look at all possible next moves and get free space remaining after each move
        self.freeSpaceForEachMove.clear()
        for neighbor in self.snake[0][0].getFreeSeqNeighbors(0):
            self.snake[1] = self.getProjectedSnake([neighbor], self.snake[0].copy())  # Use copy of list
            self.generateBoard(1, self.snake[1])
            self.freeSpaceForEachMove[neighbor] = self.freeSpace.solve(self.snake[1][0], 1)

        # Find max free space left after best move
        print('***Number of neighbors %i' % len(self.snake[0][0].seqNeighbors))
        print('***Number of free neighbors %i' % len(self.snake[0][0].getFreeSeqNeighbors(0)))
        for item in self.snake[0][0].seqNeighbors:
            print('***seqNeighbor state %s' % item.state[0])
        maxFreeSpace = max(value for key, value in self.freeSpaceForEachMove.items())
        print('***Max free space: %i' % maxFreeSpace)

        # Make next move based on corner coil priority as long as > 80% of best free space is maintained
        for tile in self.snake[0][0].getFreeSeqNeighbors(0):
            # maxFreeSpace == 0 occurs when head chases tail closely, but move is safe
            if maxFreeSpace == 0 or self.freeSpaceForEachMove[tile] / maxFreeSpace >= 0.8:
                self.moveHead(tile)
                break

    def run(self):
        print('\n#%i' % self.iteration)

        self.iterationStartTime = datetime.datetime.now()

        # --------- Path Planning Algo -------- #

        # Find path to food
        print('[Path To Food Search] - Start')
        foodPathStatus, foodPath = self.pathfind.solve(self.snake[0][0], self.food, 0, 'PathToFood')
        self.highlightPathSolution(foodPath)

        # If path to food is found
        if foodPathStatus in [PATH_TO_FOOD]:

            # Generate board, 9, where snake has just eaten the food
            self.snake[9] = self.getProjectedSnake(list(reversed(foodPath.copy())),
                                                   self.snake[0].copy())  # Use copy of list
            self.generateBoard(9, self.snake[9])

            # Check if path to food is safe and make it the next move if it is
            foodPathSafety = self.checkSafety(9)
            if foodPathSafety in [SAFE]:
                self.moveHead(foodPath[0])  # Next tile is first tile in solution
                self.messageUpdate('[Move Method] - Pathfind to Food', 'Path to Food', '#C6E0B4')

        # If no path to food found or path is found, but not safe
        if foodPathStatus in [NO_PATH] or foodPathSafety in [NOT_SAFE]:

            print('[Recursive Search] - Start')
            recursionStatus, recursionNextMove = self.recursivePrioritizedNeighborsCheck(0)  # Pass board 0
            if recursionStatus in [PASS]:  # Recursively check all possible next moves by priority
                # Next snake head is the tile to move to when recursion hits break
                self.moveHead(recursionNextMove)
                print('[Recursive Search][Safety Check] - Passed')
                self.messageUpdate('[Move Method] - Coil in Corner (Checked 8 moves ahead)',
                                   'Coil in Corner - Recursive', '#FFE699')
            elif recursionStatus in [FAILED]:
                print('[Recursive Search][Safety Check] - Failed')
                # No proven safe moves found, proceed by corner coil as long as
                # it preserves >80% possible free space
                self.cornerCoilByMaintainingFreeSpaceGuessing()

        # --------- Core Mechanics -------- #

        self.checkTail()  # Check and remove tail if needed
        self.checkFood()  # Check if ate the food
        self.checkGameEndConditions()  # Check for game end conditions
        self.oVisualDebug = self.visualDebugSetting  # Frozen working copy of VisualDebug switch for iter
        iterationTime = int((datetime.datetime.now() - self.iterationStartTime).total_seconds() * 1000)
        delay = int(self.cycleTime - iterationTime)
        if delay < 1:
            delay = 1  # Must be at least 1 or error
        self.iteration += 1

        if not self.queueStop:  # Check for game stop request
            self.runStatus = RUNNING
            self.root.after(delay, self.run)  # Loop after delay ms
        else:
            self.queueStop = False
            self.runStatus = STOPPED

        if self.queueReset and self.runStatus == STOPPED:  # Check for game reset request
            self.queueReset = False
            self.reset()


# -------- Main -------- #

if __name__ == '__main__':
    root = Tk()
    mainApp = clsMainApp(root)
    mainApp.finishSetup()
    mainApp.requestReset()
    root.mainloop()
