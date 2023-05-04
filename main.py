WIDTH = 21
HEIGHT = 21
maze = [[False] * WIDTH for _ in range(HEIGHT)]
hero = [3, 1, 2]  # [y, x, direction]


def buildMaze(maze):
    for row in range(HEIGHT):
        for column in range(WIDTH):
            if (row == 0) or (row == HEIGHT - 1) or (column == 0) or (column == WIDTH - 1):
                maze[row][column] = True

            if (row % 2 == 0) and (column % 2 == 0):
                maze[row][column] = True


def displayMaze2D(maze, hero):
    for row in range(HEIGHT):
        for column in range(WIDTH):
            if hero[0] == row and hero[1] == column:
                print("00", end="")
            elif maze[row][column]:
                print("XX", end="")
            else:
                print("  ", end="")
        print()


def displayMaze3D(maze, hero):
    leftSquare = False
    rightSquare = False
    if hero[2] == 0:  # on regarde vers le nord
        leftSquare = maze[hero[0]][hero[1] - 1]
        rightSquare = maze[hero[0]][hero[1] + 1]
    elif hero[2] == 1:  # on regarde vers l'est
        leftSquare = maze[hero[0] - 1][hero[1]]
        rightSquare = maze[hero[0] + 1][hero[1]]
    elif hero[2] == 2:  # on regarde vers le sud
        leftSquare = maze[hero[0]][hero[1] + 1]
        rightSquare = maze[hero[0]][hero[1] - 1]
    elif hero[2] == 3:  # on regarde vers l'ouest
        leftSquare = maze[hero[0] + 1][hero[1]]
        rightSquare = maze[hero[0] - 1][hero[1]]

    screen = [[" "] * 21 for _ in range(21)]  # un tableau de 10x10

    # on remplit "en dur"
    screen[20][0] = "/"
    screen[19][1] = "/"
    screen[18][2] = "/"
    screen[17][3] = "/"

    for i in range(4, 17):
        screen[16][i] = "_"

    screen[20][20] = "\\"  # deux mais ça en affichera qu'un
    screen[19][19] = "\\"
    screen[18][18] = "\\"
    screen[17][17] = "\\"

    if leftSquare:  # il y a un mur à gauche
        for i in range(4, 17):
            screen[i][3] = "|"
        screen[0][0] = "\\"
        screen[1][1] = "\\"
        screen[2][2] = "\\"
        screen[3][3] = "\\"
    else:
        for i in range(0,5):
            screen[16][i] = "_"

    if rightSquare:  # il y a un mur à droite
        for i in range(4, 17):
            screen[i][17] = "|"
        screen[0][20] = "/"
        screen[1][19] = "/"
        screen[2][18] = "/"
        screen[3][17] = "/"
    else:
        for i in range(17,21):
            screen[16][i] = "_"

    # on affiche la case devant nous
    leftSquare1 = False
    frontSquare1 = False
    rightSquare1 = False

    if hero[2] == 0:  # on regarde vers le nord
        leftSquare1 = maze[hero[0] - 1][hero[1] - 1]
        frontSquare1 = maze[hero[0] - 1][hero[1]]
        rightSquare1 = maze[hero[0] - 1][hero[1] + 1]
    elif hero[2] == 1:  # on regarde vers l'est
        leftSquare1 = maze[hero[0] - 1][hero[1] + 1]
        frontSquare1 = maze[hero[0]][hero[1] + 1]
        rightSquare1 = maze[hero[0] + 1][hero[1] + 1]
    elif hero[2] == 2:  # on regarde vers le sud
        leftSquare1 = maze[hero[0] + 1][hero[1] + 1]
        frontSquare1 = maze[hero[0] + 1][hero[1]]
        rightSquare1 = maze[hero[0] + 1][hero[1] - 1]
    elif hero[2] == 3:  # on regarde vers l'ouest (kanye ouest)
        leftSquare1 = maze[hero[0] + 1][hero[1] - 1]
        frontSquare1 = maze[hero[0]][hero[1] - 1]
        rightSquare1 = maze[hero[0] - 1][hero[1] - 1]

    if frontSquare1: # si il y a un mur devant nous
        for i in range(4, 17):
            screen[4][i] = "_"
    else:
        screen[16][4] = "/"
        screen[15][5] = "/"
        screen[14][6] = "/"

        for i in range(7, 14):
            screen[13][i] = "_"

        screen[16][16] = "\\"
        screen[15][15] = "\\"
        screen[14][14] = "\\"

    if leftSquare1:  # il y a un mur à gauche
        for i in range(4, 17):
            screen[i][3] = "|"
        for i in range(7, 14):
            screen[i][6] = "|"
        screen[4][4] = "\\"
        screen[5][5] = "\\"
        screen[6][6] = "\\"

    if rightSquare1:  # il y a un mur à droite
        for i in range(4, 17):
            screen[i][17] = "|"
        for i in range(7, 14):
            screen[i][14] = "|"
        screen[4][16] = "/"
        screen[5][15] = "/"
        screen[6][14] = "/"

    printScreen(screen)


def printScreen(screen):
    for row in range(21):
        for column in range(21):
            print(screen[row][column], end="")
        print()


buildMaze(maze)
displayMaze2D(maze, hero)
displayMaze3D(maze, hero)
