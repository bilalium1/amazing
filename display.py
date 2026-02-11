from mlx import Mlx
import os
import time
import random

ESC = 65307  # X11 ESC KEYCODE

matrix = [[random.randint(0, 15) for _ in range(10)] for _ in range(10)]


class block:
    def __init__(self, info, size, offset, color):
        self.i = info
        self.s = size
        self.o = offset
        self.c = color
    
    def draw(self):
        if (self.i & 1):  # EAST
            for y in range(self.o[1], self.o[1] + self.s):
                mlx.mlx_pixel_put(mlx_ptr, win_ptr, self.o[0] + self.s, y, self.c)
        if (self.i & 2):  # NORTH
            for x in range(self.o[0], self.o[0] + self.s):
                mlx.mlx_pixel_put(mlx_ptr, win_ptr, x, self.o[1], self.c)
        if (self.i & 4):  # WEST
            for y in range(self.o[1], self.o[1] + self.s):
                mlx.mlx_pixel_put(mlx_ptr, win_ptr, self.o[0], y, self.c)
        if (self.i & 8):  # SOUTH
            for x in range(self.o[0], self.o[0] + self.s):
                mlx.mlx_pixel_put(mlx_ptr, win_ptr, x, self.o[1] + self.s, self.c)

    def animate(self):
        for i in range(self.o[0], self.o[0] + self.s):
            for j in range(self.o[1], self.o[1] + self.s):
                mlx.mlx_pixel_put(mlx_ptr, win_ptr, i, j, self.c)
            time.sleep((0.05) / self.s)

    def clear(self):
        for i in range(self.o[0], self.o[0] + self.s):
            for j in range(self.o[1], self.o[1] + self.s):
                mlx.mlx_pixel_put(mlx_ptr, win_ptr, i, j, j + i)

for row in matrix:
    print(row)

mlx = Mlx()
mlx_ptr = mlx.mlx_init()
if not mlx_ptr:
    print("MLX init failed")
    os._exit(1)

win_ptr = mlx.mlx_new_window(mlx_ptr, 1920, 1080, "MLX Test")

for i in range(0, 9):
    for j in range(0, 9):
        b = block(matrix[i][j], 25, (j * 25, i * 25), 0xFFFFFF)
        b.animate()
        b.clear()
        b.draw()

# Draw a string
mlx.mlx_string_put(mlx_ptr, win_ptr, 300, 20, 0xFF0000, "MAZE ")

def close_window(keycode, param):
    if keycode == ESC:
        mlx.mlx_destroy_window(mlx_ptr, win_ptr)
        os._exit(0)


mlx.mlx_key_hook(win_ptr, close_window, None)
mlx.mlx_loop(mlx_ptr)

int(input("hello"))

# swne
# 0000