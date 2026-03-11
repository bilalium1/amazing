# 0000
# swne
from main_menu import draw_menu
from maze_gen import MazeGen
from maze_show import MazeShow
from mlx.init import Mlx
import os
import random
from collections import deque

broll = [0xB2EDC5, 0xB8336A, 0xEDD3C4, 0x62929E, 0x3A0C53, 0x000000, 0xAA1122]
froll = [0x7C7287, 0xACACDE, 0x7765E3, 0x5DFDCB, 0x4CC9F0, 0xAAAAAA, 0x22AA11]
roll42 = [0xFF82A9, 0x7F95D1, 0x550055, 0xF7567C, 0xD7A585, 0xFFFFFF, 0x2211AA]

ESC = 65307
KEY_R = 114
KEY_S = 115
KEY_C = 99
KEY_ENTER = 32

KEY_LEFT  = 65361
KEY_UP    = 65362
KEY_RIGHT = 65363
KEY_DOWN  = 65364

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
    
    if d["ENTRY"][0] == d["EXIT"][0] and d["ENTRY"][1] == d["EXIT"][1]:
        raise ValueError("ENTRY and EXIT Coordinates Overlap.")

    # CHECK FOR BORDERS
    if d["ENTRY"][0] >= d["WIDTH"] or d["ENTRY"][1] >= d["HEIGHT"]:
        raise ValueError("ENTRY Coordinates out of bounds.")
    if d["EXIT"][0] >= d["WIDTH"] or d["EXIT"][1] >= d["HEIGHT"]:
        raise ValueError("EXIT Coordinates out of bounds.")
    
    extras = {"BLOCK_SIZE": 25, "42": True, "SEED": 0}
    
    # SET DEFAULT
    for k, v in extras.items():
        d.setdefault(k, v)

    return d


def main():

    try:
        config = parsing()
    except Exception as e:
        print("Error :", e)
        return
    
    print(config)

    while config["BLOCK_SIZE"] * config["HEIGHT"] > 900:
        config["BLOCK_SIZE"] -= 1

    while config["BLOCK_SIZE"] * config["WIDTH"] > 1700:
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

        exit_pos = config["EXIT"]
        color_it = 0
        solved = False

        ms.draw_maze(maze_info, maze, config["WIDTH"], config["HEIGHT"])

        def key_reg(keycode, param):
            nonlocal color_it
            nonlocal maze
            nonlocal path
            nonlocal solved
            nonlocal exit_pos

            if keycode == ESC:
                mlx.mlx_destroy_window(mlx_ptr, win_ptr)
                os._exit(0)

            if keycode == KEY_C:
                solved = False
                color_it += 1

                MazeShow.FOREGROUND = froll[color_it % len(froll)]
                MazeShow.BACKGROUND = broll[color_it % len(broll)]
                MazeShow.COLOR_42 = roll42[color_it % len(roll42)]

                ms.draw_maze(maze_info, maze, config["WIDTH"], config["HEIGHT"])

            if keycode == KEY_S:
                solved = not solved
                ms.draw_path2(path, maze_info, solved)

            if keycode == KEY_R:
                solved = False
                new_seed = random.randint(0, 2**32)

                maze = mg.DFS(
                    config["WIDTH"],
                    config["HEIGHT"],
                    config["ENTRY"],
                    exit_pos,
                    config["42"],
                    config["PERFECT"],
                    new_seed
                )

                path = mg.bfs(
                    maze,
                    config["HEIGHT"],
                    config["WIDTH"],
                    config["ENTRY"],
                    exit_pos
                )

                ms.draw_maze(maze_info, maze, config["WIDTH"], config["HEIGHT"])

            def move_exit(dx: int, dy: int):

                nonlocal path
                nonlocal solved
                nonlocal maze
                nonlocal exit_pos

                if exit_pos[0] + dx == config["ENTRY"][0] and exit_pos[1] + dy == config["ENTRY"][1]:
                    return

                b = ms.block(mlx, mlx_ptr, win_ptr,
                             maze[exit_pos[1]][exit_pos[0]] & 15,
                             config["BLOCK_SIZE"],
                             (exit_pos[0] * config["BLOCK_SIZE"], exit_pos[1] * config["BLOCK_SIZE"]), 0x000000)
                b.erase(1, False)
                maze[exit_pos[1]][exit_pos[0]] -= 32
                exit_pos = (exit_pos[0] + dx, exit_pos[1] + dy)
                maze[exit_pos[1]][exit_pos[0]] += 32
                b2 = ms.block(mlx, mlx_ptr, win_ptr,
                             maze[exit_pos[1]][exit_pos[0]] & 15,
                             config["BLOCK_SIZE"],
                             (exit_pos[0] * config["BLOCK_SIZE"],exit_pos[1] * config["BLOCK_SIZE"]), 0x000000)
                b2.erase(1, True)
                if solved:
                    ms.draw_path2(path, maze_info, False)
                path = mg.bfs(
                    maze,
                    config["HEIGHT"],
                    config["WIDTH"],
                    config["ENTRY"],
                    exit_pos
                )
                if solved:
                    ms.draw_path2(path, maze_info, True)

            if keycode == KEY_RIGHT and exit_pos[0] + 1 < config["WIDTH"] and not (maze[exit_pos[1]][ exit_pos[0] + 1] & 128):
                move_exit(1, 0)
            if keycode == KEY_LEFT and exit_pos[0] - 1 >= 0 and not (maze[exit_pos[1]][ exit_pos[0] - 1] & 128):
                move_exit(-1, 0)
            if keycode == KEY_UP and exit_pos[1] - 1 >= 0 and not (maze[exit_pos[1] - 1][ exit_pos[0]] & 128):
                move_exit(0, -1)
            if keycode == KEY_DOWN and exit_pos[1] + 1 < config["HEIGHT"] and not (maze[exit_pos[1] + 1][ exit_pos[0]] & 128):
                move_exit(0, 1)

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