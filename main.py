import sys

import pygame
import random

from controls import move_player, move_player_with_joystick
from classes.constants import WIDTH, HEIGHT, FPS, SHOOT_DELAY
from functions import show_game_over, music_background
from menu import show_menu

from classes.player import Player
from classes.bullets import Bullet
from classes.refill import BulletRefill, HealthRefill, DoubleRefill, ExtraScore
from classes.meteors import Meteors, Meteors2, BlackHole
from classes.explosions import Explosion, Explosion2
from classes.enemies import Enemy1, Enemy2
from classes.bosses import Boss1, Boss2, Boss3


pygame.init()
music_background()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Heat")
clock = pygame.time.Clock()


explosions = pygame.sprite.Group()
explosions2 = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy1_group = pygame.sprite.Group()
enemy2_group = pygame.sprite.Group()
boss1_group = pygame.sprite.Group()
boss2_group = pygame.sprite.Group()
boss3_group = pygame.sprite.Group()
bullet_refill_group = pygame.sprite.Group()
health_refill_group = pygame.sprite.Group()
double_refill_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
meteor2_group = pygame.sprite.Group()
extra_score_group = pygame.sprite.Group()
black_hole_group = pygame.sprite.Group()
enemy2_bullets = pygame.sprite.Group()

boss1_bullets = pygame.sprite.Group()
boss2_bullets = pygame.sprite.Group()
boss3_bullets = pygame.sprite.Group()

boss1_health = 150
boss1_health_bar_rect = pygame.Rect(0, 0, 150, 5)
boss1_spawned = False

boss2_health = 150
boss2_health_bar_rect = pygame.Rect(0, 0, 150, 5)
boss2_spawned = False

boss3_health = 200
boss3_health_bar_rect = pygame.Rect(0, 0, 200, 5)
boss3_spawned = False

bg_y_shift = -HEIGHT
background_img = pygame.image.load('images/bg/background.jpg').convert()
background_img2 = pygame.image.load('images/bg/background2.png').convert()
background_img3 = pygame.image.load('images/bg/background3.png').convert()
background_img4 = pygame.image.load('images/bg/background4.png').convert()
background_top = background_img.copy()
current_image = background_img
new_background_activated = False

explosion_images = [pygame.image.load(f"images/explosion/explosion{i}.png") for i in range(8)]
explosion2_images = [pygame.image.load(f"images/explosion2/explosion{i}.png") for i in range(18)]
explosion3_images = [pygame.image.load(f"images/explosion3/explosion{i}.png") for i in range(18)]

enemy1_img = [
    pygame.image.load('images/enemy/enemy1_1.png').convert_alpha(),
    pygame.image.load('images/enemy/enemy1_2.png').convert_alpha(),
    pygame.image.load('images/enemy/enemy1_3.png').convert_alpha()
]
enemy2_img = [
    pygame.image.load('images/enemy/enemy2_1.png').convert_alpha(),
    pygame.image.load('images/enemy/enemy2_2.png').convert_alpha()
]
boss1_img = pygame.image.load('images/boss/boss1.png').convert_alpha()
boss2_img = pygame.image.load('images/boss/boss2_1.png').convert_alpha()
boss3_img = pygame.image.load('images/boss/boss3.png').convert_alpha()

health_refill_img = pygame.image.load('images/refill/health_refill.png').convert_alpha()
bullet_refill_img = pygame.image.load('images/refill/bullet_refill.png').convert_alpha()
double_refill_img = pygame.image.load('images/refill/double_refill.png').convert_alpha()

meteor_imgs = [
    pygame.image.load('images/meteors/meteor_1.png').convert_alpha(),
    pygame.image.load('images/meteors/meteor_2.png').convert_alpha(),
    pygame.image.load('images/meteors/meteor_3.png').convert_alpha(),
    pygame.image.load('images/meteors/meteor_4.png').convert_alpha()
]
meteor2_imgs = [
    pygame.image.load('images/meteors/meteor2_1.png').convert_alpha(),
    pygame.image.load('images/meteors/meteor2_2.png').convert_alpha(),
    pygame.image.load('images/meteors/meteor2_3.png').convert_alpha(),
    pygame.image.load('images/meteors/meteor2_4.png').convert_alpha()
]
extra_score_img = pygame.image.load('images/score/score_coin.png').convert_alpha()
black_hole_imgs = [
    pygame.image.load('images/hole/black_hole.png').convert_alpha(),
    pygame.image.load('images/hole/black_hole2.png').convert_alpha()
]

initial_player_pos = (WIDTH // 2, HEIGHT - 100)

score = 0
hi_score = 0
player = Player()
player_life = 200
bullet_counter = 200

paused = False
running = True

joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

show_menu_flag = True

def show_menu_and_run():
    global show_menu_flag, running, score, player_life, bullet_counter, player, boss1_spawned, boss1_health, boss2_spawned, boss2_health, boss3_spawned, boss3_health
    if show_menu_flag:
        menu.main()
        show_menu_flag = False
        score = 0
        player_life = 200
        bullet_counter = 200
        player.rect.topleft = initial_player_pos
        bullets.empty()
        bullet_refill_group.empty()
        health_refill_group.empty()
        double_refill_group.empty()
        extra_score_group.empty()
        black_hole_group.empty()
        meteor_group.empty()
        meteor2_group.empty()
        enemy1_group.empty()
        enemy2_group.empty()
        boss1_group.empty()
        boss2_group.empty()
        boss3_group.empty()
        explosions.empty()
        explosions2.empty()
        boss1_spawned = False
        boss1_health = 150
        boss2_spawned = False
        boss2_health = 150
        boss3_spawned = False
        boss3_health = 200

show_menu_and_run()

is_shooting = False
last_shot_time = 0

while running:
    show_menu_and_run()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not paused:
                if bullet_counter > 0 and pygame.time.get_ticks() - last_shot_time > SHOOT_DELAY:
                    last_shot_time = pygame.time.get_ticks()
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)
                    bullet_counter -= 1
                is_shooting = True

            elif event.key == pygame.K_ESCAPE:
                sys.exit(0)
            elif event.key == pygame.K_p or event.key == pygame.K_PAUSE
