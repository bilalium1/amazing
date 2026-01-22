# 0 = wall, 1 = path
#🝪🝪 shok

maze = [
    [1,1,1,1,1,1,0,1],
    [1,0,0,0,0,1,0,0],
    [1,2,2,0,0,1,0,2],
    [1,0,0,0,0,0,1,2],
    [1,1,1,1,1,1,1,2],
    [0,2,2,1,2,2,2,2],
    [1,2,0,1,2,0,0,0],
    [1,0,0,1,1,1,1,0],
    [0,0,0,0,2,2,2,2],
]



PATH = "  "
WALL = "██"

for row in maze: #so for each row in the cell we get to fill it
    for cell in row:
        if cell == 0:
            print(PATH, end="")
        elif cell == 1:
            print(WALL, end="")
        elif cell == 2:
            print("\033[31m░░\033[0m", end="")  # red block
    print()

