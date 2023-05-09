VERTICAL_WALL_EDGE = "|"
VERTICAL_WALL = "'"
CENTER_GROUND = "_"
RIGHT_GROUND = "\\"
LEFT_GROUND = "/"
CENTER_ROOF = "_"
LEFT_ROOF = "\\"
RIGHT_ROOF = "/"

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
SQUARE_SIZES = [6, 6, 4, 2]

FIRST_SQUARES_SIZE = 5
SECOND_SQUARES_SIZE = 6
THIRD_SQUARES_SIZE = 4
FOURTH_SQUARES_HEIGHT = 2
SCREEN_HEIGHT = (FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE + FOURTH_SQUARES_HEIGHT) * 2
SCREEN_WIDTH = int(SCREEN_HEIGHT * 1.3)

MAZE_WIDTH = 21
MAZE_HEIGHT = 21
myMaze = [[False] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]
myHero = [1, 1, 2]  # [y, x, direction]


def buildMaze(maze):
    for row in range(MAZE_HEIGHT):
        for column in range(MAZE_WIDTH):
            if (row == 0) or (row == MAZE_HEIGHT - 1) or (column == 0) or (column == MAZE_WIDTH - 1):
                maze[row][column] = True
            if (row % 2 == 0) and (column % 2 == 0):
                maze[row][column] = True


def displayMaze2D(maze, hero):
    for row in range(MAZE_HEIGHT):
        for column in range(MAZE_WIDTH):
            if hero[0] == row and hero[1] == column:
                print("0", end="")
            elif maze[row][column]:
                print("X", end="")
            else:
                print(" ", end="")
        print()


def displayMaze3D(maze, hero):
    screen = createEmptyScreen()
    addSquaresByDistanceInScreen(hero, maze, screen, 1)
    addSquaresByDistanceInScreen(hero, maze, screen, 0)
    # addSquaresByDistanceInScreen(hero, maze, screen, 2)
    # addSquaresByDistanceInScreen(hero, maze, screen, 3)
    printScreen(screen)


def createEmptyScreen():
    return [[" "] * SCREEN_WIDTH for _ in range(SCREEN_HEIGHT)]


def addSquaresByDistanceInScreen(hero, maze, screen, distance):
    leftSquareIsAWall = getSquareOfPositionRelativeToHero(hero, maze, -1, distance)
    frontSquareIsAWall = getSquareOfPositionRelativeToHero(hero, maze, 0, distance)
    rightSquareIsAWall = getSquareOfPositionRelativeToHero(hero, maze, 1, distance)
    squareSize = getSquareSizeByDistance(distance)
    previousSquareSizes = getPreviousSquareSizeByDistance(distance)
    previousSquareSize = getSquareSizeByDistance(distance - 1)
    if leftSquareIsAWall:
        for i in range(squareSize):
            for j in range(previousSquareSizes + i, SCREEN_HEIGHT - previousSquareSizes - i):
                screen[j][previousSquareSizes + i] = VERTICAL_WALL_EDGE if (
                        (i == 0) or (i == squareSize-1)) else VERTICAL_WALL
        for i in range(previousSquareSizes):
            screen[previousSquareSizes - 1][i] = CENTER_ROOF
            for j in range(previousSquareSizes, SCREEN_HEIGHT - previousSquareSizes - 1):
                screen[j][previousSquareSizes - previousSquareSize + i] = VERTICAL_WALL
    if rightSquareIsAWall:
        for i in range(squareSize):
            for j in range(previousSquareSizes + i, SCREEN_HEIGHT - previousSquareSizes - i):
                screen[j][SCREEN_WIDTH - previousSquareSizes - i - 1] = VERTICAL_WALL_EDGE if (
                        (i == 0) or (i == squareSize-1)) else VERTICAL_WALL
        for i in range(previousSquareSizes):
            screen[previousSquareSizes - 1][SCREEN_WIDTH - i - 1] = CENTER_ROOF
            for j in range(previousSquareSizes, SCREEN_HEIGHT - previousSquareSizes - 1):
                screen[j][SCREEN_WIDTH - (previousSquareSizes - previousSquareSize + i) - 1] = VERTICAL_WALL
    if frontSquareIsAWall:
        for i in range(previousSquareSizes, SCREEN_HEIGHT - previousSquareSizes):
            screen[i][previousSquareSizes - 1] = VERTICAL_WALL_EDGE
            screen[i][SCREEN_WIDTH - previousSquareSizes] = VERTICAL_WALL_EDGE
        for i in range(previousSquareSizes, SCREEN_WIDTH - previousSquareSizes):
            screen[previousSquareSizes - 1][i] = CENTER_ROOF
    else:
        for i in range(previousSquareSizes, previousSquareSizes + squareSize):
            screen[SCREEN_HEIGHT - 1 - i][i] = LEFT_GROUND
            screen[SCREEN_HEIGHT - 1 - i][SCREEN_WIDTH - 1 - i] = RIGHT_GROUND
        for i in range(previousSquareSizes + squareSize,
                       SCREEN_WIDTH - previousSquareSizes - squareSize):
            screen[SCREEN_HEIGHT - previousSquareSizes - squareSize - 1][i] = CENTER_GROUND
        if leftSquareIsAWall:
            for i in range(previousSquareSizes + squareSize,
                           SCREEN_HEIGHT - previousSquareSizes - squareSize):
                screen[i][previousSquareSizes + squareSize - 1] = VERTICAL_WALL_EDGE
            for i in range(previousSquareSizes, previousSquareSizes + squareSize):
                screen[i][i] = LEFT_ROOF
        else:
            for i in range(previousSquareSizes, previousSquareSizes + squareSize):
                screen[SCREEN_HEIGHT - previousSquareSizes - squareSize - 1][i] = CENTER_GROUND
        if rightSquareIsAWall:
            for i in range(previousSquareSizes + squareSize,
                           SCREEN_HEIGHT - previousSquareSizes - squareSize):
                screen[i][SCREEN_WIDTH - previousSquareSizes - squareSize] = VERTICAL_WALL_EDGE
            for i in range(previousSquareSizes, previousSquareSizes + squareSize):
                screen[i][SCREEN_WIDTH - 1 - i] = RIGHT_ROOF
        else:
            for i in range(previousSquareSizes, previousSquareSizes + squareSize):
                screen[SCREEN_HEIGHT - previousSquareSizes - squareSize - 1][
                    SCREEN_WIDTH - i - 1] = CENTER_GROUND


def getSquareOfPositionRelativeToHero(hero, maze, x, y):
    if hero[2] == NORTH:
        return maze[hero[0] - y][hero[1] + x]
    elif hero[2] == EAST:
        return maze[hero[0] + x][hero[1] + y]
    elif hero[2] == SOUTH:
        return maze[hero[0] + y][hero[1] - x]
    elif hero[2] == WEST:
        return maze[hero[0] - x][hero[1] - y]


def getSquareSizeByDistance(distance):
    return SQUARE_SIZES[distance]


def getPreviousSquareSizeByDistance(distance):
    if distance == 0:
        return 0
    else:
        return SQUARE_SIZES[distance] + getPreviousSquareSizeByDistance(distance - 1)


def printScreen(screen):
    for row in range(SCREEN_HEIGHT):
        for column in range(SCREEN_WIDTH):
            print(screen[row][column], end="")
        print()


buildMaze(myMaze)
displayMaze2D(myMaze, myHero)
displayMaze3D(myMaze, myHero)
