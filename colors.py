from math import sqrt

gartic_colors = [
    (0, 0, 0),
    (255, 255, 255),
    (1, 116, 32),
    (17, 176, 60),
    (176, 112, 28),
    (255, 193, 38),
    (102, 102, 102),
    (170, 170, 170),
    (105, 21, 6),
    (255, 0, 19),
    (153, 0, 78),
    (255, 0, 143),
    (0, 80, 205),
    (38, 201, 255),
    (150, 65, 18),
    (255, 120, 41),
    (203, 90, 87),
    (254, 175, 168),
]

gartic_colors_location = {
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
}


def get_location_white_color(resolution):
    return get_location_of_color(resolution, (255, 255, 255))


def get_location_of_color(resolution, color):
    index = gartic_colors.index(color)
    return gartic_colors_location[index][resolution]


def closest(color):
    r, g, b = color
    color_diffs = []
    for color in gartic_colors:
        cr, cg, cb = color
        color_diff = sqrt(abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]
