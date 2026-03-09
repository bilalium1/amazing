FOREGROUND = 0xE8E9ED
BACKGROUND = 0x607196
COLOR_42 = 0xFF7B9C
EXIT_COLOR = 0xFF7B9C
ENTRY_COLOR = 0xFFC759


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
            if (self.i & 1):  # EAST
                for y in range(self.o[1], self.o[1] + self.s):
                    self.m.mlx_pixel_put(self.mp, self.wp,
                                         self.o[0] + self.s, y, self.c)
            if (self.i & 2):  # NORTH
                for x in range(self.o[0], self.o[0] + self.s):
                    self.m.mlx_pixel_put(self.mp, self.wp, x,
                                         self.o[1], self.c)
            if (self.i & 4):  # WEST
                for y in range(self.o[1], self.o[1] + self.s):
                    self.m.mlx_pixel_put(self.mp, self.wp,
                                         self.o[0], y, self.c)
            if (self.i & 8):  # SOUTH
                for x in range(self.o[0], self.o[0] + self.s):
                    self.m.mlx_pixel_put(self.mp, self.wp, x,
                                         self.o[1] + self.s, self.c)
            if (self.i & 16):
                for x in range(self.o[0] + 1, self.o[0] + self.s):
                    for y in range(self.o[1] + 1, self.o[1] + self.s):
                        self.m.mlx_pixel_put(self.mp, self.wp, x, y, 0xFFC759)
            if (self.i & 32):
                for x in range(self.o[0] + 1, self.o[0] + self.s):
                    for y in range(self.o[1] + 1, self.o[1] + self.s):
                        self.m.mlx_pixel_put(self.mp, self.wp, x, y, 0xFF7B9C)

        def animate(self):
            for i in range(self.o[0], self.o[0] + self.s):
                for j in range(self.o[1], self.o[1] + self.s):
                    self.m.mlx_pixel_put(self.mp, self.wp, i, j, self.c)

        def clear(self, color):
            for i in range(self.o[0], self.o[0] + self.s):
                for j in range(self.o[1], self.o[1] + self.s):
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
                    b.clear(COLOR_42)
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
                    b.clear(ENTRY_COLOR)

    def draw_maze(self, maze_info, maze, w, h, color_offset):

        i = 0
        j = 0

        loops = 0
        sub_limit = min((h) / 3, (w) / 3)
        limit = min((h) / 2, (w) / 2)

        while (loops < sub_limit):
            self.display_line(maze_info, maze, True, i, j, loops, w - loops,
                              FOREGROUND + color_offset, BACKGROUND)
            j = w - loops - 1
            self.display_line(maze_info, maze, False, i, j, loops, h - loops,
                              FOREGROUND + color_offset, BACKGROUND)
            i = h - loops - 1
            self.display_line(maze_info, maze, True, i, j, w-loops-1, loops,
                              FOREGROUND + color_offset, BACKGROUND)
            j = loops
            self.display_line(maze_info, maze, False, i, j, h-loops-1, loops,
                              FOREGROUND + color_offset, BACKGROUND)
            loops += 1
            i = loops
            j = loops

        while (loops < limit):
            self.display_line(maze_info, maze, True, i, j, loops, w - loops,
                              BACKGROUND, 0x000000)
            j = w - loops - 1
            self.display_line(maze_info, maze, False, i, j, loops, h - loops,
                              BACKGROUND, 0x000000)
            i = h - loops - 1
            self.display_line(maze_info, maze, True, i, j, w-loops-1, loops,
                              BACKGROUND, 0x000000)
            j = loops
            self.display_line(maze_info, maze, False, i, j, h-loops-1, loops,
                              BACKGROUND, 0x000000)
            loops += 1
            i = loops
            j = loops
