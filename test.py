from mlx import Mlx
import sys
import random

matrix = [[random.randint(0, 15) for _ in range(5)] for _ in range(5)]

for row in matrix:
    print(row)

mlx = Mlx()
mlx_ptr = mlx.mlx_init()
if not mlx_ptr:
    print("MLX init failed")
    sys.exit(1)

win_ptr = mlx.mlx_new_window(mlx_ptr, 1920, 1080, "MLX Test")

# Draw some pixels
for x in range(0, 200):
    for y in range(50, 150):
        mlx.mlx_pixel_put(mlx_ptr, win_ptr, x, y, 0x0000FF)  # green square

# Draw a string
mlx.mlx_string_put(mlx_ptr, win_ptr, 150, 20, 0xFF0000, "Hello MLX")
def close_window(keycode, param):
    if keycode == 65307:  # ESC key on Debian/Linux
        mlx.mlx_destroy_window(mlx_ptr, win_ptr)
        sys.exit(0)

mlx.mlx_hook(win_ptr, 2, 1 << 0, close_window, None)
mlx.mlx_loop(mlx_ptr)

# Start loop onc

class block:
    def __init__(self, info, size, offset, color):
        self.info = info
        self.size = size
        self.offset = offset
        self.color = color
    
    def draw(self):
        for x in range(self.offset[0], self.offset[0] + self.size):
            for y in range(self.offset[1], self.offset[1] + self.size):
                mlx.mlx_pixel_put(mlx_ptr, win_ptr, x, y, 255)

