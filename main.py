import pyxel
import random
import numpy as np
from const import *
from collections import namedtuple

class Enemy():
    def __init__(self, x, y, ICON, health):
        self.health = health
        self.ICON = ICON
        self.x = x
        self.y = y
    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.ICON[0], self.ICON[1], 8, 8, 9)

class App():
    
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Baby Meat Not Too Cold")
        pyxel.load("baby.pyxres")
        self.reset()
        self.intro = True
        self.playing = False
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.TEMPERATURE = 72
        self.METERS = 25 
        self.MVMT = 0 
        self.BABY_POS = BABY_UP
        self.blocks = []
        self.x_s = []
        self.y_s = []
        self.enemies = []
        self.baby_shots = 0
        self.shots = []
        self.toygun_x = SCREEN_WIDTH // 2
        self.game_frames = 0
        self.playing = True
        self.intro = False
        self.intro_counter = 0
        self.tips = False
        self.lose = False 
        self.win = False
        self.death = None

    def update(self):
        if self.playing:
            if self.lose or self.win:
                self.playing = False
            if self.METERS <= 0:
                self.win = True
            if self.TEMPERATURE < -50:
                self.lose = True
                self.death = 1
            if self.TEMPERATURE > 160:
                self.lose = True
                self.death = 2
            if self.baby_shots > 5:
                self.lose = True
                self.death = 3
            if len(self.enemies) > 20:
                self.lose = True
                self.death = 0
            if (pyxel.btn(pyxel.KEY_SPACE)):
                self.TEMPERATURE += 1.5
            else:            
                self.TEMPERATURE -= 2
        else:
            if self.lose and pyxel.btnp(pyxel.KEY_R):
                self.reset()
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
            if self.lose and pyxel.btnp(pyxel.KEY_I):
                self.tips = True
            if self.lose and self.tips and pyxel.btnp(pyxel.KEY_SPACE):
                self.tips = False
            if self.intro and pyxel.btnp(pyxel.KEY_C):
                self.intro_counter += 1
                if self.intro_counter > 7:
                    self.tips = True 
                    self.intro = False
            if (not self.lose) and self.tips and pyxel.btnp(pyxel.KEY_SPACE):
                self.tips = False
                self.playing = True

    def pick_comment(self):
        l = len(WEATHER_COMMENTS)-1
        for i in range(0, l):
            if self.TEMPERATURE >= 160 - (20*(i)):
                return l-i, (l-i)//3
            elif self.TEMPERATURE <= -40 + (20*(i)):
                return i, (i)//3

    def pick_loc(self):
        x = None
        y = None
        x_s = [enemy.x for enemy in self.enemies]
        y_s = [enemy.y for enemy in self.enemies]
        while (x is None or x in x_s or self.on_baby(x, 0) or self.invalid_loc(x, 20)):
            x = np.random.choice(SCREEN_WIDTH, 1)
        while (y is None or y in y_s or self.on_baby(0, y) or self.invalid_loc(50, y)):
            y = np.random.choice(SCREEN_HEIGHT, 1)
        return x, y

    def on_enemy(self, x, y):
        for enemy in self.enemies:
            if x >= enemy.x and \
               x <= enemy.x + 8 and \
               y >= enemy.y and \
               y <= enemy.y + 8:
               return True, enemy
        return False, None

    def on_baby(self, x, y):
        if x:
            toggle = [0, 0] if self.BABY_POS == BABY_RIGHT else [8, 8]
            if x >= (SCREEN_WIDTH//2)-12+toggle[0] and \
            x <= (SCREEN_WIDTH//2)-12+toggle[0]+ self.BABY_POS[2][0] and \
            y >= 24-toggle[1] and \
            y <= 24-toggle[1]+self.BABY_POS[2][1]:
                return True 
        return False
        
    def invalid_loc(self, x, y):
        if x > SCREEN_WIDTH - 16 or \
           x < 0 or \
           y > SCREEN_HEIGHT-32 or \
           y < 16:
           return True
        else: return False
    def invalid_shot(self, x, y):
        if y < 16:
           return True
        else: return False

    def choose_enemy(self):
        if self.game_frames % 12 == 0:
            if self.TEMPERATURE < -20: return PENGUIN, p_health
            elif self.TEMPERATURE < 0: return ICICLE, ic_health
            elif self.TEMPERATURE < 0: return ICE_CREAM, i_c_health
            elif self.TEMPERATURE > 120: return FIREBALL, f_health
            elif self.TEMPERATURE > 110: return BARNACLE, b_health
            elif self.TEMPERATURE > 90: return LIZARD, l_health
            elif self.TEMPERATURE > 70: return MOSQUITO, m_health
        return None, None

    def update_terrain(self):
        for i in range(0, len(self.blocks)):
            pyxel.blt(28+(i*16),(SCREEN_HEIGHT-8)-(i*16),0, self.blocks[i][0], self.blocks[i][1], 16, 16, 9)
        if self.game_frames % 100 == 0:
            self.blocks.remove(self.blocks[0])
            idx = np.random.choice(5, 1)
            self.blocks.append(terrain[idx[0]])
            self.METERS -= 1

    def update_shot(self):
        for shot in self.shots:
            hit_enemy, enemy = self.on_enemy(shot[0], shot[1])
            if self.on_baby(shot[0], shot[1]):
                self.baby_shots+=1
                self.shots.remove(shot)
            elif hit_enemy:
                self.shots.remove(shot)
                enemy.health -= 1
                if enemy.health == 0:
                    self.enemies.remove(enemy)
            elif self.invalid_shot(shot[0], shot[1]):
                self.shots.remove(shot)
            else:
                shot[1] -= 1

    def shoot(self):
        shot = [self.toygun_x+3, SCREEN_HEIGHT-10] 
        self.shots.append(shot)

    def draw_scene(self):
        # Drawing the default steps # 
        for i in range(0, 6):
            l = 6-i
            for k in range(0, l):
                x = 124-(k*16)
                y = SCREEN_HEIGHT-8-(i*16)
                pyxel.blt(x, y, 0, DEFAULT[0], DEFAULT[0], 16, 16, 0)

        # Show game info #
        pyxel.rect(0, 0, 100, HEIGHT_SCORE, 0)
        pyxel.text(0, 0, f" steps from meat: {self.METERS}", 7)

        # Weather comments # 
        index, color = self.pick_comment()
        comment = WEATHER_COMMENTS[index]
        text_x = self.center_text(comment, SCREEN_WIDTH)

        # bottom bar
        pyxel.rect(0, SCREEN_HEIGHT-8, SCREEN_WIDTH, 8, 13)
        pyxel.text(text_x, SCREEN_HEIGHT-pyxel.FONT_HEIGHT, comment, COLORS[color])

    def draw_enemy(self):
        # make an enemy appear given temperature #
        ENEMY, e_health = self.choose_enemy()
        if not ENEMY is None:
            x, y = self.pick_loc()
            enemy = Enemy(x, y, ENEMY, e_health)
            self.enemies.append(enemy)
        for enemy in self.enemies:
            enemy.draw()

    def draw_baby(self):
        # baby animation #
        toggle = [0, 0] if self.BABY_POS == BABY_RIGHT else [8, 8]
        pyxel.blt((SCREEN_WIDTH//2)-12+toggle[0], 24-toggle[1], 0, self.BABY_POS[self.MVMT][0], self.BABY_POS[self.MVMT][1], self.BABY_POS[2][0], self.BABY_POS[2][1], 0)
        if self.game_frames % 25 == 0:
            self.MVMT = 0 if self.MVMT == 1 else 1
        if self.game_frames % 50 == 0:
            self.BABY_POS = BABY_RIGHT if self.BABY_POS == BABY_UP else BABY_UP

    def draw_terrain(self):
        if len(self.blocks) == 0:
            self.blocks = [terrain[idx] for idx in np.random.choice(5, 6)]
        else:
            self.update_terrain()

    def draw_gun(self):
        if len(self.shots) > 0:
            self.draw_shots()
        if pyxel.btn(pyxel.KEY_RIGHT):
            if self.toygun_x < SCREEN_WIDTH-16:
                self.toygun_x += 1
        elif pyxel.btn(pyxel.KEY_LEFT):
            if self.toygun_x > 0:
                self.toygun_x -= 1
        if pyxel.btnp(pyxel.KEY_UP):
            self.shoot()
        pyxel.blt(self.toygun_x, SCREEN_HEIGHT-16, 0, SMALL_GUN[0], SMALL_GUN[1], 8, 16, 9)
    
    def draw_shots(self):
        for shot in self.shots:
            pyxel.pset(shot[0], shot[1], 8)
        self.update_shot()

    def draw_lose(self):
        pyxel.cls(13)
        MESSAGE = lose_states[self.death]
        pyxel.text(0, 15, "ANGRY BABY", 9)
        pyxel.text(50, 75, "COLD BABY", 10)
        pyxel.text(20, 5, "ANGRY BABY", 5)
        pyxel.text(100, 50, "COLD BABY", 7)
        pyxel.text(70, 80, "ANGRY BABY", 4)
        pyxel.text(5, 60, "COLD BABY", 2)
        pyxel.text(40, 30, "ANGRY BABY", 1)
        pyxel.text(0, 75, "COLD BABY", 12)
        pyxel.text(100, 75, "ANGRY BABY", 14)
        pyxel.text(90, 20, "COLD BABY", 15)
        pyxel.text(70, -2, "ANGRY BABY", 11)
        x_val = self.center_text(MESSAGE, SCREEN_WIDTH)
        width = len(MESSAGE) * pyxel.FONT_WIDTH
        pyxel.rect(SCREEN_WIDTH//2-40, SCREEN_HEIGHT//2-32, 80, 64, 7)
        pyxel.text(SCREEN_WIDTH//2-30, SCREEN_HEIGHT//2-16, "Press R \n to play again", 0)
        pyxel.text(SCREEN_WIDTH//2-30, SCREEN_HEIGHT//2, "Press Q \n to quit", 0)
        pyxel.text(SCREEN_WIDTH//2-30, SCREEN_HEIGHT//2+16, "Press I \n for tips", 0)
        pyxel.text(x_val, SCREEN_HEIGHT//2-30, MESSAGE, 8)

    def draw_win(self):
        pyxel.cls(11)
        pyxel.text(0, 15, "HAPPY BABY", 9)
        pyxel.text(50, 75, "MEAT BABY", 10)
        pyxel.text(20, 5, "HAPPY BABY", 5)
        pyxel.text(100, 50, "MEAT BABY", 7)
        pyxel.text(70, 80, "HAPPY BABY", 4)
        pyxel.text(5, 60, "MEAT BABY", 2)
        pyxel.text(40, 30, "HAPPY BABY", 1)
        pyxel.text(0, 75, "MEAT BABY", 12)
        pyxel.text(100, 75, "HAPPY BABY", 14)
        pyxel.text(100, 75, "HAPPY BABY", 14)
        pyxel.text(90, 20, "MEAT BABY", 15)
        pyxel.text(70, -2, "HAPPY BABY", 13)
        pyxel.rect(SCREEN_WIDTH//2-32, SCREEN_HEIGHT//2-32, 64, 64, 7)
        text = "BABY GOT MEAT"
        pyxel.text(self.center_text(text, SCREEN_WIDTH), SCREEN_HEIGHT//2-30, text, 3)
        pyxel.text(SCREEN_WIDTH//2-30, SCREEN_HEIGHT//2+16, "Press Q \nto quit", 0)
        pyxel.blt(SCREEN_WIDTH//2-16, SCREEN_HEIGHT//2-16, 0, MEAT[0], MEAT[1], 32, 32, 9)

    def draw_tips(self):
        pyxel.cls(3)
        pyxel.text(2, 2, "GOAL: Reach the meat", 0)
        if self.lose:
            pyxel.text(2, 2+pyxel.FONT_HEIGHT, "Press -SPACE- to go back", 0)
        else:
            pyxel.text(2, 2+pyxel.FONT_HEIGHT, "Press -SPACE- to play", 0)
        pyxel.text(2, 18, "Hold space bar: raise temp\n\
                           \nL + R arrow keys: move gun\n\
                           \nU arrow key: shoot\n\
                           \nShoot often:enemies have health\
                           \n\nDon't shoot the baby.", 2)

    def draw_intro(self):
        pyxel.cls(6)
        pyxel.text(2, 2, "INTRO", 0)
        pyxel.text(2, pyxel.FONT_HEIGHT+2, "Press -C- to continue", 0)
        pyxel.text(2, 16, intro_dialogue[self.intro_counter], 9)

    def draw(self):
        if self.tips:
            self.draw_tips()
        elif self.win:
            self.draw_win()
        elif self.lose:
            self.draw_lose()
        elif self.intro:
            self.draw_intro()
        else:
            pyxel.cls(9)
            self.draw_baby()
            self.draw_terrain()
            self.draw_scene()
            self.draw_enemy()
            self.draw_gun()
            self.game_frames+=1

    @staticmethod
    def center_text(text, page_width, char_width=pyxel.FONT_WIDTH):
        """Helper function for calcuating the start x value for centered text."""
        text_width = len(text) * char_width
        return (page_width - text_width) // 2

App()
