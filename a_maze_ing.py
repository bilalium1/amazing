# 0000
# swne

from mlx.init import Mlx
import random
import os
import time
import sys

ESC = 65307  # X11 ESC KEYCODE

fps = 60

sys.setrecursionlimit(10000)

E, N, W, S = 1, 2, 4, 8

DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}


OPP = {E: W, W: E, N: S, S: N}

def generate_maze_it(w, h):
    maze = [[15 for _ in range(w)] for _ in range(h)]  # all walls closed

    def dfs(x, y):
        maze[y][x] = maze[y][x] | 64  # set block as visited

        dirs = [E, N, W, S]
        [N, E , W, S]
        random.shuffle(dirs)

        for d in dirs:
            nx = x + DX[d]
            ny = y + DY[d]

            if 0 <= nx < w and 0 <= ny < h and not (maze[ny][nx] & 64):
                # remove wall
                maze[y][x] ^= d
                maze[ny][nx] ^= OPP[d]

                return (nx, ny)
        return (-1, -1)

    stack = [(0, 0)]
    while stack:
        x, y = stack[-1]
        nx, ny = dfs(x, y)
        if nx == -1:
            stack.pop()
        else:
            stack.append((nx, ny))

    return maze


def add_42(maze: list[list[int]], w: int, h: int, st: tuple, end: tuple):
    # dimensions x: 7 y : 6
    # see if it overlaps with start/end pos
    center = (int(w / 2), int(h / 2))
    zone_42 = (center[0] - 3, center[1] - 3)

    def display_42():
        for y in range(0, 5):
            for x in range(0, 6):
                if (x % 2 == 0 and y & 2 == 0):
                    maze[y][x] &= 128

    if (zone_42[0] <= st[0] <= zone_42[0] + 6):
        if (zone_42[0] + (st[0] - zone_42[0] + 1) + 6 <= w):
            zone_42[0] = st[0] - zone_42[0] + 1
        elif (zone_42[0] - (zone_42[0] + 7 - st[0] - 1) >= 0):
            zone_42[0] = zone_42[0] - 1
    pass


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


# st (10, 2)
# 42 (5, 0)
# 0 <=  <= 6
# 8 - (6 - 1) - 1 = 8

# BLOCK CLASS


class block:
    """
    This class is for each block in the maze to be displayed
    """
    def __init__(self, mmlx, mlx_ptr, win_ptr, info, size, offset, color):
        self.i = info
        self.s = size
        self.o = offset
        self.c = color
        self.mp = mlx_ptr
        self.wp = win_ptr
        self.m = mmlx

    def draw(self):
        if (self.i & 1):  # EAST
            for y in range(self.o[1], self.o[1] + self.s):
                self.m.mlx_pixel_put(self.mp, self.wp, self.o[0] + self.s, y, self.c)
        if (self.i & 2):  # NORTH
            for x in range(self.o[0], self.o[0] + self.s):
                self.m.mlx_pixel_put(self.mp, self.wp, x, self.o[1], self.c)
        if (self.i & 4):  # WEST
            for y in range(self.o[1], self.o[1] + self.s):
                self.m.mlx_pixel_put(self.mp, self.wp, self.o[0], y, self.c)
        if (self.i & 8):  # SOUTH
            for x in range(self.o[0], self.o[0] + self.s):
                self.m.mlx_pixel_put(self.mp, self.wp, x, self.o[1] + self.s, self.c)
        if (self.i & 16):
            for x in range(self.o[0] + 1, self.o[0] + self.s):
                for y in range(self.o[1] + 1, self.o[1] + self.s):
                    self.m.mlx_pixel_put(self.mp, self.wp, x, y, 0x0000FF)
        if (self.i & 32):
            for x in range(self.o[0] + 1, self.o[0] + self.s):
                for y in range(self.o[1] + 1, self.o[1] + self.s):
                    self.m.mlx_pixel_put(self.mp, self.wp, x, y, 0x00FF00)

    def animate(self):
        for i in range(self.o[0], self.o[0] + self.s):
            for j in range(self.o[1], self.o[1] + self.s):
                self.m.mlx_pixel_put(self.mp, self.wp, i, j, self.c)

    def clear(self, color):
        for i in range(self.o[0], self.o[0] + self.s):
            for j in range(self.o[1], self.o[1] + self.s):
                self.m.mlx_pixel_put(self.mp, self.wp, i, j, color)


def display_line(info, maze, hv, i, j, st, ed, color, bg_color):

    inc = 1
    if st <= ed:
        inc = 1
    else:
        inc = -1

    if (hv):
        for j in range(st, ed, inc):
            b = block(info['mlx'], info['mptr'], info['wptr'], maze[i][j], info['size'], (j * info['size'], i * info['size']), color)
            b.clear(bg_color)
            b.draw()
    else:
        for i in range(st, ed, inc):
            b = block(info['mlx'], info['mptr'], info['wptr'], maze[i][j], info['size'], (j * info['size'], i * info['size']), color)
            b.clear(bg_color)
            b.draw()


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
        if sep[0] == "BLOCK_SIZE":
            size = int(sep[1])
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

    while (size * height > 1015):
        size -= 1

    while (size * width > 1900):
        size -= 1

    print(f"width :{width}")
    print(f"height :{height}")

    maze = [[0]*width for _ in range(height)]
    maze = generate_maze_it(width, height)

    maze[start_pos[0]][start_pos[1]] = maze[start_pos[0]][start_pos[1]] | 16
    maze[end_pos[0]][end_pos[1]] = maze[end_pos[0]][end_pos[1]] | 32

    for row in maze:
        print(row)

    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    if not mlx_ptr:
        print("MLX init failed")
        os._exit(1)

    window_x = (width * size) + 1
    window_y = (height * size) + 1

    win_ptr = mlx.mlx_new_window(mlx_ptr, window_x, window_y, "MLX Test")

    i = 0
    j = 0

    loops = 0
    sub_limit = min((height) / 2.5, (width) / 2.5)
    limit = min((height) / 2, (width) / 2)

    mlx.mlx_string_put(mlx_ptr, win_ptr, int(window_x / 2) - 35, int(window_y / 2) + 5, 0x0055AA, "M.S.I.M.N.A.T")
    mlx.mlx_string_put(mlx_ptr, win_ptr, int(window_x / 2) - 10, int(window_y / 2) + 20, 0x0055AA, "MAZE")

    print(sub_limit)

    # maze, size, mlx, mlx_ptr, win_ptr, i, j, st, ed, color

    maze_info = {
        "mlx": mlx,
        "size": size,
        "mptr": mlx_ptr,
        "wptr": win_ptr,
    }

    i = 0
    j = 0

    while (loops < sub_limit):
        display_line(maze_info, maze, True, i, j, loops, width - loops, 0xAAFFFF, 0x222255)
        display_line(maze_info, maze, False, i, j, loops, height - loops, 0x2255AA, 0x050510)
        display_line(maze_info, maze, True, i, j, width-loops-1, loops, 0x222255, 0x050510)
        j -= 1
        display_line(maze_info, maze, False, i, j, height-loops-1, loops, 0xAAAAFF, 0x222255)
        loops += 1
        print(loops)
        i = loops
        j = loops

    while (loops < limit):
        for j in range(loops, width - loops):
            b = block(mlx, mlx_ptr, win_ptr, maze[i][j], size, (j * size, i * size), 0xFFFFFF)
            b.clear(0x000000)
            b.draw()
        for i in range(loops, height - loops):
            b = block(mlx, mlx_ptr, win_ptr, maze[i][j], size, (j * size, i * size), 0xFFFFFF)
            b.clear(0x000000)
            b.draw()
        for j in range(width-loops-1, loops, -1):
            b = block(mlx, mlx_ptr, win_ptr, maze[i][j], size, (j * size, i * size), 0xFFFFFF)
            b.clear(0x000000)
            b.draw()
        j -= 1
        for i in range(height-loops-1, loops, -1):
            b = block(mlx, mlx_ptr, win_ptr, maze[i][j], size, (j * size, i * size), 0xFFFFFF)
            b.clear(0x000000)
            b.draw()
        loops += 1
        i = loops
        j = loops

    # Draw a string
    mlx.mlx_string_put(mlx_ptr, win_ptr, 300, 20, 0xFF0000, "MAZE")


    def close_window(keycode, param):
        if keycode == ESC:
            mlx.mlx_destroy_window(mlx_ptr, win_ptr)
            os._exit(0)

    mlx.mlx_key_hook(win_ptr, close_window, None)
    mlx.mlx_loop(mlx_ptr)
    file.close()


if __name__ == "__main__":
    main()
