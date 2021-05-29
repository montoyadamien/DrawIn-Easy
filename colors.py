from math import sqrt
from commons import GAME_GARTIC, GAME_SKRIBBL

pen_location = {
    GAME_GARTIC: {
        '2560x1440': (699, 1249),
    },
    GAME_SKRIBBL: {
        '2560x1440': (1354, 908),
    }
}

colors = {
    GAME_GARTIC: [
        (0, 0, 0, 255),
        (255, 255, 255, 255),
        (1, 116, 32, 255),
        (17, 176, 60, 255),
        (176, 112, 28, 255),
        (255, 193, 38, 255),
        (102, 102, 102, 255),
        (170, 170, 170, 255),
        (105, 21, 6, 255),
        (255, 0, 19, 255),
        (153, 0, 78, 255),
        (255, 0, 143, 255),
        (0, 80, 205, 255),
        (38, 201, 255, 255),
        (150, 65, 18, 255),
        (255, 120, 41, 255),
        (203, 90, 87, 255),
        (254, 175, 168, 255),
    ],
    GAME_SKRIBBL: [
        (255, 255, 255, 255),
        (0, 0, 0, 255),
        (193, 193, 193, 255),
        (76, 76, 76, 255),
        (239, 19, 11, 255),
        (116, 11, 7, 255),
        (255, 113, 0, 255),
        (194, 56, 0, 255),
        (255, 228, 0, 255),
        (323, 162, 0, 255),
        (0, 204, 0, 255),
        (0, 85, 16, 255),
        (0, 178, 255, 255),
        (0, 86, 158, 255),
        (35, 31, 211, 255),
        (14, 8, 101, 255),
        (163, 0, 186, 255),
        (85, 0, 105, 255),
        (211, 124, 170, 255),
        (167, 85, 116, 255),
        (160, 82, 45, 255),
        (99, 48, 13, 255),
    ]
}

colors_location = {
    GAME_GARTIC: {
        0: {  # black
            '2560x1440': (431, 528),  # x increment = 64, y increment = 68
        },
        1: {  # white
            '2560x1440': (431, 596),
        },
        2: {  # dark green
            '2560x1440': (431, 664),
        },
        3: {  # green
            '2560x1440': (431, 732),
        },
        4: {  # dark yellow
            '2560x1440': (431, 800),
        },
        5: {  # yellow
            '2560x1440': (431, 868),
        },
        6: {  # dark grey
            '2560x1440': (495, 528),
        },
        7: {  # grey
            '2560x1440': (495, 596),
        },
        8: {  # dark red
            '2560x1440': (495, 664),
        },
        9: {  # red
            '2560x1440': (495, 732),
        },
        10: {  # dark pink
            '2560x1440': (495, 800),
        },
        11: {  # pink
            '2560x1440': (495, 868),
        },
        12: {  # dark blue
            '2560x1440': (559, 528),
        },
        13: {  # blue
            '2560x1440': (559, 596),
        },
        14: {  # dark orange
            '2560x1440': (559, 664),
        },
        15: {  # orange
            '2560x1440': (559, 732),
        },
        16: {  # dark beige
            '2560x1440': (559, 800),
        },
        17: {  # beige
            '2560x1440': (559, 868),
        }
    },
    GAME_SKRIBBL: {
        0: {  # white
            '2560x1440': (906, 896),  # x increment = 24, y increment = 24
        },
        1: {  # black
            '2560x1440': (906, 920),
        },
        2: {  # grey
            '2560x1440': (930, 896),
        },
        3: {  # dark grey
            '2560x1440': (930, 920),
        },
        4: {  # red
            '2560x1440': (954, 896),
        },
        5: {  # dark red
            '2560x1440': (954, 920),
        },
        6: {  # orange
            '2560x1440': (978, 896),
        },
        7: {  # dark orange
            '2560x1440': (978, 920),
        },
        8: {  # yellow
            '2560x1440': (1002, 896),
        },
        9: {  # dark yellow
            '2560x1440': (1002, 920),
        },
        10: {  # green
            '2560x1440': (1026, 896),
        },
        11: {  # dark green
            '2560x1440': (1026, 920),
        },
        12: {  # blue
            '2560x1440': (1050, 896),
        },
        13: {  # dark blue
            '2560x1440': (1050, 920),
        },
        14: {  # more dark blue
            '2560x1440': (1074, 896),
        },
        15: {  # more more dark blue
            '2560x1440': (1074, 920),
        },
        16: {  # purple
            '2560x1440': (1098, 896),
        },
        17: {  # dark purple
            '2560x1440': (1098, 920),
        },
        18: {  # pink
            '2560x1440': (1122, 896),
        },
        19: {  # dark ink
            '2560x1440': (1122, 920),
        },
        20: {  # brown
            '2560x1440': (1146, 896),
        },
        21: {  # dark brown
            '2560x1440': (1146, 920),
        },
    }
}


def get_pen_location(resolution, game):
    return pen_location[game][resolution]


def get_location_white_color(resolution, game):
    return get_location_of_color(resolution, (255, 255, 255, 255), game)


def get_location_of_color(resolution, color, game):
    index = colors[game].index(color)
    return colors_location[game][index][resolution]


def closest(color, game):
    r, g, b, a = color
    color_diffs = []
    for color in colors[game]:
        cr, cg, cb, ca = color
        color_diff = sqrt(abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]
