# 0000
# swne

import random

E, N, W, S = 1, 2, 4, 8

DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}

OPP = {E: W, W: E, N: S, S: N}


def generate_maze(w, h):
    maze = [[15 for _ in range(w)] for _ in range(h)]  # all walls closed
    visited = [[False]*w for _ in range(h)]

    def dfs(x, y):
        visited[y][x] = True

        dirs = [E, N, W, S]
        random.shuffle(dirs)

        for d in dirs:
            nx = x + DX[d]
            ny = y + DY[d]

            if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:
                # remove wall
                maze[y][x] ^= d
                maze[ny][nx] ^= OPP[d]

                dfs(nx, ny)

    dfs(0, 0)
    return maze

def backtracker(location: list[int], visted: list[int]):
    pass

def convert(maze: list[list[int]], w: int, h: int) -> list[list[int]]:
    maze_conv = [[0] * (w * 3) for _ in range(h * 3)]

    for i in range(h):
        for j in range(w):

            x = i * 3
            y = j * 3

            for k in range(3):

                if maze[i][j] & 1:
                    maze_conv[x + k][y + 2] = 1

                if maze[i][j] & 2:
                    maze_conv[x][y + k] = 1

                if maze[i][j] & 4:
                    maze_conv[x + k][y] = 1

                if maze[i][j] & 8:                                       
                    maze_conv[x + 2][y + k] = 1
            maze_conv[x + 1][y + 1] = 2

    return maze_conv


def display(maze: list[list[int]], w: int, h: int):

    hex = "0123456789ABCDEF"
    
    i = 0
    while (i < h):
        j = 0
        while (j < w):
            print(hex[maze[i][j]], end="")
            j += 1
        print("")
        i += 1


def gen_maze(maze: list[list[int]], w: int, h: int):
    i = 0
    while (i < h):
        j = 0
        while (j < w):
            maze[i][j] = random.randint(0, 15)
            j += 1
        i += 1


def display_maze(maze: list[list[int]]):
    PATH = "  "
    WALL = "██"

    for row in maze:
        for cell in row:
            if cell == 0:
                print(PATH, end="")
            elif cell == 1:
                print(WALL, end="")
            elif cell == 2:
                print("\033[31m██\033[0m", end="")  # red block
            elif cell == 3:
                print("\033[36m░░\033[0m", end="")  # red block
        print()


def main():

    width = 0
    height = 0

    start_pos = [0, 0]
    end_pos = [0, 0]


    file = open("config.txt", "r")

    content = file.read()
    lines = content.split("\n")
    for line in lines:
        sep = line.split("=")
        if sep[0] == "WIDTH":
            width = int(sep[1])
        elif sep[0] == "HEIGHT":
            height = int(sep[1])

    print(f"width :{width}")
    print(f"height :{height}")

    maze = [[0]*width for _ in range(height)]
    maze = generate_maze(width, height)
    new_maze = convert(maze, width, height)
    display_maze(new_maze)

    file.close()


if __name__ == "__main__":
    main()