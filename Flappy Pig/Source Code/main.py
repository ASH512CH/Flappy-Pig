import random
import sys
import time
import tkinter as tk
from tkinter.messagebox import showinfo
import pygame

#b = pygame.image.load('assets/img/character.png')
# HIDE TK WINDOW
root = tk.Tk()
root.withdraw()
# SHOW WELCOME
a = showinfo("<!WELCOME!>","welcome to PWB")
# START PYGAME
pygame.init()

# ALL VARIABLES
display_width = 440
display_height = 700
floor_x = 0
gravity = 0.25
character_movement = 0
obstacle_list = []
game_status = True
game_font = pygame.font.Font('assets/fonts/Minecraft.ttf', 40)
score = 0
speed_game_1 = 85
speed_game_2 = 100
high_score = 0
active_score = True
prev_score = 0
# --------------------------------------------------------- #
create_obstacle = pygame.USEREVENT
pygame.time.set_timer(create_obstacle, 930)
# --------------------------------------------------------- #
background_image = pygame.transform.scale2x(
    pygame.image.load('assets/img/background.png'))
background_night_img = pygame.transform.scale2x(
    pygame.image.load('assets/img/background_night.png'))
floor_img = pygame.transform.scale2x(
    pygame.image.load('assets/img/floor.png'))
obstacle_img = pygame.transform.scale2x(
    pygame.image.load('assets/img/obstacle.png'))
character_img = pygame.transform.scale2x(
    pygame.image.load('assets/img/character.png'))
game_over_img = pygame.transform.scale2x(
    pygame.image.load('assets/img/game_over.png'))
game_over_img_rect = game_over_img.get_rect(center=(220, 420))
# --------------------------------------------------------- #
win_sound = pygame.mixer.Sound('assets/sound/point.wav')
game_over_sound = pygame.mixer.Sound('assets/sound/smb_mario_die 1.wav')
# --------------------------------------------------------- #
background_img_index = 0
background = [background_image, background_night_img]

pygame.display.set_caption("PWB")
pygame.display.set_icon(character_img)


def generate_obstacle_rect():
    random_obstacle = random.randrange(300, 570)
    obstacle_rect_up = obstacle_img.get_rect(midbottom= (700, random_obstacle - 300 ))
    obstacle_rect_down = obstacle_img.get_rect(midtop= (700, random_obstacle))
    return obstacle_rect_up, obstacle_rect_down


def move_obstacle_rect(obstacles):
    for obstacle in obstacles:
        obstacle.centerx -= 5
    inside_obstacle = [obstacle for obstacle in obstacles if obstacle.right > -50]
    return inside_obstacle


def display_obstacles(obstacles):
    for obstacle in obstacles:
        if obstacle.bottom >= 600:
            main_screen.blit(obstacle_img, obstacle)
        else:
            reversed_obstacle = pygame.transform.flip(obstacle_img, False, True)
            main_screen.blit(reversed_obstacle, obstacle)


def check_collision(obstacles):
    global active_score
    for obstacle in obstacles:
        if character_img_rect.colliderect(obstacle):
            game_over_sound.play()
            time.sleep(0.5)
            active_score = True
            return False
        if character_img_rect.top <= -5 or character_img_rect.bottom >= 636:
            game_over_sound.play()
            time.sleep(0.5)
            active_score = True
            return False
    return True


def display_score(status):
    global score, high_score
    if status == 'active':
        text1 = game_font.render(str(score), False, (255, 255, 255))
        text1_rect = text1.get_rect(center=(220, 80))
        main_screen.blit(text1, text1_rect)
    if status == 'game_over':
        # SCORE
        text1 = game_font.render(f'Score : {score}', False, (60, 60, 60))
        text1_rect = text1.get_rect(center=(220, 80))
        main_screen.blit(text1, text1_rect)
        # HIGH SCORE
        text2 = game_font.render(f'HighScore : {high_score}', False, (60, 60, 60))
        text2_rect = text2.get_rect(center=(220, 130))
        main_screen.blit(text2, text2_rect)
        

def reset():
    global score
    score = 0
    return score


def update_score():
    global score, high_score, active_score
    
    if obstacle_list:
        for obstacle in obstacle_list:
            if 95 < obstacle.centerx < 105 and active_score:
                win_sound.play()
                score += 1
                active_score = False
            if obstacle.centerx < 0:
                active_score = True
    
    if score > high_score:
        high_score = score
    return high_score


def update_level():
    global score
    if score >= 30:
        clock.tick(140)
    elif score >= 20:
        clock.tick(125)
    elif score >= 10:
        clock.tick(100)
    else:
        clock.tick(85)
    

character_img_rect = character_img.get_rect(center=(100, 420))

# DISPLAY GAME
time.sleep(1.2)
main_screen = pygame.display.set_mode((display_width, display_height))

# GAME TIMER
clock = pygame.time.Clock()

# GAME LOGIC
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # END PYGAME MODULES
            pygame.quit()
            # TERMINATE PROGRAM
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or pygame.K_SPACE:
                character_movement = 0
                character_movement -= 8
            if event.key == pygame.K_KP_ENTER and game_status == False:
                reset()
                game_status = True
                obstacle_list.clear()
                character_img_rect.center = (100, 450)
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        if event.type == create_obstacle:
            obstacle_list.extend(generate_obstacle_rect())
    
    # DISPLAY SCREEN
    main_screen.blit(background[background_img_index], (0, 0))
    if score - prev_score == 10:
        background_img_index += 1
        prev_score = score
    if background_img_index >= len(background):
        background_img_index = 0
    

    if game_status:
        # DISPLAY CHARACTER IMAGE
        main_screen.blit(character_img, character_img_rect)
        # CHECK FOR COLLISIONS
        game_status = check_collision(obstacle_list)
        # OBSTACLE
        obstacle_list = move_obstacle_rect(obstacle_list)
        display_obstacles(obstacle_list)
        # FLOOR GRAVITY AND CHARACTER MOVEMENT
        character_movement += gravity
        character_img_rect.centery += character_movement
        # SHOW SCORE
        update_score()
        display_score('active')
    else:
        prev_score = 0
        background_img_index = 0
        main_screen.blit(background_image, (0, 0))
        main_screen.blit(game_over_img, game_over_img_rect)
        display_score('game_over')
        



    # DISPLAY FLOOR
    floor_x -= 1 
    main_screen.blit(floor_img, (floor_x, 630))
    main_screen.blit(floor_img, (floor_x + 448, 630))
    if floor_x <= -440:
        floor_x = 0
    
    # UPDATE SCREEN
    pygame.display.update()

    # GAME LEVEL
    update_level()


