# 0000
# swne

import mlx
import random
from collections import deque

fps = 60

E, N, W, S = 1, 2, 4, 8

DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}

OPP = {E: W, W: E, N: S, S: N}

def solve_maze(maze, w, h, start, end):
    sx, sy = start
    ex, ey = end
    visited = [[False]*w for _ in range(h)]
    parent = [[None]*w for _ in range(h)]
    
    q = deque()
    q.append((sx, sy))
    visited[sy][sx] = True
    
    while q:
        x, y = q.popleft()
        if (x, y) == (ex, ey):
            break
        cell = maze[y][x]
        
        for d in [S, W, N, E]:
            if cell & d:
                continue
        nx = x + DX[d]
        ny = y + DY[d]
    
    if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:
        visited[ny][nx] = True
        parent[ny][nx] = (x, y)
        q.append((nx, ny))
        
    path = []
    cur = (ex, ey)
    while cur:
        path.append(cur)
        x, y = cur
        cur = parent[y][x]
    
    path.reverse()
    return path

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

def convert(maze, w, h):

    maze_conv = [[0] * (w * 3) for _ in range(h * 3)]

    for i in range(h):
        for j in range(w):

            x = i * 3
            y = j * 3

            cell = maze[i][j]
            full = (cell == 15)

            # Center
            maze_conv[x+1][y+1] = 0

            # East
            if cell & E:
                for k in range(3):
                    maze_conv[x+k][y+2] = 1

            # South
            if cell & S:
                for k in range(3):
                    maze_conv[x+2][y+k] = 1

            # North (only if full or top edge)
            if full or (i == 0 and (cell & N)):
                if cell & N:
                    for k in range(3):
                        maze_conv[x][y+k] = 1

            # West (only if full or left edge)
            if full or (j == 0 and (cell & W)):
                if cell & W:
                    for k in range(3):
                        maze_conv[x+k][y] = 1

            if full:
                for k in range(3):
                    maze_conv[x+k][y] = 4
                for k in range(3):
                    maze_conv[x+k][y+1] = 4
                for k in range(3):
                    maze_conv[x+k][y+2] = 4

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


# ▞
def display_maze(maze: list[list[int]]):
    PATH = "__"
    WALL = "▓▒"

    for row in maze:
        for cell in row:
            if cell == 0:
                print(PATH, end="")
            elif cell == 1:
                print(WALL, end="")
            elif cell == 2:
                print("\033[31m🯅 \033[0m", end="")  # red block
            elif cell == 3:
                print("\033[36m🮿 \033[0m", end="")  # red block
            elif cell == 4:
                print("\033[32m▞▞\033[0m" ,end="")  # invis
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
        elif sep[0] == "ENTRY":
            sep2 = sep[1].split(",")
            start_pos[0] = int(sep2[0])
            start_pos[1] = int(sep2[1])
        elif sep[0] == "EXIT":
            sep2 = sep[1].split(",")
            end_pos[0] = int(sep2[0])
            end_pos[1] = int(sep2[1])

    print(f"width :{width}")
    print(f"height :{height}")

    maze = [[0]*width for _ in range(height)]
    maze = generate_maze(width, height)
    """maze[1][1] = 15
    maze[2][1] = 15
    maze[3][1] = 15
    maze[3][2] = 15
    maze[3][3] = 15
    maze[4][3] = 15
    maze[5][3] = 15
    maze[5][5] = 15
    maze[5][6] = 15
    maze[5][7] = 15
    maze[4][5] = 15
    maze[3][5] = 15
    maze[3][6] = 15
    maze[3][7] = 15
    maze[2][7] = 15
    maze[1][7] = 15
    maze[1][5] = 15
    maze[1][6] = 15"""
    new_maze = convert(maze, width, height)
    new_maze[(start_pos[0] * 3) + 1][(start_pos[1] * 3) + 1] = 2
    new_maze[(end_pos[0] * 3) + 1][(end_pos[1] * 3) + 1] = 3
    display_maze(new_maze)
    path = solve_maze(maze, width, height, start_pos, end_pos)
    print(path)
    file.close()


if __name__ == "__main__":
    main()