# 0000
# swne

from maze_gen import MazeGen
from maze_show import MazeShow
from mlx.init import Mlx
import os
import random
from collections import deque

broll = [0xB2EDC5, 0xB8336A, 0xEDD3C4, 0x62929E, 0x3A0CA3]
froll = [0x7C7287, 0xACACDE, 0x7765E3, 0x5DFDCB, 0x4CC9F0]
roll42 = [0xFF82A9, 0x7F95D1, 0x000000, 0xF7567C, 0xF72585]

ESC = 65307  # X11 ESC KEYCODE
KEY_R = 114
KEY_S = 115
KEY_C = 99
fps = 60

E, N, W, S = 1, 2, 4, 8

DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}

OPP = {E: W, W: E, N: S, S: N}


def parsing() -> dict:
    file = open("config.txt", "r")

    d = {}
    for line in file.read().split("\n"):
        if len(line.split("=")) < 2:
            continue
        key = line.split("=")[0].strip()
        val = line.split("=")[1]
        if (key in ["WIDTH", "HEIGHT", "BLOCK_SIZE"]):
            try:
                val = int(val)
            except ValueError:
                raise ValueError(f"Invalid value for {key}.")
            if val < 0:
                raise ValueError(f"Negative Value for {key}.")
        elif (key in ["ENTRY", "EXIT"]):
            try:
                val = (int(val.split(",")[0]), int(val.split(",")[1]))
            except ValueError:
                raise ValueError(f"Invalid Value for {key}")
            x, y = val
            if x < 0 or y < 0:
                raise ValueError(f"Negative coordinates for {key}.")
        elif (key in ["OUTPUT_FILE"]):
            if not val:
                raise ValueError(f"{key} must have a value.")
        elif (key in ["PERFECT", "42"]):
            if (val.lower() == "false"):
                val = False
            else:
                val = True
        d.update({key: val})
    file.close()

    # CHECK IF ANY MANDATORY CONFIGS ARE MISSING
    man = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}
    if set(d.keys()).intersection(man) != man:
        raise Exception(f"Mandatory argument(s) missing."
                        f"{man - set(d.keys()).intersection(man)}")

    # CHECK FOR BORDERS
    if d["ENTRY"][0] >= d["WIDTH"] or d["ENTRY"][1] >= d["HEIGHT"]:
        raise ValueError("ENTRY Coordinates out of bounds.")
    if d["EXIT"][0] >= d["WIDTH"] or d["EXIT"][1] >= d["HEIGHT"]:
        raise ValueError("EXIT Coordinates out of bounds.")

    return d


def main():

    config = {}
    try:
        config = parsing()
    except Exception as e:
        print("Error :", e)
        return

    while (config["BLOCK_SIZE"] * config["HEIGHT"] > 1015):
        config["BLOCK_SIZE"] -= 1

    while (config["BLOCK_SIZE"] * config["WIDTH"] > 1900):
        config["BLOCK_SIZE"] -= 1
    print(config)
    mg = MazeGen.MazeGen()
    ms = MazeShow.MazeShow()

    if not ("SEED" in config.keys()):
        seed = 0
    else:
        seed = config["SEED"]

    maze = mg.DFS(config["WIDTH"], config["HEIGHT"], config["ENTRY"],
                  config["EXIT"], config["42"], config["PERFECT"], seed)

    mg.output(maze, config["WIDTH"], config["HEIGHT"], config["OUTPUT_FILE"])

    # s = bfs(maze, config["WIDTH"], config["HEIGHT"], config["ENTRY"],
    #               config["EXIT"])

    path = mg.bfs(maze, config["HEIGHT"], config["WIDTH"], config["ENTRY"], config["EXIT"])

    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    if not mlx_ptr:
        print("MLX init failed")
        os._exit(1)

    window_x = (config["WIDTH"] * config["BLOCK_SIZE"])
    window_y = (config["HEIGHT"] * config["BLOCK_SIZE"]) + 30

    win_ptr = mlx.mlx_new_window(mlx_ptr, window_x, window_y, "MLX Test")

    mlx.mlx_string_put(mlx_ptr, win_ptr, 0, window_y - 20, 0xFFFFFF, "C - CHANGE COLOR")
    mlx.mlx_string_put(mlx_ptr, win_ptr, 0, window_y, 0xFFFFFF, "R - REGENRATE MAZE")
    mlx.mlx_string_put(mlx_ptr, win_ptr, 150, window_y -20, 0xFFFFFF, "S - SOLVE")
    mlx.mlx_string_put(mlx_ptr, win_ptr, 150, window_y, 0xFFFFFF, "ESC - QUIT")

    mlx.mlx_string_put(mlx_ptr, win_ptr, int(window_x / 2) - 35,
                       int(window_y / 2) + 5, 0x0055AA, "M.S.I.M.N.A.T")
    mlx.mlx_string_put(mlx_ptr, win_ptr, int(window_x / 2) - 10,
                       int(window_y / 2) + 20, 0x0055AA, "MAZE")

    # maze, size, mlx, mlx_ptr, win_ptr, i, j, st, ed, color

    maze_info = {
        "mlx": mlx,
        "size": config["BLOCK_SIZE"],
        "mptr": mlx_ptr,
        "wptr": win_ptr,
    }

    color_it = 0

    ms.draw_maze(maze_info, maze, config["WIDTH"], config["HEIGHT"])
    print(path)

    def key_reg(keycode, param):
        nonlocal color_it
        nonlocal maze
        nonlocal path

        if keycode == ESC:
            mlx.mlx_destroy_window(mlx_ptr, win_ptr)
            os._exit(0)

        if keycode == KEY_C:
            color_it += 1
            MazeShow.FOREGROUND = froll[color_it % len(froll)]
            MazeShow.BACKGROUND = broll[color_it % len(broll)]
            MazeShow.COLOR_42 = roll42[color_it % len(roll42)]

            ms.draw_maze(maze_info, maze, config["WIDTH"],
                         config["HEIGHT"])
        if keycode == KEY_S:
            print("Starting BFS Solver...")
            ms.draw_path2(path, maze_info, 0xFFFFFF)

        if keycode == KEY_R:
            color_it += 1
            maze = mg.DFS(config["WIDTH"], config["HEIGHT"], config["ENTRY"],
                          config["EXIT"], config["42"], config["PERFECT"],
                          random.seed())
            path = mg.bfs(maze, config["HEIGHT"], config["WIDTH"], config["ENTRY"], config["EXIT"])
            ms.draw_maze(maze_info, maze, config["WIDTH"],
                         config["HEIGHT"])

    mlx.mlx_key_hook(win_ptr, key_reg, None)
    mlx.mlx_loop(mlx_ptr)


if __name__ == "__main__":
    main()
