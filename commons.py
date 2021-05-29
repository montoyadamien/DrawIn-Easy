GAME_GARTIC = 'GP'
GAME_SKRIBBL = 'SIO'

GAMES_NAMES = {
    GAME_GARTIC: 'Gartic Phone',
    GAME_SKRIBBL: 'Skribbl.io'
}

GAMES = [GAME_GARTIC, GAME_SKRIBBL]


def get_game_name(game):
    return GAMES_NAMES[game]
