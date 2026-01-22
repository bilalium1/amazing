# 1110
# swne

import random

def backtracker(location: list[int], visted: list[int]):
    pass

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

def display_ascii(maze: list[list[int]], w: int, h: int):
    i = 0
            
    while (i < h):
        j = 0
        while (j < w):
            print(ascii_list[maze[i][j]], end="")
            j += 1
        print("")
        i += 1


def gen_maze(maze: list[list[int]], w: int, h: int):
    i = 0
    while (i < h):
        j = 0
        while (j < w):
            maze[i][j] = random.randint(0, 15)
            j += 1
        i += 1
    
    display(maze, w, h)
    display_ascii(maze, w, h)


def main():

    width = 0
    height = 0

    start_pos = [0, 0]
    end_pos = [0, 0]


    file = open("config.txt", "r")

    content = file.read()
    lines = content.split("\n")
    for line in lines:
        sep = line.split("=")
        if sep[0] == "WIDTH":
            width = int(sep[1])
        elif sep[0] == "HEIGHT":
            height = int(sep[1])

    print(f"width :{width}")
    print(f"height :{height}")

    maze = [[0]*width for _ in range(height)]
    gen_maze(maze, width, height)

    file.close()


if __name__ == "__main__":
    main()