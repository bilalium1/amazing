from collections import deque

S, W, N, E = 1, 2, 4, 8

DX = {E: 1,W: -1, N: 0, S: 0}
DY = {E: 0,W: 0, N: -1, S: 1}

def bfs(maze: list[list[int]], h: int, w, int, start: tuple, end: tuple) -> list:
    
    queue = deque([(start[0], start[1], [start])])
    visited = {start}

    while queue:
        x, y, path = queue.popleft()
        if (x, y == end):
            return path
        for direction in [S, W, N, E]:
            if (maze[y][x] & direction) == 0:
                nx = x + DX[direction]
                ny = y + DY[direction]

                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(nx, ny, path + [(nx, ny)])
    return None