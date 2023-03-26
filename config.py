WIN_WIDTH = 640
WIN_HEIGHT = 480
TILESIZE = 32
RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE  = (0, 0, 255)
FPS = 30
PLAYER_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1
MAP_HEIGHT = 30 * 32
MAP_WIDTH = 80 *32

BULLET_SPD = 16
PLAYER_SPEED = 6
ENEMY_SPEED = 2
FONTSIZE = 16
tilemap = [
    '..................................................................................',
    '.                 BS                                B                            .',
    '.                 B                                 B                            .',
    '.                 B                                 B                            .',
    '.                 B          GGGGGGGGGGGGG          B                            .',
    '.                 B          GGGGGGGGGGGGG          B                            .',
    '.                 B          GGGGGGGGGGGGG          B                            .',
    '.                 B          GGGGGGGGGGGGG          B                            .',
    '.                 B          GGGGGGGGGGGGG          B                            .',
    '.BBBBBBBB         B                                 BBBBBBBBBBBBBBBBBBBB         .',
    '.                 B                                 B                            .',
    '.                 B                                 B                            .',
    '.                 B                                 B                            .',
    '.                 B                                NB                            .',
    '.          BBBBBBBBBBBBBBBBBBBBBBB       BBBBBBBBBBBBBBBBBBBBBBBBBBBBB           .',
    '.                                                                                .',
    '.                                                                                .',
    '.                                                                                .',
    '.                                                                                .',
    '.BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB    .',
    '.              B                       B                                    B    .',
    '.              B                       B                                    B    .',
    '.       B      B            B          B                                    B    .',
    '.BBB    BBB    B            B          B                                    B    .',
    '.         B    B            B     BBBBBBBBBBBBBBBBBBBBBBBBBBBB              B    .',
    '.         B    B            B                                               B    .',
    '.         B    BBBBBBBBBBGGGB                                               B    .',
    '.         BGGGGGGGGGGGGGGGGGB                                               C    .',
    '.         BGGGGGGGGGGGGGGGGGB                                               C    .',
    '..................................................................................',
]