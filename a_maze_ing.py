# 0000
# swne

from maze_gen import MazeGen
from maze_show import MazeShow
from mlx.init import Mlx
import random
import os

ESC = 65307  # X11 ESC KEYCODE
KEY_R = 114

fps = 60


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

    mg = MazeGen.MazeGen()
    ms = MazeShow.MazeShow()
    maze = mg.DFS(width, height, start_pos, end_pos, False, False)

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

    mlx.mlx_string_put(mlx_ptr, win_ptr, int(window_x / 2) - 35, int(window_y / 2) + 5, 0x0055AA, "M.S.I.M.N.A.T")
    mlx.mlx_string_put(mlx_ptr, win_ptr, int(window_x / 2) - 10, int(window_y / 2) + 20, 0x0055AA, "MAZE")

    # maze, size, mlx, mlx_ptr, win_ptr, i, j, st, ed, color

    maze_info = {
        "mlx": mlx,
        "size": size,
        "mptr": mlx_ptr,
        "wptr": win_ptr,
    }

    ms.draw_maze(maze_info, maze, width, height, 0)

    # Draw a string
    mlx.mlx_string_put(mlx_ptr, win_ptr, 300, 20, 0xFF0000, "MAZE")

    def close_window(keycode, param):
        if keycode == ESC:
            mlx.mlx_destroy_window(mlx_ptr, win_ptr)
            os._exit(0)
        if keycode == KEY_R:
            colors = (0x000001, 0x000100, 0x010000)
            ms.draw_maze(maze_info, maze, width,
                         height,
                         colors[random.randint(0, 2)] * random.randint(25, 99))

    mlx.mlx_key_hook(win_ptr, close_window, None)
    mlx.mlx_loop(mlx_ptr)
    file.close()


if __name__ == "__main__":
    main()
