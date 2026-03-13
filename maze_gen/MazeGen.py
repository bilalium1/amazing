import random
from collections import deque
from typing import Any

S, W, N, E = 1, 2, 4, 8

DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}

OPP = {E: W, W: E, N: S, S: N}


class MazeGen():
    def __init__(self) -> None:
        pass

    def add_42(self, maze: list[list[int]], w: int, h: int,
               st: tuple, end: tuple) -> None:
        center = (w // 2, h // 2)
        start_42 = [center[0] - 4, center[1] - 2]

        blocks = [(0, 0), (0, 1), (0, 2),
                  (1, 2),
                  (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
                  (4, 0), (4, 2), (4, 3), (4, 4),
                  (5, 0), (5, 2), (5, 4),
                  (6, 0), (6, 1), (6, 2), (6, 4),
                  ]

        def check_over(pos: tuple) -> bool:
            for b in blocks:
                if (pos[0] == start_42[0] + b[0]
                        or pos[1] == start_42[1] + b[1]):
                    return True
            return False

        loop_count = 0

        while (check_over(st) or check_over(end)):
            t = random.randint(-2, 2)
            if start_42[0] + t > 0 and start_42[0] + 7 + t < w:
                start_42[0] += t
            if start_42[1] + t > 0 and start_42[1] + 6 + t < h:
                start_42[1] += t
            loop_count += 1
            if loop_count > 50:
                return

        def display_42() -> None:
            # 4
            for b in blocks:
                maze[start_42[1] + b[1]][start_42[0] + b[0]] |= 15 | 64 | 128

        display_42()

    def DFS(self, w: int, h: int, sp: tuple, ep: tuple,
            w42: bool, pfct: bool, seed: int) -> list[list[int]]:
        """
        This is a function that generates 2d array of integers
        ranging from 0 to 15, each bit in every integers refers
        to the walls of each block in the maze

        :param w: width of the maze
        :param h: height of the maze
        """
        maze = [[15 for _ in range(w)] for _ in range(h)]  # closed maze

        random.seed(seed)

        if w42:
            self.add_42(maze, w, h, sp, ep)

        def dfs(x: int, y: int) -> tuple:
            maze[y][x] = maze[y][x] | 64  # set block as visited

            dirs = [S, W, N, E]
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

                if (maze[y][x] & 128):
                    continue

                dirs = [S, W, N, E]
                random.shuffle(dirs)
                for d in dirs:
                    nx, ny = x + DX[d], y + DY[d]
                    if 0 <= nx < w and 0 <= ny < h:
                        if maze[y][x] & d and maze[ny][nx] & OPP[d]:
                            maze[y][x] ^= d
                            maze[ny][nx] ^= OPP[d]
                        break

        maze[sp[1]][sp[0]] |= 16
        maze[ep[1]][ep[0]] |= 32

        return maze

    def bfs(self, maze: list[list[int]], h: int, w: int, start: tuple,
            end: tuple) -> Any:
        queue = deque([(start[0], start[1], [start])])
        visited = {start}

        while queue:
            print(queue)
            x, y, path = queue.popleft()
            if (x, y) == end:
                return path

            for direction in [S, W, N, E]:
                # move if path is open
                if (maze[y][x] & direction) == 0:
                    nx = x + DX[direction]
                    ny = y + DY[direction]

                    if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny, path + [(nx, ny)]))

        return None

    def output(self, maze: list[list[int]], w: int, h: int, st: tuple,
               end: tuple, out_file: str, path: list[tuple]) -> None:
        file = open(out_file, "w")

        hex = "0123456789ABCDEF"
        i = 0
        while (i < h):
            j = 0
            while (j < w):
                file.write(hex[maze[i][j] & 15])
                j += 1
            file.write("\n")
            i += 1
        file.write("\n")
        file.write(f"{st[0]}, {st[1]}")
        file.write("\n")
        file.write(f"{end[0]}, {end[1]}")
        file.write("\n")

        if path == None:
            return

        for i in range(1, len(path)):
            prev = path[i - 1]
            curr = path[i]
            dp = abs((curr[0] - prev[0])) - abs((curr[1] - prev[1]))
            if (dp > 0):
                if (curr[0] - prev[0] > 0):
                    file.write("E")
                else:
                    file.write("W")
            else:
                if (curr[1] - prev[1] > 0):
                    file.write("S")
                else:
                    file.write("N")
