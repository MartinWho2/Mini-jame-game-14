def parse_level(tile_file_name: str, movable_file_name: str, level_name: int):
    dict = {}

    # Tiles
    flag_idx = 34
    hole_idx = 32
    button_idx = 31
    laser_right = 13, 1
    laser_left = 19, 7
    laser_up = 22, 10
    laser_down = 16, 4
    wall_vert = 28
    wall_hor = 25

    # Movable
    box = 0
    guard = 1
    spawn = 2

    # with open(tile_file_name, 'r') as f:
    #     for idx, line in enumerate(f.readlines()):
    #         # robert