import random

E, N, W, S = 1, 2, 4, 8

DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}

OPP = {E: W, W: E, N: S, S: N}


class MazeGen():
    def __init__(self):
        pass

    def add_42(self, maze: list[list[int]], w: int, h: int,
               st: tuple, end: tuple):
        center = (w // 2, h // 2)
        zone_42 = [center[0] - 4, center[1] - 2]

        def overlaps(pos):
            return (zone_42[0] <= pos[0] <= zone_42[0] + 6 and
                    zone_42[1] <= pos[1] <= zone_42[1] + 6)

        for pos in (st, end):
            if overlaps(pos):
                zone_42[0] = min(w - 7, pos[0] + 1)
                zone_42[1] = min(h - 7, pos[1] + 1)

        zone_42[0] = max(0, min(zone_42[0], w - 7))
        zone_42[1] = max(0, min(zone_42[1], h - 7))

        def display_42():
            # 4
            for i in range(0, 3):
                maze[zone_42[1] + i][zone_42[0]] |= 207
            maze[zone_42[1] + 2][zone_42[0] + 1] |= 207
            for i in range(0, 5):
                maze[zone_42[1] + i][zone_42[0] + 2] |= 207
            # 2
            for i in range(4, 7):
                maze[zone_42[1]][zone_42[0] + i] |= 207
            maze[zone_42[1] + 1][zone_42[0] + 6] |= 207
            for i in range(4, 7):
                maze[zone_42[1] + 2][zone_42[0] + i] |= 207
            maze[zone_42[1] + 3][zone_42[0] + 4] |= 207
            for i in range(4, 7):
                maze[zone_42[1] + 4][zone_42[0] + i] |= 207

        display_42()

    def DFS(self, w: int, h: int, sp, ep, w42: bool, pfct: bool):
        """
        This is a function that generates 2d array of integers
        ranging from 0 to 15, each bit in every integers refers
        to the walls of each block in the maze

        :param w: width of the maze
        :param h: height of the maze
        """
        maze = [[15 for _ in range(w)] for _ in range(h)]  # closed maze
        if w42:
            self.add_42(maze, w, h, sp, ep)

        def dfs(x, y):
            maze[y][x] = maze[y][x] | 64  # set block as visited

            dirs = [E, N, W, S]
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

        if not pfct:
            for _ in range((w * h) // 5):
                x, y = random.randint(0, w-1), random.randint(0, h-1)
                dirs = [E, N, W, S]
                random.shuffle(dirs)
                for d in dirs:
                    nx, ny = x + DX[d], y + DY[d]
                    if 0 <= nx < w and 0 <= ny < h:
                        if maze[y][x] & d and maze[ny][nx] & OPP[d]:
                            maze[y][x] ^= d
                            maze[ny][nx] ^= OPP[d]
                        break

        return maze

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
