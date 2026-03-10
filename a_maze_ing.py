# 0000
# swne
from main_menu import draw_menu
from maze_gen import MazeGen
from maze_show import MazeShow
from mlx.init import Mlx
import os
import random
from collections import deque

broll = [0xB2EDC5, 0xB8336A, 0xEDD3C4, 0x62929E, 0x3A0CA3, 0x000000]
froll = [0x7C7287, 0xACACDE, 0x7765E3, 0x5DFDCB, 0x4CC9F0, 0xAAAAAA]
roll42 = [0xFF82A9, 0x7F95D1, 0x000000, 0xF7567C, 0xF72585, 0xFFFFFF]

ESC = 65307
KEY_R = 114
KEY_S = 115
KEY_C = 99
KEY_ENTER = 32
fps = 60

S, W, N, E = 1, 2, 4, 8

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

        if key in ["WIDTH", "HEIGHT", "BLOCK_SIZE"]:
            val = int(val)

        elif key in ["ENTRY", "EXIT"]:
            x, y = val.split(",")
            val = (int(x), int(y))

        elif key in ["PERFECT", "42"]:
            val = False if val.lower() == "false" else True

        d.update({key: val})

    file.close()

    man = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}
    if set(d.keys()).intersection(man) != man:
        raise Exception(f"Mandatory argument(s) missing.")

    return d


def main():

    try:
        config = parsing()
    except Exception as e:
        print("Error :", e)
        return

    while config["BLOCK_SIZE"] * config["HEIGHT"] > 1015:
        config["BLOCK_SIZE"] -= 1

    while config["BLOCK_SIZE"] * config["WIDTH"] > 1900:
        config["BLOCK_SIZE"] -= 1

    mg = MazeGen.MazeGen()
    ms = MazeShow.MazeShow()

    seed = config.get("SEED", random.randint(0, 2**32))

    maze = mg.DFS(
        config["WIDTH"],
        config["HEIGHT"],
        config["ENTRY"],
        config["EXIT"],
        config["42"],
        config["PERFECT"],
        seed
    )

    mg.output(
        maze,
        config["WIDTH"],
        config["HEIGHT"],
        config["ENTRY"],
        config["EXIT"],
        config["OUTPUT_FILE"]
    )

    path = mg.bfs(
        maze,
        config["HEIGHT"],
        config["WIDTH"],
        config["ENTRY"],
        config["EXIT"]
    )

    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()

    if not mlx_ptr:
        print("MLX init failed")
        os._exit(1)

    def maze_window():

        nonlocal maze
        nonlocal path

        window_x = config["WIDTH"] * config["BLOCK_SIZE"]
        window_y = (config["HEIGHT"] * config["BLOCK_SIZE"]) + 30

        win_ptr = mlx.mlx_new_window(mlx_ptr, window_x, window_y, "Maze")

        mlx.mlx_string_put(mlx_ptr, win_ptr, 0, window_y - 20, 0xFFFFFF, "C - COLOR")
        mlx.mlx_string_put(mlx_ptr, win_ptr, 0, window_y, 0xFFFFFF, "R - REGENERATE")
        mlx.mlx_string_put(mlx_ptr, win_ptr, 150, window_y - 20, 0xFFFFFF, "S - SOLVE")
        mlx.mlx_string_put(mlx_ptr, win_ptr, 150, window_y, 0xFFFFFF, "ESC - QUIT")

        maze_info = {
            "mlx": mlx,
            "size": config["BLOCK_SIZE"],
            "mptr": mlx_ptr,
            "wptr": win_ptr,
        }

        color_it = 0
        solved = False

        ms.draw_maze(maze_info, maze, config["WIDTH"], config["HEIGHT"])

        def key_reg(keycode, param):
            nonlocal color_it
            nonlocal maze
            nonlocal path
            nonlocal solved

            if keycode == ESC:
                mlx.mlx_destroy_window(mlx_ptr, win_ptr)
                os._exit(0)

            if keycode == KEY_C:
                color_it += 1

                MazeShow.FOREGROUND = froll[color_it % len(froll)]
                MazeShow.BACKGROUND = broll[color_it % len(broll)]
                MazeShow.COLOR_42 = roll42[color_it % len(roll42)]

                ms.draw_maze(maze_info, maze, config["WIDTH"], config["HEIGHT"])

            if keycode == KEY_S:
                solved = not solved
                ms.draw_path2(path, maze_info, solved)

            if keycode == KEY_R:

                seed = random.randint(0, 2**32)

                maze = mg.DFS(
                    config["WIDTH"],
                    config["HEIGHT"],
                    config["ENTRY"],
                    config["EXIT"],
                    config["42"],
                    config["PERFECT"],
                    seed
                )

                path = mg.bfs(
                    maze,
                    config["HEIGHT"],
                    config["WIDTH"],
                    config["ENTRY"],
                    config["EXIT"]
                )

                ms.draw_maze(maze_info, maze, config["WIDTH"], config["HEIGHT"])

        mlx.mlx_key_hook(win_ptr, key_reg, None)

    menu_win = draw_menu(mlx, mlx_ptr)

    def menu_key_hook(keycode, param):

        if keycode == ESC:
            mlx.mlx_destroy_window(mlx_ptr, menu_win)
            os._exit(0)

        if keycode == KEY_ENTER:
            mlx.mlx_destroy_window(mlx_ptr, menu_win)
            maze_window()

    mlx.mlx_key_hook(menu_win, menu_key_hook, None)
 
    mlx.mlx_loop(mlx_ptr)


if __name__ == "__main__":
    main()