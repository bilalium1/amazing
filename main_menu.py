from typing import Any


def draw_menu(mlx: Any, mlx_ptr: Any) -> Any:
    menu_w = 550
    menu_h = 400
    menu_win = mlx.mlx_new_window(mlx_ptr, menu_w, menu_h, "Main Menu")
    mlx.mlx_string_put(mlx_ptr, menu_win, 200, 50,
                       0xFFFFFF, "=== MAZE GENERATOR ===")
    mlx.mlx_string_put(mlx_ptr, menu_win, 50, 120,
                       0xAAAAAA, "Controls & Shortcuts:")
    mlx.mlx_string_put(mlx_ptr, menu_win, 50, 150,
                       0xFFFFFF, "[ C ] - Change Color")
    mlx.mlx_string_put(mlx_ptr, menu_win, 50, 180,
                       0xFFFFFF, "[ S ] - Solve Maze Hide Solve")
    mlx.mlx_string_put(mlx_ptr, menu_win, 50, 210,
                       0xFFFFFF, "[ R ] - Regenerate maze")
    mlx.mlx_string_put(mlx_ptr, menu_win, 50, 270,
                       0xFFFFFF, "[ ARROWS ] - Move exit point.")
    mlx.mlx_string_put(mlx_ptr, menu_win, 50, 240,
                       0xFFFFFF, "[ ESC ] - Exit")

    mlx.mlx_string_put(mlx_ptr, menu_win, 200, 320, 0x6C3BAA,
                       "Press [SPACE] to start")
    return (menu_win)
