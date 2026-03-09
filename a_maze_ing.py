# 0000
# swne

from maze_gen import MazeGen
from maze_show import MazeShow
from mlx.init import Mlx
import random
import os
from collections import deque
import time

ESC = 65307  # X11 ESC KEYCODE
KEY_R = 114
KEY_S = 115
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
        if (key in ["WIDTH", "HEIGHT", "BLOCK_SIZE", "SEED"]):
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
        elif (key in ["PERFECT"]):
            val = bool(val)
        d.update({key: val})
    file.close()

    man = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}
    if set(d.keys()).intersection(man) != man:
        raise Exception(f"Mandatory argument(s) missing. {man - set(d.keys()).intersection(man)}")

    return d

def bfs(maze: list[list[int]], h: int, w: int, start: tuple, end: tuple):
    queue = deque([(start[0], start[1], [start])])
    visited = set()
    visited.add(start)

    while queue:
        x, y, path = queue.popleft()

        if (x, y == end):
            return path
        for direction in [E, N, W, S]:
            if ((maze[x][y] & direction) == 0): 
                nx, ny = x + DX[direction], y + DY[direction]
                #check the boundaries, we'll add the 42 boundaries too
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                    visited.add(nx, ny)
                    new_path = list(path)
                    new_path.append(nx, ny)
                    queue.append(nx, ny, new_path)
    return None


def bfs_animated(maze_info, maze, w, h, start, end, ms):
    queue = deque([(start[0], start[1], [start])])
    visited = {(start[1], start[0])} # Use a set with the start tuple

    while queue:
        x, y, path = queue.popleft()

        if (x, y) == end:
            for px, py in path:
                # Use ms.block to draw the final solution
                b = ms.block(maze_info['mlx'], maze_info['mptr'], maze_info['wptr'], 
                          maze[py][px], maze_info['size'], (px * maze_info['size'], py * maze_info['size']), 0x00FF00)
                b.draw()
            return path

        for direction in [E, N, W, S]:
            # Check if there's NO wall in this direction
            if not (maze[y][x] & direction): 
                nx, ny = x + DX[direction], y + DY[direction]
                
                # Boundary check and Visited check
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                    visited.add((ny, nx))
                    
                    # Optional: Draw the frontier in BLUE
                    exploration_block = ms.block(maze_info['mlx'], maze_info['mptr'], maze_info['wptr'], 
                                              maze[ny][nx], maze_info['size'], 
                                              (nx * maze_info['size'], ny * maze_info['size']), 0x0000FF)
                    exploration_block.draw()
                    
                    # Crucial: This allows the MLX window to update during the loop
                    # time.sleep(0.01) 
                    
                    queue.append((ny, nx, path + [(ny, nx)]))
    return None


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

    maze = mg.DFS(config["WIDTH"], config["HEIGHT"], config["ENTRY"],
                  config["EXIT"], True, False, config["SEED"])

    mg.output(maze, config["WIDTH"], config["HEIGHT"], config["OUTPUT_FILE"])

    maze[config["ENTRY"][0]][config["ENTRY"][1]] |= 16
    maze[config["EXIT"][0]][config["EXIT"][1]] |= 32
    
    # s = bfs(maze, config["WIDTH"], config["HEIGHT"], config["ENTRY"],
    #               config["EXIT"])

    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    if not mlx_ptr:
        print("MLX init failed")
        os._exit(1)

    window_x = (config["WIDTH"] * config["BLOCK_SIZE"]) + 1
    window_y = (config["HEIGHT"] * config["BLOCK_SIZE"]) + 1

    win_ptr = mlx.mlx_new_window(mlx_ptr, window_x, window_y, "MLX Test")

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

    ms.draw_maze(maze_info, maze, config["WIDTH"], config["HEIGHT"], 0)

    def close_window(keycode, param):
        if keycode == ESC:
            mlx.mlx_destroy_window(mlx_ptr, win_ptr)
            os._exit(0)
        if keycode == KEY_R:
            colors = (0x000001, 0x000100, 0x010000)
            ms.draw_maze(maze_info, maze, config["WIDTH"],
                         config["HEIGHT"],
                         colors[random.randint(0, 2)] * random.randint(25, 99))
        if keycode == KEY_S:
            print("Starting BFS Solver...")
            bfs_animated(maze_info, maze, config["WIDTH"], config["HEIGHT"], config["ENTRY"],
                  config["EXIT"], ms)

    mlx.mlx_key_hook(win_ptr, close_window, None)
    mlx.mlx_loop(mlx_ptr)


if __name__ == "__main__":
    main()
