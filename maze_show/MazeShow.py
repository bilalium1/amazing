import time
FOREGROUND = 0x2A1F2D
BACKGROUND = 0x003F91
COLOR_42 = 0x5B6C5D
ENTRY_COLOR = 0xFFFFFF
EXIT_COLOR = 0x000000


broll = [0xB2EDC5, 0xB8336A, 0xEDD3C4]
froll = [0x7C7287, 0xACACDE, 0x7765E3]


class MazeShow():
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
            if (self.i & 8):  # EAST
                for y in range(self.o[1], self.o[1] + self.s):
                    self.m.mlx_pixel_put(self.mp, self.wp,
                                         self.o[0] + self.s, y, self.c)
            if (self.i & 4):  # NORTH
                for x in range(self.o[0], self.o[0] + self.s):
                    self.m.mlx_pixel_put(self.mp, self.wp, x,
                                         self.o[1], self.c)
            if (self.i & 2):  # WEST
                for y in range(self.o[1], self.o[1] + self.s):
                    self.m.mlx_pixel_put(self.mp, self.wp,
                                         self.o[0], y, self.c)
            if (self.i & 1):  # SOUTH
                for x in range(self.o[0], self.o[0] + self.s):
                    self.m.mlx_pixel_put(self.mp, self.wp, x,
                                         self.o[1] + self.s, self.c)
            if (self.i & 16): # entry
                for x in range(self.o[0] + 2, self.o[0] + self.s - 1):
                    for y in range(self.o[1] + 2, self.o[1] + self.s - 1):
                        self.m.mlx_pixel_put(self.mp, self.wp, x, y,
                                             ENTRY_COLOR)
            if (self.i & 32): # exit
                for x in range(self.o[0] + 2, self.o[0] + self.s - 1):
                    for y in range(self.o[1] + 2, self.o[1] + self.s - 1):
                        self.m.mlx_pixel_put(self.mp, self.wp, x, y,
                                             EXIT_COLOR)

        def erase(self, margin, fill: bool):
            if fill:
                color = 0x000000
            else:
                color = BACKGROUND
            for i in range(self.o[0] + margin, self.o[0] + self.s - margin):
                for j in range(self.o[1] + margin,
                               self.o[1] + self.s - margin):
                    self.m.mlx_pixel_put(self.mp, self.wp, i, j, color)

        def line(self, color, previous, current, next):
            x_center = self.o[0] + self.s // 2
            y_center = self.o[1] + self.s // 2

            def draw_line(curr, prev):
                dp = abs((curr[0] - prev[0])) - abs((curr[1] - prev[1]))
                if dp == 1:
                    if (curr[0] - prev[0] > 0):
                        for i in range(self.o[0], x_center):
                            self.m.mlx_pixel_put(self.mp, self.wp, i,
                                                 y_center, color)
                            self.m.mlx_pixel_put(self.mp, self.wp, i,
                                                 y_center + 1, color)

                    else:
                        for i in range(self.o[0] + self.s, x_center, -1):
                            self.m.mlx_pixel_put(self.mp, self.wp, i,
                                                 y_center, color)
                            self.m.mlx_pixel_put(self.mp, self.wp, i,
                                                 y_center + 1, color)

                elif dp == -1:
                    if (curr[1] - prev[1] > 0):
                        for i in range(self.o[1], y_center, 1):
                            self.m.mlx_pixel_put(self.mp, self.wp,
                                                 x_center, i, color)
                            self.m.mlx_pixel_put(self.mp, self.wp,
                                                 x_center + 1, i, color)
                    else:
                        for i in range(self.o[1] + self.s, y_center, -1):
                            self.m.mlx_pixel_put(self.mp, self.wp,
                                                 x_center, i, color)
                            self.m.mlx_pixel_put(self.mp, self.wp,
                                                 x_center + 1, i, color)

            draw_line(current, previous)
            draw_line(current, next)

        def animate(self):
            for i in range(self.o[0], self.o[0] + self.s):
                for j in range(self.o[1], self.o[1] + self.s):
                    self.m.mlx_pixel_put(self.mp, self.wp, i, j, self.c)
            time.sleep(0.5)

        def clear(self, color):
            for i in range(self.o[0], self.o[0] + self.s):
                for j in range(self.o[1], self.o[1] + self.s):
                    self.m.mlx_pixel_put(self.mp, self.wp, i, j, color)

        def color_42(self, color):
            for i in range(self.o[0] + 2, self.o[0] + self.s - 1):
                for j in range(self.o[1] + 2, self.o[1] + self.s - 1):
                    self.m.mlx_pixel_put(self.mp, self.wp, i, j, color)

    def display_line(self, info, maze, hv, i, j, st, ed, color, bg_color):

        inc = 1
        if st <= ed:
            inc = 1
        else:
            inc = -1

        if (hv):
            for j in range(st, ed, inc):
                b = self.block(info['mlx'],
                               info['mptr'], info['wptr'],
                               maze[i][j], info['size'],
                               (j * info['size'], i * info['size']),
                               color)
                b.clear(bg_color)
                b.draw()
                if maze[i][j] & 128:
                    b.color_42(COLOR_42)
        else:
            for i in range(st, ed, inc):
                b = self.block(info['mlx'],
                               info['mptr'], info['wptr'],
                               maze[i][j], info['size'],
                               (j * info['size'], i * info['size']),
                               color)
                b.clear(bg_color)
                b.draw()
                if maze[i][j] & 128:
                    b.color_42(COLOR_42)

    def draw_maze(self, maze_info, maze, w, h):

        i = 0
        j = 0

        loops = 0
        limit = min((h) / 2, (w) / 2)

        while (loops < limit):
            self.display_line(maze_info, maze, True, i, j, loops, w - loops,
                              FOREGROUND, BACKGROUND)
            j = w - loops - 1
            self.display_line(maze_info, maze, False, i, j, loops, h - loops,
                              FOREGROUND, BACKGROUND)
            i = h - loops - 1
            self.display_line(maze_info, maze, True, i, j, w-loops-1, loops,
                              FOREGROUND, BACKGROUND)
            j = loops
            self.display_line(maze_info, maze, False, i, j, h-loops-1, loops,
                              FOREGROUND, BACKGROUND)
            loops += 1
            i = loops
            j = loops

    def draw_path(self, path: list[tuple], info, color):

        for i in path:
            coord = (i[0] * info["size"], i[1] * info["size"])

            b = self.block(info["mlx"], info["mptr"], info["wptr"], 0,
                           info["size"], coord, color)
            for j in range(5, 2, -1):
                b.erase(j, True)

    def draw_path2(self, path: list[tuple], info, de: bool):

        if de:
            color = COLOR_42
        else:
            color = BACKGROUND

        for i in range(1, len(path) - 1):
            coord = (path[i][0] * info["size"], path[i][1] * info["size"])

            b = self.block(info["mlx"], info["mptr"], info["wptr"], 0,
                           info["size"], coord, FOREGROUND)
            b.line(color, path[i - 1], path[i], path[i + 1])
