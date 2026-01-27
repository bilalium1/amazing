# 2 = wall, 1 = path
#🝪🝪 shok
import random 

"""maze = [
    [1,1,1,1,1,1,1],
    [1,0,1,0,0,0,1],
    [1,0,1,1,1,0,1],
    [1,0,0,0,1,0,1],
    [1,1,1,2,1,0,1],
    [1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1],
]"""

ls = [0, 1, 2, 3]
maze = [[random.choice(ls) for _ in range(100)] for _ in range(100)]

def display():
    PATH = "  "
    WALL = "██"

    for row in maze:
        for cell in row:
            if cell == 0:
                print(PATH, end="")
            elif cell == 1:
                print(WALL, end="")
            elif cell == 2:
                print("\033[31m██\033[0m", end="")  # red block
            elif cell == 3:
                print("\033[36m░░\033[0m", end="")  # red block
        print()

display()
