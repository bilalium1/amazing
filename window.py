        # --- MAIN MENU SETUP ---
    menu_w = 600
    menu_h = 400
    menu_win = mlx.mlx_new_window(mlx_ptr, menu_w, menu_h, "Main Menu")

    def draw_menu():
        mlx.mlx_string_put(mlx_ptr, menu_win, 200, 50, 0xFFFFFF, "=== MAZE GENERATOR ===")
        mlx.mlx_string_put(mlx_ptr, menu_win, 50, 120, 0xAAAAAA, "Controls & Shortcuts:")
        mlx.mlx_string_put(mlx_ptr, menu_win, 50, 150, 0xFFFFFF, "[ C ] - Change Color")
        mlx.mlx_string_put(mlx_ptr, menu_win, 50, 180, 0xFFFFFF, "[ S ] - Solve Maze")
        mlx.mlx_string_put(mlx_ptr, menu_win, 50, 210, 0xFFFFFF, "[ M ] - Change Mode (Perfect/Random)")
        mlx.mlx_string_put(mlx_ptr, menu_win, 50, 240, 0xFFFFFF, "[ ESC ] - Exit")

        mlx.mlx_string_put(mlx_ptr, menu_win, 180, 320, 0x00FF00, "Press [ENTER] to start")

    draw_menu()

    def menu_key_hook(keycode, param):
        if keycode == ESC:
            mlx.mlx_destroy_window(mlx_ptr, menu_win)
            os._exit(0)
        elif keycode == KEY_ENTER:
            # Destroy the menu, and boot up the maze display
            mlx.mlx_destroy_window(mlx_ptr, menu_win)
            start_maze(mlx, mlx_ptr, width, height, size, start_pos, end_pos)

    # Attach menu hook and start the infinite MLX loop
    mlx.mlx_key_hook(menu_win, menu_key_hook, None)
    mlx.mlx_loop(mlx_ptr)