import pyxel
BABY_RIGHT = [[8, 32], [8, 16], [24, 16]]
BABY_UP = [[40, 32], [40, 8], [16, 24]]

MEAT = [16, 0]

# Enemies
MOSQUITO = [24, 56]
m_health = 1
LIZARD = [8, 56]
l_health = 3
BARNACLE = [0, 64]
b_health = 4
FIREBALL = [8, 64]
f_health = 4
ICICLE = [16, 56]
ic_health = 3
PENGUIN = [16, 64]
p_health = 5
ICE_CREAM = [24, 64]
i_c_health = 4

BIG_GUN = [8, 80]
SMALL_GUN = [0, 80]

# Terrain # 
GRASS = [16, 72]
ROCKS = [32, 72]
MOUNTAINS = [16, 88]
CACTUS = [32, 88]
ROAD = [48, 72]

DEFAULT = [0, 0]

terrain = [GRASS, MOUNTAINS, ROCKS, CACTUS, ROAD]

COLORS = [7, 3, 14, 8]



SCREEN_WIDTH = 128
SCREEN_HEIGHT = 80

HEIGHT_SCORE = pyxel.FONT_HEIGHT
HEIGHT_DEATH = 5

intro_dialogue = ["You are tasked with \n\nbaby sitting Baby", 
            "Yes their name is Baby.", 
            "The room is set up with\n\
            \nBaby's favorite entertainment:\n\
            \nClimbing to reach the meat.\n\
            \nBaby loves meat.", 
            "This would be an easy task \n\
            \nBut the room has \n\na tricky thermostat\n\
            \nIf left alone the temperature \n\ndrops signficantly.",
            "So you will manually turn it up\n\
            \nBut not too much \n\nor you burn baby.", 
            "Also, creatures will come when \n\
            \nthe temperature is to their \n\nliking.\n\
            \nYou must dispose of them or \n\
            \nBaby will not climb to get meat.",
            "Once Baby has meat then you win. \n\
            \nWhat it is that you win \n\nI don't know.\n\
            \nThey don't tell me anything.",
            "Controls are shown on the \n\nnext page."]

lose_states = ["BABY HATES CROWDS", "BABY IS COLD", "YOU BURNED BABY", "YOU SHOT BABY"]

WEATHER_COMMENTS = ["ANGRY BABY",
                    "BRRRRRR BABY", 
                    "CHILLY BABY", 
                    "SWEATER BABY", 
                    "BREEZY BABY...", 
                    "COMFY BABY", 
                    "SWEATY BABY",
                    "BURN BABY BURN! BABY",
                    "DISCO INFERNO BABY",
                    "FIRE BABY",
                    "TOAST BABY"]
