> This project was created as part of the **42 School curriculum** by  
> **[adkaid-s]** and **[blemrabe]**

<h1 align="center">A_MAZE_ING</h1>

<p align="center">
<i>Let's get lost in the maze</i>
</p>

<p align="center">
  <img src="https://github.com/bilalium1/amazing/blob/main/reamde_assets/maze_mp4-ezgif.com-video-to-gif-converter.gif" width="800" height="100%">
</p>

---

# 📚 About The Project

**A_MAZE_ING** is a maze generation and visualization project combining **algorithmic complexity** with **interactive graphics**.

The project features:

- 🧠 A **Python-based maze generator**
- 🧩 Generation of **perfect mazes** (single valid path between any two points)
- 🎮 An **interactive graphical interface** built with **MiniLibX**
- 🚀 Real-time maze regeneration and path visualization

The generator produces structured maze data which is then rendered visually using **MLX**, allowing dynamic interaction with the maze.

---

# ❓ Developer FAQ

## How do I install and run the project?

The project uses a **Makefile** to simplify setup and execution.

### Install dependencies

```bash
make install
This launches the maze generator using the default `config.txt`.
```
---

## 🧹 Clean temporary files

```bash
make clean
```

Removes Python cache files such as:

```
__pycache__
.mypy_cache
```

---

# ⚙️ Configuration

Maze parameters are defined inside `config.txt` using:

```
KEY=VALUE
```

Lines starting with `#` are treated as comments.

---

## Required Configuration Keys

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Number of horizontal cells | `WIDTH=20` |
| `HEIGHT` | Number of vertical cells | `HEIGHT=15` |
| `ENTRY` | Starting coordinates `(x,y)` | `ENTRY=0,0` |
| `EXIT` | Ending coordinates `(x,y)` | `EXIT=19,14` |
| `OUTPUT_FILE` | Destination file for hex maze data | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Generate a perfect maze (single path) | `PERFECT=True` |

### Optional Configuration Keys

| Key | Description | Example |
|-----|-------------|---------|
| `BLOCK_SIZE` | Size of each block in the maze | `BLOCK_SIZE=25` |
| `SEED` | Maze Seed | `SEED=42` |
| `42` | display 42 on the maze | `42=True` |

---

# 🧠 Algorithms

## Maze Generation

**Algorithm Used:**  
Depth-First Search (DFS)

### Why DFS?

DFS naturally produces:

- long winding corridors
- fewer intersections
- a more **labyrinth-like structure**

It also simplifies the creation of **perfect mazes** by ensuring that the maze forms a **spanning tree with no loops**.

---

## Maze Solving

**Algorithm Used:**  
Breadth-First Search (BFS)

### Why BFS?

BFS guarantees the **shortest possible path** between the maze entry and exit.

This ensures that the **"Show Path"** feature always displays the **optimal solution**.

---

# 🎮 Visual Interaction (MiniLibX)

The maze is rendered using **MiniLibX (MLX)**, allowing real-time interaction.

---

## Controls

| Key | Action |
|-----|--------|
| **R** | Generate a new maze |
| **S** | Toggle shortest path display |
| **C** | Cycle color schemes |
| **Arrow Keys** | Move the exit position dynamically |
| **ESC** | Exit the program |

---

# ♻️ Code Reusability

The maze generation logic is encapsulated inside a standalone class:

``MazeGen``

## Features

- Generates perfect mazes
- Exposes the maze structure
- Includes BFS solving functionality

---

## Example Usage

```python
from maze_gen import MazeGen
from mazeshow import MazeShow

maze_gen = MazeGen.MazeGen()
maze_map = maze_gen.DFS(...) -> list[list[int]:

maze_show = MazeShow.MazeShow()
maze_show.draw_maze(maze_map, ...)
```

The internal maze representation is stored as a **2D list of integers**, describing **walls and passages**.

---

# 📖 Resources

## References

- **Recursive Backtracker Maze Generation** — DFS implementation reference  
- **MiniLibX Documentation** — graphical rendering  
- **PEP 257 / Flake8 standards** — code quality and formatting  

---

# 🤖 AI Disclosure

AI tools were used during development for:

### Boilerplate Generation

Creating the initial structure for:

- configuration parser
- MLX wrapper classes

### Debugging

Helping identify logic errors in:

- the **"42" pattern placement**

### Refactoring

Improving the efficiency of:

- BFS path reconstruction

---

All generated code was:

- reviewed
- modified to meet **42 standards**
- fully understood before submission

---

# 👨‍💻 Project Management

## Team

### Developer 1 : **[adkaid-s]**

- Maze generation logic
- DFS/BFS algorithms
- Interactive key controls

### Developer 2 **[blemrabe]**

- MazeShow UI
- MLX integration
- Hex output formatting

---

## Project Evolution

The project initially started as a **terminal ASCII renderer**.

To improve:

- user experience
- visual clarity
- animation possibilities

the project transitioned early into a **full MiniLibX graphical implementation**.

---

# 🛠 Tools

- Python **3.10+**
- **MiniLibX**
- **flake8**            
- **mypy**
- **Git** 
---

<p align="center">
  <img src="https://www.nicepng.com/png/full/149-1491524_png-sonic-advance-knuckles-gif.png" width="280">
</p>
<p align="center"><em>MADE BY M.S.I.M.N.A.T</em></p>
