# 99899999989
import pygame
import time
from pygame.locals import *
from pygame import mixer
import json
from random import randint
pygame.init()
mixer.init()

ratio = 1920/pygame.display.Info().current_w
ratioy = 1080/pygame.display.Info().current_h

pygame.mixer.music.load('mc_backgroundloop.mp3')
pygame.mixer.music.play(-1, 0.5)
pygame.mixer.music.set_volume(0.5)

click = pygame.mixer.Sound('mc_click.mp3')
click2 = pygame.mixer.Sound('mc_click2.mp3')
boing = pygame.mixer.Sound('boing.mp3')
click.set_volume(0.6)
click2.set_volume(0.6)
boing.set_volume(0.6)

timing = time.time()

clickable = False
clicked = False
menu = True
is_shop = False
is_wardrobe = False
is_settings = False

cps = 0
click_time = time.time()
ua = False
u1 = False
u2 = False
u3 = False
u4 = False
u5 = False
u6 = False
u7 = False
u8 = False
u9 = False
freq = 0.5
leftclick = True
# mw = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))
mw = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h))

pygame.display.set_caption('Mushroom Clicker')
pygame.display.set_icon(pygame.image.load('mc_icon.png'))
green = pygame.transform.scale(pygame.image.load('mc_greenshade.png').convert_alpha(), (60/ratio, 60/ratioy))

with open('wardrobe.json', 'r') as file:
    wardrobe = json.load(file)
with open('settings.json', 'r') as file:
    options = json.load(file)
auto = wardrobe['auto']
glasses_visible = wardrobe['glasses']
hat_visible = wardrobe['hat']
clock = pygame.time.Clock()

with open ('balance.json', 'r') as file:
    money_balance = json.load(file)
balance = money_balance['balance']
with open('upgrades.json', 'r') as file:
    upgrades = json.load(file)

achievements = {'cool_style': False,
                'hard_working_shroom': False}


step = 1
pygame.font.init()
font2 = pygame.font.SysFont('MS Sans Serif', round(80/ratio))

# просто спрайти, які не функціонують
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, img, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.img = img
        self.image = pygame.transform.scale(pygame.image.load(img), (w/ratio, h/ratioy))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.w = w
        self.rect.h = h

    def show(self):
        mw.blit(self.image, (mw.get_rect().left + self.rect.x/ratio, mw.get_rect().top + self.rect.y/ratioy))

# кнопки (грибочок - теж кнопка)
class Cookie(pygame.sprite.Sprite):
    def __init__(self, img, x, y, w, h, is_clicked):
        pygame.sprite.Sprite.__init__(self)
        self.img = img
        self.image = pygame.transform.scale(pygame.image.load(img), (w/ratio, h/ratioy))
        self.rect = self.image.get_rect()
        self.rect.x = x/ratio
        self.rect.y = y/ratioy
        self.rect.w = w/ratio
        self.rect.h = h/ratioy
        self.is_clicked = is_clicked
    def click(self, x_offset, y_offset):
        self.image = pygame.transform.scale(pygame.image.load(self.img), (self.rect.w*0.95, self.rect.h*0.95))
        self.rect.x += x_offset
        self.rect.y += y_offset
        self.is_clicked = True

    def release(self, x_offset, y_offset):
        if self.is_clicked:
            self.image = pygame.transform.scale(pygame.image.load(self.img), (self.rect.w, self.rect.h))
            self.rect.x -= x_offset
            self.rect.y -= y_offset
        self.is_clicked = False
    def show(self):
        mw.blit(self.image, (mw.get_rect().left + self.rect.x, mw.get_rect().top + self.rect.y))

# покращення
class Upgrade(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, locked_img, img, bought_img):
        pygame.sprite.Sprite.__init__(self)
        self.locked_img = locked_img
        self.img = img
        self.bought_img = bought_img
        self.locked_img = pygame.transform.scale(pygame.image.load(locked_img).convert_alpha(), (w/ratio, h/ratioy))
        self.image = pygame.transform.scale(pygame.image.load(img).convert_alpha(), (w/ratio, h/ratioy))
        self.bought_img = pygame.transform.scale(pygame.image.load(bought_img).convert_alpha(), (w/ratio, h/ratioy))
        self.rect = self.image.get_rect()
        self.rect.x = x/ratio
        self.rect.y = y/ratioy
        self.rect.w = w/ratio
        self.rect.h = h/ratioy
    def showlocked(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))
        mw.blit(self.locked_img, (self.rect.x, self.rect.y))
    def show(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))
    def showbought(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))
        mw.blit(self.bought_img, (self.rect.x, self.rect.y))

# сюда какие-то классы

curx, cury = pygame.mouse.get_pos()

# елементи гри (кнопки, спрайти, досягнення...)

upgradeauto_icon = GameSprite('mc_cursor.png', 200 , 200 , 100 , 100 )

auto_v = Cookie('mc_tick.png', 320 , 220 , 60 , 60 , False)
auto_x = Cookie('mc_x.png', 400 , 220 , 60 , 60 , False)

u1_v = Cookie('mc_tick.png', 320 , 370 , 60 , 60 , False)
u1_x = Cookie('mc_x.png', 400 , 370 , 60 , 60 , False)

u2_v = Cookie('mc_tick.png', 320 , 520 , 60 , 60 , False)
u2_x = Cookie('mc_x.png', 400 , 520 , 60 , 60 , False)

u3_v = Cookie('mc_tick.png', 320 , 670 , 60 , 60 , False)
u3_x = Cookie('mc_x.png', 400 , 670 , 60 , 60 , False)

u4_v = Cookie('mc_tick.png', 620 , 220 , 60 , 60 , False)
u4_x = Cookie('mc_x.png', 700 , 220 , 60 , 60 , False)

u5_v = Cookie('mc_tick.png', 620, 370, 60, 60, False)
u5_x = Cookie('mc_x.png', 700, 370, 60, 60, False)

u6_v = Cookie('mc_tick.png', 620, 520, 60, 60, False)
u6_x = Cookie('mc_x.png', 700, 520, 60, 60, False)

u7_v = Cookie('mc_tick.png', 620, 670, 60, 60, False)
u7_x = Cookie('mc_x.png', 700, 670, 60, 60, False)

u8_v = Cookie('mc_tick.png', 920, 220, 60, 60, False)
u8_x = Cookie('mc_x.png', 1000, 220, 60, 60, False)

u9_v = Cookie('mc_tick.png', 920, 370, 60, 60, False)
u9_x = Cookie('mc_x.png', 1000, 370, 60, 60, False)

cur_v = Cookie('mc_tick.png', 900, 350, 60, 60, False)
cur_x = Cookie('mc_x.png', 1000, 350, 60, 60, False)
cursor_icon = GameSprite('mc_cursor.png',800, 350, 60, 60)

upgradecrown = Upgrade(960, 700, 500/1.5, 200, 'mc_locked_shade.png', 'mc_upgradecrown.png', 'mc_greenshade.png')
upgradehoop = Upgrade(610, 700, 500/1.5, 200, 'mc_locked_shade.png', 'mc_upgradehoop.png', 'mc_greenshade.png')
upgradeball = Upgrade(1310, 450, 500/1.5, 200, 'mc_locked_shade.png', 'mc_upgradeball.png', 'mc_greenshade.png')
upgradeskate = Upgrade(960, 450, 500/1.5, 200, 'mc_locked_shade.png', 'mc_upgradeskate.png', 'mc_greenshade.png')
upgradelawn = Upgrade(610 , 450 , 500/1.5 , 200 , 'mc_locked_shade.png', 'mc_upgrade5.png', 'mc_greenshade.png')
upgradedinny = Upgrade(260 , 450 , 500/1.5 , 200 , 'mc_locked_shade.png', 'mc_upgradedinny.png', 'mc_greenshade.png')
upgradeocto = Upgrade(1310 , 200 , 500/1.5 , 200 , 'mc_locked_shade.png', 'mc_upgradeocto.png', 'mc_greenshade.png')
upgrade2 = Upgrade(960 , 200 , 500/1.5 , 200 , 'mc_locked_shade.png', 'mc_upgrade2.png', 'mc_greenshade.png')
upgrade1 = Upgrade(610 , 200 , 500/1.5 , 200 , "mc_locked_shade.png", 'mc_upgrade1.png', 'mc_greenshade.png')
autoclicker = Upgrade(260 , 200 , 500/1.5 , 200 , "mc_locked_shade.png", 'mc_upgradeauto.png', 'mc_greenshade.png')

lawn_icon = GameSprite('mc_grassfield839x402.png', 500, 370, 839/8/ratio, 402/8/ratioy)

bg = GameSprite('bg.jpg', 0, 0, 1920, 1080)
help_screen = GameSprite('mc_help.png', 0, 0, 1920, 1080)
title = GameSprite('mc_title.png', 0, 0,1920, 1080)
coin = GameSprite('coin.png', 20 , 20 , 100 , 100 )
test_cookie = Cookie('shroom.png', 720 , 270 , 525 , 525 , False)
test_cookie.rect.center = mw.get_rect().center
cursor = Cookie('mc_cursor.png', curx, cury, 296/8 , 296/8 , False)
glasses = Cookie('mc_glasses.png', 808 , 615 , 921/3 , 324/3 , False)
hat = Cookie('mc_hat.png', 838 , 175 , 250 , 250 , False)
cross1 = Cookie('mc_cross.png', 10 , 10 , 100 , 100 , False)
return_button = Cookie('mc_return.png', 10 , 980 , 100 , 100 , False)
shop_button = Cookie('mc_shopbutton.png', 1810 , 975 , 100 , 100 , False)
shop = GameSprite('mc_shop.png', 0, 0, 1920 , 1080 )
shop_return_button = Cookie('mc_return.png', 200 , 900 , 100 , 100 , False)
ach_return = Cookie('mc_return.png', 200 , 900 , 100 , 100 , False)
exclamation = GameSprite('mc_available.png', 1780 , 925 , 50 , 50 )
hanger = Cookie('mc_wardrobe.png', 1690 , 975 , 125 , 100 , False)
octopus = Cookie('mc_octopus.png', 1100 , 670 , 200 , 200 , False)
dinosaur = Cookie('mc_dinosaur 719x927.png', 570 , 560 , 719/3.2 , 927/3.2 , False)
achievementsscreen = GameSprite('mc_achievements_screen.png', 0, 0, 1920 , 1080 )
glasses_w = GameSprite('mc_glasses.png', 200 , 380 , 100 , 40 )
hat_w = GameSprite('mc_hat.png', 200 , 500 , 100 , 100 )
octopus_w = GameSprite('mc_octopus.png', 620 , 670 , 200 , 200 )
octopus_icon = GameSprite('mc_octopus.png', 200 , 650 , 100 , 100 )
dinosaur_icon = GameSprite('mc_dinosaur 719x927.png', 500 , 180 , 100 , 120 )
lawn = Cookie('mc_grassfield839x402.png', 530 , 600 , 839 , 402 , False)

skate = Cookie('mc_skate375x231.png', 780, 660, 375, 231, False)
skate_icon = GameSprite('mc_skate375x231.png', 500, 510, 100, 75)

ball = Cookie('mc_ball.png', 550, 400, 150, 150, False)
ball_icon = GameSprite('mc_ball.png', 500, 660, 80, 80)

hoop = Cookie('mc_hoop.png', 1330, 350, 300, 440, False)
hoop_icon = GameSprite('mc_hoopicon.png', 800, 220, 75, 75)

crown = Cookie('mc_crown.png', 730, 150, 500, 350, False)
crown_icon = GameSprite('mc_crown.png', 800, 350, 100, 75)

settings = GameSprite('mc_settings.png', 0, 0, 1920, 1080)

settings_button = Cookie('mc_cog.png', 1570 , 975 , 100 , 100 , False)
settings_return = Cookie('mc_return.png', 200 , 900 , 100 , 100 , False)

music = Cookie('mc_music.png', 800, 200, 100, 100, False)
sound = Cookie('mc_sound.png', 950, 200, 100, 100, False)
# сховати системний курсор
cps_a = cps
#ігровий цикл
game = True
while game:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('balance.json', 'w') as file:
                json.dump(money_balance, file)
            with open('upgrades.json', 'w') as file_upgrades:
                json.dump(upgrades, file_upgrades)
            with open('wardrobe.json', 'w') as file:
                json.dump(wardrobe, file)
            with open('settings.json', 'w') as file:
                json.dump(options, file)
            game = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            leftclick = True
        elif event.type == pygame.MOUSEBUTTONUP:
            leftclick = False


    if time.time() - 1 > click_time:
        cps_a = cps
        cps = 0
        click_time = time.time()
    bg.show()
    if clickable:
        if upgrades['upgrade_5'] and wardrobe['lawn']:
            lawn.show()
        if upgrades['upgrade_6'] and wardrobe['skate']:
            skate.show()
        test_cookie.show()

        if upgrades['upgrade_3'] and clickable and wardrobe['octo']:
            octopus.show()

        if upgrades['upgrade_4'] and wardrobe['dinosaur']:
            dinosaur.show()

        if upgrades['upgrade_7'] and wardrobe['ball']:
            ball.show()
        if upgrades['upgrade_8'] and wardrobe['hoop']:
            hoop.show()

        coin.show()
        money = font2.render(str(balance) + ' (' + str(step) + ')', 1, (255, 255, 255))
        mw.blit(money, (130/ratio , 45 /ratioy))
        cps_text = font2.render('Кліків в секунду: ' + str(cps_a), 1, (255, 255, 255))
        mw.blit(cps_text, (1350 /ratio, 45 /ratioy))

        if upgrades['upgrade_1'] and clickable and wardrobe['glasses']:
            glasses.show()

        if upgrades['upgrade_2'] and clickable and wardrobe['hat']:
            hat.show()
        if upgrades['upgrade_9'] and wardrobe['crown']:
            crown.show()

        return_button.show()
        shop_button.show()
        hanger.show()
        settings_button.show()
        col_set = pygame.sprite.collide_rect(settings_button, cursor)
        if col_set:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and not is_shop and not is_wardrobe:
                    is_settings = True

        col_ach = pygame.sprite.collide_rect(hanger, cursor)
        if col_ach:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and not is_shop:
                    is_wardrobe = True

        if is_wardrobe:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    leftclick = True
                    print(leftclick)
                elif event.type == pygame.MOUSEBUTTONUP:
                    leftclick = False
                    print(leftclick)
            achievementsscreen.show()
            ach_return.show()

            col_ach_return = pygame.sprite.collide_rect(ach_return, cursor)
            if col_ach_return:
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        is_wardrobe = False

            if upgrades['upgrade_auto']:
                upgradeauto_icon.show( )
                auto_v.show()
                auto_x.show()

                col_v1 = pygame.sprite.collide_rect(cursor, auto_v)
                if col_v1:
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONDOWN and event.button == 1:
                            wardrobe['auto'] = True
                            mw.blit(green, (320 /ratio, 220 /ratioy))

                col_x1 = pygame.sprite.collide_rect(cursor, auto_x)
                if col_x1:
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONDOWN and event.button == 1:
                            wardrobe['auto'] = False
                            mw.blit(green, (400 /ratio , 220 /ratioy))

            if upgrades['upgrade_1']:
                glasses_w.show()
                u1_v.show()
                u1_x.show()

                if pygame.sprite.collide_rect(cursor, u1_v):
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONDOWN and event.button == 1:
                            wardrobe['glasses'] = True
                            mw.blit(green, (320 /ratio, 370 /ratioy))

                if pygame.sprite.collide_rect(cursor, u1_x):
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONDOWN and event.button == 1:
                            wardrobe['glasses'] = False
                            mw.blit(green, (400 /ratio, 370 /ratioy))

            if upgrades['upgrade_2']:
                hat_w.show()
                u2_v.show()
                u2_x.show()

                if pygame.sprite.collide_rect(cursor, u2_v):
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONDOWN and event.button == 1:
                            wardrobe['hat'] = True
                            mw.blit(green, (320 /ratio, 520 /ratioy))

                if pygame.sprite.collide_rect(cursor, u2_x):
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONDOWN and event.button == 1:
                            wardrobe['hat'] = False
                            mw.blit(green, (400 /ratio, 520 /ratioy))

            if upgrades['upgrade_3']:
                octopus_icon.show()
                u3_v.show()
                u3_x.show()

                if pygame.sprite.collide_rect(u3_v, cursor):
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONDOWN and event.button == 1:
                            wardrobe['octo'] = True
                            mw.blit(green, (320 /ratio, 670 /ratioy))

                if pygame.sprite.collide_rect(u3_x, cursor):
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONDOWN and event.button == 1:
                            wardrobe['octo'] = False
                            mw.blit(green, (400 /ratio, 670 /ratioy))

            if upgrades['upgrade_4']:
                dinosaur_icon.show()
                u4_v.show()
                u4_x.show()
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN and event.button == 1 and pygame.sprite.collide_rect(u4_v, cursor):
                        wardrobe['dinosaur'] = True
                        mw.blit(green, (620/ratio , 220 /ratioy))
                    if event.type == MOUSEBUTTONDOWN and event.button == 1 and pygame.sprite.collide_rect(u4_x, cursor):
                        wardrobe['dinosaur'] = False
                        mw.blit(green, (700 /ratio, 220/ratioy))

            if upgrades['upgrade_5']:
                lawn_icon.show()
                u5_v.show()
                u5_x.show()
                if pygame.sprite.collide_rect(u5_v, cursor) and leftclick:
                    wardrobe['lawn'] = True
                    # mw.blit(green, (620/ratio, 370/ratioy))
                elif pygame.sprite.collide_rect(u5_x, cursor) and leftclick:
                    wardrobe['lawn'] = False
                    # mw.blit(green, (700 / ratio, 370 / ratioy))
            if upgrades['upgrade_6']:
                skate_icon.show()
                u6_v.show()
                u6_x.show()
                if pygame.sprite.collide_rect(u6_v, cursor) and leftclick:
                    wardrobe['skate'] = True
                elif pygame.sprite.collide_rect(u6_x, cursor) and leftclick:
                    wardrobe['skate'] = False
            if upgrades['upgrade_7']:
                ball_icon.show()
                u7_v.show()
                u7_x.show()
                if pygame.sprite.collide_rect(u7_v, cursor) and leftclick:
                    wardrobe['ball'] = True
                elif pygame.sprite.collide_rect(u7_x, cursor) and leftclick:
                    wardrobe['ball'] = False

            if upgrades['upgrade_8']:
                hoop_icon.show()
                u8_v.show()
                u8_x.show()
                if pygame.sprite.collide_rect(u8_v, cursor) and leftclick:
                    wardrobe['hoop'] = True
                elif pygame.sprite.collide_rect(u8_x, cursor) and leftclick:
                    wardrobe['hoop'] = False
            if upgrades['upgrade_9']:
                crown_icon.show()
                u9_v.show()
                u9_x.show()
                if pygame.sprite.collide_rect(u9_v, cursor) and leftclick:
                    wardrobe['crown'] = True
                elif pygame.sprite.collide_rect(u9_x, cursor) and leftclick:
                    wardrobe['crown'] = False



        if ua or u1 or u2 or u3 or u4 or u5 or u6 or u7 or u8 or u9:
            exclamation.show()

        if is_shop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
            shop.show()
            shop_return_button.show()

            srbcol = pygame.sprite.collide_rect(shop_return_button, cursor)
            if srbcol:
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        is_shop = False

        if balance < 100 and not upgrades['upgrade_auto'] and is_shop:
            autoclicker.showlocked()
            ua = False

        if balance >= 100 and not upgrades['upgrade_auto']:
            ua = True

        if balance >= 100 and not upgrades['upgrade_auto'] and is_shop:
                autoclicker.show()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and colauto:
                        upgrades['upgrade_auto'] = True
                        wardrobe['auto'] = True
                        balance -= 100

        if upgrades['upgrade_auto'] and is_shop:
            autoclicker.showbought()
            ua = False
            auto = True


        if not upgrades['upgrade_1'] and is_shop:
            upgrade1.showlocked()
            u1 = False

        if balance >= 500 and not upgrades['upgrade_1']:
            u1 = True

        if balance >= 500 and not upgrades['upgrade_1'] and is_shop:
            upgrade1.show()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and col1:
                upgrades['upgrade_1'] = True
                balance -= 500
                wardrobe['glasses'] = True

        if upgrades['upgrade_1'] and is_shop:
            upgrade1.showbought()
            u1 = False

        if not upgrades['upgrade_2'] and is_shop:
            upgrade2.showlocked()
            u2 = False

        if not upgrades['upgrade_2'] and balance >= 1000:
            u2 = True

        if not upgrades['upgrade_2'] and balance >= 1000 and upgrades['upgrade_1'] and is_shop:
            upgrade2.show()

            col2 = pygame.sprite.collide_rect(upgrade2, cursor)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and col2 and upgrades['upgrade_1']:
                    upgrades['upgrade_2'] = True
                    balance -= 1000
                    wardrobe['hat'] = True
        if upgrades['upgrade_2'] and is_shop:
            upgrade2.showbought()
            u2 = False

        if not upgrades['upgrade_3'] and is_shop:
            upgradeocto.showlocked()
            u3 = False

        if not upgrades['upgrade_3'] and upgrades['upgrade_2'] and balance >= 2500:
            u3 = True

        if not upgrades['upgrade_3'] and upgrades['upgrade_2'] and balance >= 2500 and is_shop:
            upgradeocto.show()

            colocto = pygame.sprite.collide_rect(upgradeocto, cursor)
            if colocto:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and colocto and upgrades['upgrade_2']:
                        upgrades['upgrade_3'] = True
                        balance -= 2500
                        wardrobe['octo'] = True

        if upgrades['upgrade_3'] and is_shop:
            upgradeocto.showbought()
            u3 = False

        if not upgrades['upgrade_4'] and is_shop:
            upgradedinny.showlocked()
            u4 = False

        if not upgrades['upgrade_4'] and upgrades['upgrade_3'] and balance >= 10000:
            u4 = True

        if not upgrades['upgrade_4'] and upgrades['upgrade_3'] and balance >= 10000 and is_shop:
            upgradedinny.show()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pygame.sprite.collide_rect(upgradedinny, cursor) and upgrades['upgrade_3']:
                    upgrades['upgrade_4'] = True
                    balance -= 10000
                    wardrobe['dinosaur'] = True
        if upgrades['upgrade_4'] and is_shop:
            upgradedinny.showbought()
            u4 = False

        if not upgrades['upgrade_5'] and is_shop:
            upgradelawn.showlocked()
            u5 = False

        if not upgrades['upgrade_5'] and upgrades['upgrade_4'] and balance >= 22000:
            u5 = True

        if not upgrades['upgrade_5'] and upgrades['upgrade_4'] and balance >= 22000 and is_shop:
            upgradelawn.show()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pygame.sprite.collide_rect(upgradelawn, cursor) and upgrades['upgrade_4']:
                    upgrades['upgrade_5'] = True
                    balance -= 22000
                    wardrobe['lawn'] = True

        if upgrades['upgrade_5'] and is_shop:
            upgradelawn.showbought()
            u5 = False

        if not upgrades['upgrade_6'] and is_shop:
            upgradeskate.showlocked()
            u6 = False

        if not upgrades['upgrade_6'] and upgrades['upgrade_5'] and balance >= 50000:
            u6 = True

        if not upgrades['upgrade_6'] and upgrades['upgrade_5'] and balance >= 50000 and is_shop:
            upgradeskate.show()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pygame.sprite.collide_rect(upgradeskate, cursor) and upgrades['upgrade_5']:
                    upgrades['upgrade_6'] = True
                    balance -= 50000
                    wardrobe['skate'] = True

        if upgrades['upgrade_6'] and is_shop:
            upgradeskate.showbought()
            u6 = False

        if not upgrades['upgrade_7'] and is_shop:
            upgradeball.showlocked()
            u7 = False

        if not upgrades['upgrade_7'] and upgrades['upgrade_6'] and balance >= 100000:
            u7 = True

        if not upgrades['upgrade_7'] and upgrades['upgrade_6'] and balance >= 100000 and is_shop:
            upgradeball.show()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pygame.sprite.collide_rect(upgradeball, cursor) and upgrades['upgrade_6']:
                    upgrades['upgrade_7'] = True
                    balance -= 100000
                    wardrobe['ball'] = True

        if upgrades['upgrade_7'] and is_shop:
            upgradeball.showbought()
            u7 = False

        if not upgrades['upgrade_8'] and is_shop:
            upgradehoop.showlocked()
            u8 = False

        if not upgrades['upgrade_8'] and upgrades['upgrade_7'] and balance >= 400000:
            u8 = True

        if not upgrades['upgrade_8'] and upgrades['upgrade_7'] and balance >= 400000 and is_shop:
            upgradehoop.show()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pygame.sprite.collide_rect(
                        upgradehoop, cursor) and upgrades['upgrade_7']:
                    upgrades['upgrade_8'] = True
                    balance -= 400000
                    wardrobe['hoop'] = True

        if upgrades['upgrade_8'] and is_shop:
            upgradehoop.showbought()
            u8 = False

        if not upgrades['upgrade_9'] and is_shop:
            upgradecrown.showlocked()
            u9 = False

        if not upgrades['upgrade_9'] and upgrades['upgrade_8'] and balance >= 1000000:
            u9 = True

        if not upgrades['upgrade_9'] and upgrades['upgrade_8'] and balance >= 1000000 and is_shop:
            upgradecrown.show()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pygame.sprite.collide_rect(
                        upgradecrown, cursor) and upgrades['upgrade_8']:
                    upgrades['upgrade_9'] = True
                    balance -= 1000000
                    wardrobe['crown'] = True

        if upgrades['upgrade_9'] and is_shop:
            upgradecrown.showbought()
            u9 = False

        if is_settings:
            settings.show()
            settings_return.show()
            settings_return_col = pygame.sprite.collide_rect(settings_return, cursor)
            if settings_return_col:
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        is_settings = False
            music.show()
            sound.show()
            cur_v.show()
            cur_x.show()
            cursor_icon.show()
            if pygame.sprite.collide_rect(music, cursor):
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONUP and event.button == 1 and options['music'] == True:
                        pygame.mixer.music.set_volume(0)
                        music.image = pygame.transform.scale(pygame.image.load('mc_nomusic.png'), (100, 100))
                        options['music'] = False
                    elif event.type == MOUSEBUTTONUP and event.button == 1 and options['music'] == False:
                        pygame.mixer.music.set_volume(0.5)
                        music.image = pygame.transform.scale(pygame.image.load('mc_music.png'), (100, 100))
                        options['music'] = True
            if pygame.sprite.collide_rect(sound, cursor):
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONUP and event.button == 1 and options['sound'] == True:
                        click.set_volume(0)
                        click2.set_volume(0)
                        boing.set_volume(0)
                        sound.image = pygame.transform.scale(pygame.image.load('mc_nosound.png'), (100, 100))
                        options['sound'] = False
                    elif event.type == MOUSEBUTTONUP and event.button == 1 and options['sound'] == False:
                        click.set_volume(0.6)
                        click2.set_volume(0.6)
                        boing.set_volume(0.6)
                        sound.image = pygame.transform.scale(pygame.image.load('mc_sound.png'), (100, 100))
                        options['sound'] = True
            if pygame.sprite.collide_rect(cur_v, cursor):
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONUP and event.button == 1:
                        options['cursor'] = True
            if pygame.sprite.collide_rect(cur_x, cursor):
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONUP and event.button == 1:
                        options['cursor'] = False


        # if balance == 25:
        #     print('Ви можете прокачати свій грибочок!')

        colreturn = pygame.sprite.collide_rect(return_button, cursor)
        if colreturn:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    menu = True
                    clickable = False

                if event.type == MOUSEBUTTONUP:
                    menu = True
                    clickable = False

        colshop = pygame.sprite.collide_rect(shop_button, cursor)
        if colshop:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and not is_wardrobe:
                    is_shop = True


    col = pygame.sprite.collide_rect(test_cookie, cursor)
    colauto = pygame.sprite.collide_rect(autoclicker, cursor)
    col1 = pygame.sprite.collide_rect(upgrade1, cursor)

    money_balance['balance'] = balance
    money_balance['step'] = step

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            with open('balance.json', 'w') as file:
                json.dump(money_balance, file)
            with open('upgrades.json', 'w') as file:
                json.dump(upgrades, file)
            with open('wardrobe.json', 'w') as file:
                json.dump(wardrobe, file)
            with open('settings.json', 'w') as file:
                json.dump(options, file)
            game = False

    if clickable:
        if keys[pygame.K_BACKSPACE]:
            clickable = False
            menu = True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not clicked and col and not pygame.sprite.collide_rect(cursor, octopus) and not is_shop and not is_wardrobe and not pygame.sprite.collide_rect(cursor, dinosaur) and not is_settings:
            test_cookie.click(10, 10)
            if upgrades['upgrade_1']:
                glasses.click(5/ratio, -5/ratioy)
            if upgrades['upgrade_2']:
                hat.click(5, 15)
            if upgrades['upgrade_9']:
                crown.click(10/ratio, 15/ratioy)
            click.play()
            balance += step
            cps += 1
            # print(balance)
            clicked = True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not clicked and pygame.sprite.collide_rect(cursor, octopus) and wardrobe['octo'] and not is_shop and not is_wardrobe:
            octopus.click(5, 5)
            click2.play()
            clicked = True
            cps += 1

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            octopus.release(5, 5)
            crown.release(10, 15)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not clicked and pygame.sprite.collide_rect(cursor, dinosaur) and wardrobe['dinosaur'] and not is_shop and not is_wardrobe:
            dinosaur.click(5, 5)
            click2.play()
            clicked = True
            cps += 1

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dinosaur.release(5, 5)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            test_cookie.release(10, 10)
            clicked = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not clicked and pygame.sprite.collide_rect(
        cursor, ball) and wardrobe['ball'] and not is_shop and not is_wardrobe:
                ball.click(5, 5)
                boing.play()
                clicked = True
                cps += 1
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            ball.release(5, 5)
            clicked = False

            if upgrades['upgrade_1']:
                glasses.release(5/ratio, -5/ratioy)
            if upgrades['upgrade_2']:
                hat.release(5, 15)

            clicked = False


    if keys[pygame.K_q] and balance > 0:
        balance -= 5
    if keys[pygame.K_e] and balance > 0:
        balance += 5
    if keys[pygame.K_a] and balance > 0:
        balance += 50
    if keys[pygame.K_d] and balance > 0:
        balance += 500
    if balance < 0:
        balance = 0
    click_to_start = font2.render('Натисніть пробіл, щоб почати', 1, (255, 255, 255))
    help_splash = font2.render('H - допомога', 1, (255, 255, 255))

    if menu and not clickable:
        title.show()
        mw.blit(click_to_start, (mw.get_rect().centerx - 400/ratio , mw.get_rect().bottom - 200/ratioy))
        mw.blit(help_splash, (mw.get_rect().centerx - 200/ratio , mw.get_rect().bottom - 100/ratioy))
        cross1.show()

        for event in pygame.event.get():
            if keys[pygame.K_SPACE] or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not pygame.sprite.collide_rect(cross1, cursor):
                clickable = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clickable = True
            if keys[pygame.K_ESCAPE] or event.type == pygame.QUIT or pygame.sprite.collide_rect(cross1, cursor) and event.type == pygame.MOUSEBUTTONDOWN:
                with open('balance.json', 'w') as file:
                    json.dump(money_balance, file)
                with open('upgrades.json', 'w') as file_upgrades:
                    json.dump(upgrades, file_upgrades)
                with open('wardrobe.json', 'w') as file:
                    json.dump(wardrobe, file)
                with open('settings.json', 'w') as file:
                    json.dump(options, file)
                game = False

    if upgrades['upgrade_auto'] and wardrobe['auto']:
        if time.time() - freq > timing:
            balance += step
            timing = time.time()
            click.play()

    if upgrades['upgrade_1']:
        step = 2
    if upgrades['upgrade_2']:
        step = 4
    if upgrades['upgrade_3']:
        step = 7
    if upgrades['upgrade_4']:
        step = 10
    if upgrades['upgrade_5']:
        freq = 0.2
    if upgrades['upgrade_6']:
        step = 25
    if upgrades['upgrade_7']:
        freq = 0.1
    if upgrades['upgrade_8']:
        step = 50
    if keys[pygame.K_h]:
        help_screen.show()

    # a.show()
    # if keys[pygame.K_p]:
    #     a.unlock()


    if options['cursor']:
        cursor.show()
        pygame.mouse.set_visible(False)
    if not options['cursor']:
        pygame.mouse.set_visible(True)
    curx, cury = pygame.mouse.get_pos()
    cursor.rect.x = curx
    cursor.rect.y = cury
    pygame.display.update()
