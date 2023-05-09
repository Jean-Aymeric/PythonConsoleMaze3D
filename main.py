VERTICAL_WALL = "|"
CENTER_GROUND = "_"
RIGHT_GROUND = "\\"
LEFT_GROUND = "/"
CENTER_ROOF = "_"
LEFT_ROOF = "\\"
RIGHT_ROOF = "/"

FIRST_SQUARES_SIZE = 5
SECOND_SQUARES_SIZE = 6
THIRD_SQUARES_SIZE = 4
FOURTH_SQUARES_HEIGHT = 2
SCREEN_HEIGHT = (FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE + FOURTH_SQUARES_HEIGHT) * 2
SCREEN_WIDTH = int(SCREEN_HEIGHT * 1.3)

MAZE_WIDTH = 21
MAZE_HEIGHT = 21
myMaze = [[False] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]
myHero = [3, 3, 0]  # [y, x, direction]


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
                print("00", end="")
            elif maze[row][column]:
                print("XX", end="")
            else:
                print("  ", end="")
        print()


def displayMaze3D(maze, hero):
    screen = createEmptyScreen()
    addFirstSquaresInScreen(hero, maze, screen)
    addSecondSquaresInScreen(hero, maze, screen)
    addThirdSquaresInScreen(hero, maze, screen)
    addFourthSquaresInScreen(hero, maze, screen)
    printScreen(screen)


def createEmptyScreen():
    return [[" "] * SCREEN_WIDTH for _ in range(SCREEN_HEIGHT)]


def addFirstSquaresInScreen(hero, maze, screen):
    leftSquareIsAWall = False
    rightSquareIsAWall = False
    if hero[2] == 0:  # on regarde vers le nord
        leftSquareIsAWall = maze[hero[0]][hero[1] - 1]
        rightSquareIsAWall = maze[hero[0]][hero[1] + 1]
    elif hero[2] == 1:  # on regarde vers l'est
        leftSquareIsAWall = maze[hero[0] - 1][hero[1]]
        rightSquareIsAWall = maze[hero[0] + 1][hero[1]]
    elif hero[2] == 2:  # on regarde vers le sud
        leftSquareIsAWall = maze[hero[0]][hero[1] + 1]
        rightSquareIsAWall = maze[hero[0]][hero[1] - 1]
    elif hero[2] == 3:  # on regarde vers l'ouest
        leftSquareIsAWall = maze[hero[0] + 1][hero[1]]
        rightSquareIsAWall = maze[hero[0] - 1][hero[1]]

    for i in range(FIRST_SQUARES_SIZE):
        screen[SCREEN_HEIGHT - 1 - i][i] = LEFT_GROUND
        screen[SCREEN_HEIGHT - 1 - i][SCREEN_WIDTH - 1 - i] = RIGHT_GROUND
    for i in range(FIRST_SQUARES_SIZE, SCREEN_WIDTH - FIRST_SQUARES_SIZE):
        screen[SCREEN_HEIGHT - FIRST_SQUARES_SIZE - 1][i] = CENTER_GROUND

    if leftSquareIsAWall:
        for i in range(FIRST_SQUARES_SIZE, SCREEN_HEIGHT - FIRST_SQUARES_SIZE):
            screen[i][FIRST_SQUARES_SIZE - 1] = VERTICAL_WALL
        for i in range(FIRST_SQUARES_SIZE):
            screen[i][i] = LEFT_ROOF
    else:
        for i in range(FIRST_SQUARES_SIZE):
            screen[SCREEN_HEIGHT - 1 - FIRST_SQUARES_SIZE][i] = CENTER_GROUND

    if rightSquareIsAWall:  # il y a un mur à droite
        for i in range(FIRST_SQUARES_SIZE, SCREEN_HEIGHT - FIRST_SQUARES_SIZE):
            screen[i][SCREEN_WIDTH - FIRST_SQUARES_SIZE] = VERTICAL_WALL
        for i in range(FIRST_SQUARES_SIZE):
            screen[i][SCREEN_WIDTH - 1 - i] = RIGHT_ROOF
    else:
        for i in range(SCREEN_WIDTH - FIRST_SQUARES_SIZE, SCREEN_WIDTH):
            screen[SCREEN_HEIGHT - 1 - FIRST_SQUARES_SIZE][i] = CENTER_GROUND


def addSecondSquaresInScreen(hero, maze, screen):
    # on affiche la case devant nous
    leftSquareIsAWall = False
    frontSquareIsAWall = False
    rightSquareIsAWall = False
    if hero[2] == 0:
        leftSquareIsAWall = maze[hero[0] - 1][hero[1] - 1]
        frontSquareIsAWall = maze[hero[0] - 1][hero[1]]
        rightSquareIsAWall = maze[hero[0] - 1][hero[1] + 1]
    elif hero[2] == 1:
        leftSquareIsAWall = maze[hero[0] - 1][hero[1] + 1]
        frontSquareIsAWall = maze[hero[0]][hero[1] + 1]
        rightSquareIsAWall = maze[hero[0] + 1][hero[1] + 1]
    elif hero[2] == 2:
        leftSquareIsAWall = maze[hero[0] + 1][hero[1] + 1]
        frontSquareIsAWall = maze[hero[0] + 1][hero[1]]
        rightSquareIsAWall = maze[hero[0] + 1][hero[1] - 1]
    elif hero[2] == 3:
        leftSquareIsAWall = maze[hero[0] + 1][hero[1] - 1]
        frontSquareIsAWall = maze[hero[0]][hero[1] - 1]
        rightSquareIsAWall = maze[hero[0] - 1][hero[1] - 1]

    if frontSquareIsAWall:
        for i in range(FIRST_SQUARES_SIZE, SCREEN_HEIGHT - FIRST_SQUARES_SIZE):
            screen[i][FIRST_SQUARES_SIZE - 1] = VERTICAL_WALL
            screen[i][SCREEN_WIDTH - FIRST_SQUARES_SIZE] = VERTICAL_WALL
        for i in range(FIRST_SQUARES_SIZE, SCREEN_WIDTH - FIRST_SQUARES_SIZE):
            screen[FIRST_SQUARES_SIZE - 1][i] = CENTER_ROOF
    else:
        for i in range(FIRST_SQUARES_SIZE, FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE):
            screen[SCREEN_HEIGHT - 1 - i][i] = LEFT_GROUND
            screen[SCREEN_HEIGHT - 1 - i][SCREEN_WIDTH - 1 - i] = RIGHT_GROUND
        for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE,
                       SCREEN_WIDTH - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE):
            screen[SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - 1][i] = CENTER_GROUND
        if leftSquareIsAWall:
            for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE,
                           SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE):
                screen[i][FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE - 1] = VERTICAL_WALL
            for i in range(FIRST_SQUARES_SIZE, FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE):
                screen[i][i] = LEFT_ROOF
        else:
            for i in range(FIRST_SQUARES_SIZE, FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE):
                screen[SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - 1][i] = CENTER_GROUND
        if rightSquareIsAWall:
            for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE,
                           SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE):
                screen[i][SCREEN_WIDTH - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE] = VERTICAL_WALL
            for i in range(FIRST_SQUARES_SIZE, FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE):
                screen[i][SCREEN_WIDTH - 1 - i] = RIGHT_ROOF
        else:
            for i in range(FIRST_SQUARES_SIZE, FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE):
                screen[SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - 1][
                    SCREEN_WIDTH - i - 1] = CENTER_GROUND
    if leftSquareIsAWall:
        for i in range(FIRST_SQUARES_SIZE, SCREEN_HEIGHT - FIRST_SQUARES_SIZE):
            screen[i][FIRST_SQUARES_SIZE - 1] = VERTICAL_WALL
        for i in range(FIRST_SQUARES_SIZE):
            screen[FIRST_SQUARES_SIZE - 1][i] = CENTER_ROOF
    if rightSquareIsAWall:
        for i in range(FIRST_SQUARES_SIZE, SCREEN_HEIGHT - FIRST_SQUARES_SIZE):
            screen[i][SCREEN_WIDTH - FIRST_SQUARES_SIZE] = VERTICAL_WALL
        for i in range(FIRST_SQUARES_SIZE):
            screen[FIRST_SQUARES_SIZE - 1][SCREEN_WIDTH - i - 1] = CENTER_ROOF


def addThirdSquaresInScreen(hero, maze, screen):
    leftSquareIsAWall = False
    frontSquareIsAWall = False
    rightSquareIsAWall = False
    if hero[2] == 0:
        leftSquareIsAWall = maze[hero[0] - 2][hero[1] - 1]
        frontSquareIsAWall = maze[hero[0] - 2][hero[1]]
        rightSquareIsAWall = maze[hero[0] - 2][hero[1] + 1]
    elif hero[2] == 1:
        leftSquareIsAWall = maze[hero[0] - 1][hero[1] + 2]
        frontSquareIsAWall = maze[hero[0]][hero[1] + 2]
        rightSquareIsAWall = maze[hero[0] + 1][hero[1] + 2]
    elif hero[2] == 2:
        leftSquareIsAWall = maze[hero[0] + 2][hero[1] + 1]
        frontSquareIsAWall = maze[hero[0] + 2][hero[1]]
        rightSquareIsAWall = maze[hero[0] + 2][hero[1] - 1]
    elif hero[2] == 3:
        leftSquareIsAWall = maze[hero[0] + 1][hero[1] - 2]
        frontSquareIsAWall = maze[hero[0]][hero[1] - 2]
        rightSquareIsAWall = maze[hero[0] - 1][hero[1] - 2]

    if frontSquareIsAWall:
        for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE,
                       SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE):
            screen[i][FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE - 1] = VERTICAL_WALL
            screen[i][SCREEN_WIDTH - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE] = VERTICAL_WALL
        for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE,
                       SCREEN_WIDTH - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE):
            screen[FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE - 1][i] = CENTER_ROOF
    else:
        for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE,
                       FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE):
            screen[SCREEN_HEIGHT - 1 - i][i] = LEFT_GROUND
            screen[SCREEN_HEIGHT - 1 - i][SCREEN_WIDTH - 1 - i] = RIGHT_GROUND
        for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE,
                       SCREEN_WIDTH - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE):
            screen[SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE - 1][i] = CENTER_GROUND
        if leftSquareIsAWall:
            for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE,
                           SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE):
                screen[i][FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE - 1] = VERTICAL_WALL
            for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE,
                           FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE):
                screen[i][i] = LEFT_ROOF
        else:
            for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE,
                           FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE):
                screen[SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE - 1][
                    i] = CENTER_GROUND
        if rightSquareIsAWall:
            for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE,
                           SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE):
                screen[i][SCREEN_WIDTH - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE] = VERTICAL_WALL
            for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE,
                           FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE):
                screen[i][SCREEN_WIDTH - 1 - i] = RIGHT_ROOF
        else:
            for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE,
                           FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE):
                screen[SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE - 1][
                    SCREEN_WIDTH - i - 1] = CENTER_GROUND

    if leftSquareIsAWall:
        for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE,
                       SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE):
            screen[i][FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE - 1] = VERTICAL_WALL
        for i in range(SECOND_SQUARES_SIZE):
            screen[FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE - 1][i + FIRST_SQUARES_SIZE] = CENTER_ROOF
    if rightSquareIsAWall:
        for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE,
                       SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE):
            screen[i][SCREEN_WIDTH - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE] = VERTICAL_WALL
        for i in range(SECOND_SQUARES_SIZE):
            screen[FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE - 1][
                SCREEN_WIDTH - FIRST_SQUARES_SIZE - i - 1] = CENTER_ROOF


def addFourthSquaresInScreen(hero, maze, screen):
    leftSquareIsAWall = False
    frontSquareIsAWall = False
    rightSquareIsAWall = False
    if hero[2] == 0:
        leftSquareIsAWall = maze[hero[0] - 3][hero[1] - 1]
        frontSquareIsAWall = maze[hero[0] - 3][hero[1]]
        rightSquareIsAWall = maze[hero[0] - 3][hero[1] + 1]
    elif hero[2] == 1:
        leftSquareIsAWall = maze[hero[0] - 1][hero[1] + 3]
        frontSquareIsAWall = maze[hero[0]][hero[1] + 3]
        rightSquareIsAWall = maze[hero[0] + 1][hero[1] + 3]
    elif hero[2] == 2:
        leftSquareIsAWall = maze[hero[0] + 3][hero[1] + 1]
        frontSquareIsAWall = maze[hero[0] + 3][hero[1]]
        rightSquareIsAWall = maze[hero[0] + 3][hero[1] - 1]
    elif hero[2] == 3:
        leftSquareIsAWall = maze[hero[0] + 1][hero[1] - 3]
        frontSquareIsAWall = maze[hero[0]][hero[1] - 3]
        rightSquareIsAWall = maze[hero[0] - 1][hero[1] - 3]
    if frontSquareIsAWall:
        for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE,
                       SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE):
            screen[i][FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE - 1] = VERTICAL_WALL
            screen[i][SCREEN_WIDTH - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE] = VERTICAL_WALL
        for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE,
                       SCREEN_WIDTH - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE):
            screen[FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE - 1][i] = CENTER_ROOF
    else:
        for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE,
                       FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE + FOURTH_SQUARES_HEIGHT):
            screen[SCREEN_HEIGHT - 1 - i][i] = LEFT_GROUND
            screen[SCREEN_HEIGHT - 1 - i][SCREEN_WIDTH - 1 - i] = RIGHT_GROUND
        for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE + FOURTH_SQUARES_HEIGHT,
                       SCREEN_WIDTH - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE - FOURTH_SQUARES_HEIGHT):
            screen[
                SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE - FOURTH_SQUARES_HEIGHT - 1][
                i] = CENTER_GROUND
        if leftSquareIsAWall:
            for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE + FOURTH_SQUARES_HEIGHT,
                           SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE - FOURTH_SQUARES_HEIGHT):
                screen[i][
                    FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE + FOURTH_SQUARES_HEIGHT - 1] = VERTICAL_WALL
            for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE,
                           FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE + FOURTH_SQUARES_HEIGHT):
                screen[i][i] = LEFT_ROOF
        else:
            for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE,
                           FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE + FOURTH_SQUARES_HEIGHT):
                screen[
                    SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE - FOURTH_SQUARES_HEIGHT - 1][
                    i] = CENTER_GROUND
        if rightSquareIsAWall:
            for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE + FOURTH_SQUARES_HEIGHT,
                           SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE - FOURTH_SQUARES_HEIGHT):
                screen[i][
                    SCREEN_WIDTH - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE - FOURTH_SQUARES_HEIGHT] = VERTICAL_WALL
            for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE,
                           FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE + FOURTH_SQUARES_HEIGHT):
                screen[i][SCREEN_WIDTH - 1 - i] = RIGHT_ROOF
        else:
            for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE,
                           FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE + FOURTH_SQUARES_HEIGHT):
                screen[
                    SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE - FOURTH_SQUARES_HEIGHT - 1][
                    SCREEN_WIDTH - i - 1] = CENTER_GROUND

    if leftSquareIsAWall:
        for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE,
                       SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE):
            screen[i][FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE - 1] = VERTICAL_WALL
        for i in range(THIRD_SQUARES_SIZE):
            screen[FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE - 1][
                i + FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE] = CENTER_ROOF
    if rightSquareIsAWall:
        for i in range(FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE,
                       SCREEN_HEIGHT - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE):
            screen[i][SCREEN_WIDTH - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - THIRD_SQUARES_SIZE] = VERTICAL_WALL
        for i in range(THIRD_SQUARES_SIZE):
            screen[FIRST_SQUARES_SIZE + SECOND_SQUARES_SIZE + THIRD_SQUARES_SIZE - 1][
                SCREEN_WIDTH - FIRST_SQUARES_SIZE - SECOND_SQUARES_SIZE - i - 1] = CENTER_ROOF


def printScreen(screen):
    for row in range(SCREEN_HEIGHT):
        for column in range(SCREEN_WIDTH):
            print(screen[row][column], end="")
        print()


buildMaze(myMaze)
displayMaze2D(myMaze, myHero)
displayMaze3D(myMaze, myHero)
