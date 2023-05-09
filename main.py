VERTICAL_WALL_EDGE = "|"
VERTICAL_WALL = "'"
CENTER_GROUND = "-"
RIGHT_GROUND = "\\"
LEFT_GROUND = "/"
CENTER_ROOF = "_"
LEFT_ROOF = "\\"
RIGHT_ROOF = "/"

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
SQUARE_SIZES = [5, 9, 7, 5, 4, 3]

SCREEN_HEIGHT = sum(SQUARE_SIZES) * 2 + 1
SCREEN_WIDTH = int(SCREEN_HEIGHT * 1.1)

MAZE_WIDTH = 21
MAZE_HEIGHT = 11
myMaze = [[False] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]
myHero = [1, 3, 1]  # [y, x, direction]


def buildMaze(maze):
    for row in range(MAZE_HEIGHT):
        for column in range(MAZE_WIDTH):
            if (row == 0) or (row == MAZE_HEIGHT - 1) or (column == 0) or (column == MAZE_WIDTH - 1):
                maze[row][column] = True
            if (row % 3 == 0) and (column % 3 == 0):
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
    for distance in range(len(SQUARE_SIZES) - 1, -1, -1):
        addSquaresByDistanceInScreen(hero, maze, screen, distance)
    printScreen(screen)


def createEmptyScreen():
    return [[" "] * SCREEN_WIDTH for _ in range(SCREEN_HEIGHT)]


def addSquaresByDistanceInScreen(hero, maze, screen, distance):
    if (distance > 1) and getSquareOfPositionRelativeToHero(hero, maze, 0, 1):
        return
    leftSquareIsAWall = getSquareOfPositionRelativeToHero(hero, maze, -1, distance)
    frontSquareIsAWall = getSquareOfPositionRelativeToHero(hero, maze, 0, distance)
    rightSquareIsAWall = getSquareOfPositionRelativeToHero(hero, maze, 1, distance)
    squareSize = getSquareSizeByDistance(distance)
    previousSquareTotalSize = getPreviousSquareTotalSizeByDistance(distance)

    if leftSquareIsAWall:
        if previousSquareTotalSize != 0:
            for i in range(previousSquareTotalSize, SCREEN_HEIGHT - previousSquareTotalSize):
                screen[i][previousSquareTotalSize - 1] = VERTICAL_WALL_EDGE
        for j in range(1, squareSize):
            for i in range(previousSquareTotalSize + j, SCREEN_HEIGHT - previousSquareTotalSize - j):
                screen[i][previousSquareTotalSize - 1 + j] = VERTICAL_WALL
        for j in range(previousSquareTotalSize, SCREEN_HEIGHT - previousSquareTotalSize - 1):
            for i in range(previousSquareTotalSize - 1):
                screen[j][i] = VERTICAL_WALL
        for i in range(previousSquareTotalSize):
            screen[previousSquareTotalSize - 1][i] = CENTER_ROOF

    if rightSquareIsAWall:
        if previousSquareTotalSize != 0:
            for i in range(previousSquareTotalSize, SCREEN_HEIGHT - previousSquareTotalSize):
                screen[i][SCREEN_WIDTH - previousSquareTotalSize] = VERTICAL_WALL_EDGE
        for j in range(1, squareSize):
            for i in range(previousSquareTotalSize + j, SCREEN_HEIGHT - previousSquareTotalSize - j):
                screen[i][SCREEN_WIDTH - previousSquareTotalSize - j] = VERTICAL_WALL
        for j in range(previousSquareTotalSize, SCREEN_HEIGHT - previousSquareTotalSize - 1):
            for i in range(previousSquareTotalSize - 1):
                screen[j][SCREEN_WIDTH - previousSquareTotalSize + i + 1] = VERTICAL_WALL
        for i in range(previousSquareTotalSize):
            screen[previousSquareTotalSize - 1][SCREEN_WIDTH - i - 1] = CENTER_ROOF

    if frontSquareIsAWall:
        for i in range(previousSquareTotalSize, SCREEN_HEIGHT - previousSquareTotalSize):
            screen[i][previousSquareTotalSize - 1] = VERTICAL_WALL_EDGE
            screen[i][SCREEN_WIDTH - previousSquareTotalSize] = VERTICAL_WALL_EDGE
        for i in range(previousSquareTotalSize, SCREEN_WIDTH - previousSquareTotalSize):
            screen[previousSquareTotalSize - 1][i] = CENTER_ROOF
        for j in range(previousSquareTotalSize, SCREEN_WIDTH - previousSquareTotalSize):
            for i in range(previousSquareTotalSize, SCREEN_HEIGHT - previousSquareTotalSize):
                screen[i][j] = VERTICAL_WALL
    else:
        if leftSquareIsAWall:
            for i in range(previousSquareTotalSize + squareSize,
                           SCREEN_HEIGHT - previousSquareTotalSize - squareSize):
                screen[i][previousSquareTotalSize + squareSize - 1] = VERTICAL_WALL_EDGE
            for i in range(previousSquareTotalSize, previousSquareTotalSize + squareSize):
                screen[i][i] = LEFT_ROOF
        else:
            for i in range(previousSquareTotalSize, previousSquareTotalSize + squareSize):
                screen[SCREEN_HEIGHT - previousSquareTotalSize - squareSize - 1][i] = CENTER_GROUND
        if rightSquareIsAWall:
            for i in range(previousSquareTotalSize + squareSize,
                           SCREEN_HEIGHT - previousSquareTotalSize - squareSize):
                screen[i][SCREEN_WIDTH - previousSquareTotalSize - squareSize] = VERTICAL_WALL_EDGE
            for i in range(previousSquareTotalSize, previousSquareTotalSize + squareSize):
                screen[i][SCREEN_WIDTH - 1 - i] = RIGHT_ROOF
        else:
            for i in range(previousSquareTotalSize, previousSquareTotalSize + squareSize):
                screen[SCREEN_HEIGHT - previousSquareTotalSize - squareSize - 1][
                    SCREEN_WIDTH - i - 1] = CENTER_GROUND
        for i in range(previousSquareTotalSize + squareSize,
                       SCREEN_WIDTH - previousSquareTotalSize - squareSize):
            screen[SCREEN_HEIGHT - previousSquareTotalSize - squareSize - 1][i] = CENTER_GROUND
        for i in range(previousSquareTotalSize, previousSquareTotalSize + squareSize):
            screen[SCREEN_HEIGHT - 1 - i][i] = LEFT_GROUND
            screen[SCREEN_HEIGHT - 1 - i][SCREEN_WIDTH - 1 - i] = RIGHT_GROUND


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


def getPreviousSquareTotalSizeByDistance(distance):
    return sum(SQUARE_SIZES[:distance])


def printScreen(screen):
    for row in range(SCREEN_HEIGHT):
        for column in range(SCREEN_WIDTH):
            print(screen[row][column], end="")
        print()


buildMaze(myMaze)
displayMaze2D(myMaze, myHero)
displayMaze3D(myMaze, myHero)
