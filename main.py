import pygame
from color import *
from ball import Ball
from player import Player
from fps import *
from copy import deepcopy

pygame.init()
pygame.display.set_caption('Sa bàn Futsal')
icon = pygame.image.load('Images\\icon.png')
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((750, 700))
shirt_font = pygame.font.SysFont('Arial', 20)
text_font = pygame.font.SysFont('Arial', 20)

# Pitch
pitch_img = pygame.image.load('Images\\pitch.png')
pitch_img = pygame.transform.rotate(pitch_img, 90)
img_width = pitch_img.get_width()
img_height = pitch_img.get_height()
height = 700
width = img_width*img_height/height
pitch_img = pygame.transform.scale(pitch_img, (width, height))
img_rect = pygame.Rect(0, 0, width, height)

# Click
object_clicked = False
object_num = -1

# Players team 1
players_1 = []
for i in range(5):
    players_1.append(Player(625, 40+50*i, i+1))

# Player team 2
players_2 = []
for i in range(5):
    players_2.append(Player(700, 40+50*i, i+1))

# Ball
ball = Ball(625, 290)

# Run Button
run_rect = pygame.Rect(600, 10, 100, 50)
run = False

# Subs Rect
subs_rect = pygame.Rect(width, 0, 760-width, 340)

# Reset button
reset_rect = pygame.Rect(width+40, 350, 100, 50)

# Step
steps = []
info = [ball]
for player in players_1:
    info.append(player)
for player in players_2:
    info.append(player)
steps.append(info)
current_step = 0

# Speed control
ball_speed = 0
player_speed = 0

# Next step button
previous_step_rect = pygame.Rect(width+10, 425, 75, 50)
next_step_rect = pygame.Rect(width+100, 425, 75, 50)
next_clicked = False

clock = pygame.time.Clock()
running = True

def draw_players():
    global next_clicked, player_speed, ball_speed
    info = steps[current_step]
    if next_clicked:
        player_speed += 1
        last_info = steps[current_step-1]
        for i in range(1, 6):
            pos = info[i].pos()
            last_pos = last_info[i].pos()
            x = last_pos[0]+(pos[0]-last_pos[0])/speed*ball_speed
            y = last_pos[1]+(pos[1]-last_pos[1])/speed*ball_speed
            pygame.draw.circle(screen, BLACK, (x, y), 15)
            if i == 1:
                pygame.draw.circle(screen, GRASS, (x, y), 13)
            else:
                pygame.draw.circle(screen, TEAM_1, (x, y), 13)
            screen.blit(shirt_font.render(str(info[i].shirt_num()), True, WHITE), (x-5, y-12))
        for i in range(6, 11):    
            pos = info[i].pos()
            last_pos = last_info[i].pos()
            x = last_pos[0]+(pos[0]-last_pos[0])/speed*ball_speed
            y = last_pos[1]+(pos[1]-last_pos[1])/speed*ball_speed
            pygame.draw.circle(screen, BLACK, (x, y), 15)
            if i == 6:
                pygame.draw.circle(screen, PURPLE, (x, y), 13)
            else:
                pygame.draw.circle(screen, TEAM_2, (x, y), 13)
            screen.blit(shirt_font.render(str(info[i].shirt_num()), True, WHITE), (x-5, y-12))
        if player_speed == speed:
            player_speed = 0
            ball_speed = 0
            next_clicked = False
      
    else:
        for i in range(1, 6):
            pygame.draw.circle(screen, BLACK, info[i].pos(), 15)
            if i == 1:
                pygame.draw.circle(screen, GRASS, info[i].pos(), 13)
            else:
                pygame.draw.circle(screen, TEAM_1, info[i].pos(), 13)
            screen.blit(shirt_font.render(str(info[i].shirt_num()), True, WHITE), (info[i].pos()[0]-5, info[i].pos()[1]-12))
    
        for i in range(6, 11):
            pygame.draw.circle(screen, BLACK, info[i].pos(), 15)
            if i == 6:
                pygame.draw.circle(screen, PURPLE, info[i].pos(), 13)
            else:
                pygame.draw.circle(screen, TEAM_2, info[i].pos(), 13)
            screen.blit(shirt_font.render(str(info[i].shirt_num()), True, WHITE), (info[i].pos()[0]-5, info[i].pos()[1]-12))
        
def draw_ball():
    global next_clicked, ball_speed
    pos = steps[current_step][0].pos()
    if next_clicked:
        ball_speed += 1
        last_pos = steps[current_step-1][0].pos()
        x = last_pos[0]+(pos[0]-last_pos[0])/speed*ball_speed
        y = last_pos[1]+(pos[1]-last_pos[1])/speed*ball_speed
        pygame.draw.circle(screen, BLACK, (x, y), 10)
        pygame.draw.circle(screen, BALL_COLOR, (x, y), 8)
    else:
        pygame.draw.circle(screen, BLACK, pos, 10)
        pygame.draw.circle(screen, BALL_COLOR, pos, 8)

def move_object(x, y):
    if object_clicked == False:
        return
    
    info = steps[current_step]
    
    if object_num == 0:
        info[0].move(x, y)
        return
    
    if object_num <= 5:
        info[object_num].move(x, y)
    else:
        info[object_num].move(x, y)

def draw_basic_UI():
    screen.fill(GRASS)
    screen.blit(pitch_img, (0, 0))
    pygame.draw.rect(screen, BLACK, (0, 0, width, height), 2)
    pygame.draw.rect(screen, LIGHT_YELLOW, subs_rect)
    
def draw_reset_button():
    pygame.draw.rect(screen, WHITE, reset_rect)
    pygame.draw.rect(screen, BLACK, reset_rect, 2)
    screen.blit(text_font.render('Reset', True, BLACK), (reset_rect.x+20, reset_rect.y+10))

def step_index():
    length = len(steps)
    screen.blit(text_font.render(str(current_step+1)+'/'+str(length), True, BLACK), (700, 300))

def draw_all_steps_button():
    pygame.draw.rect(screen, WHITE, previous_step_rect)
    pygame.draw.rect(screen, BLACK, previous_step_rect, 2)
    screen.blit(text_font.render('Previous', True, BLACK), (previous_step_rect.x+5, previous_step_rect.y+10))
    
    pygame.draw.rect(screen, WHITE, next_step_rect)
    pygame.draw.rect(screen, BLACK, next_step_rect, 2)
    screen.blit(text_font.render('Next', True, BLACK), (next_step_rect.x+20, next_step_rect.y+10))

while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    clock.tick(fps)
    
    draw_basic_UI()
    step_index()
    draw_reset_button()
    draw_all_steps_button()
    draw_players()
    draw_ball()
    move_object(mouse_x, mouse_y)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if object_clicked == False:
                x, y = mouse_x, mouse_y
                info = steps[current_step]
                dis = (x-info[0].pos()[0])**2 + (y-info[0].pos()[1])**2
                if dis <= 100:
                    object_clicked = True
                    object_num = 0
                for i in range(1, 6):
                    dis = (x-info[i].pos()[0])**2 + (y-info[i].pos()[1])**2
                    if dis <= 225:
                        object_clicked = True
                        object_num = info[i].shirt_num()
                for i in range(6, 11):
                    dis = (x-info[i].pos()[0])**2 + (y-info[i].pos()[1])**2
                    if dis <= 225:
                        object_clicked = True
                        object_num = info[i].shirt_num() + 5
            else:
                if object_clicked:
                    if subs_rect.collidepoint(mouse_x, mouse_y) or img_rect.collidepoint(mouse_x, mouse_y):
                        object_clicked = False
                        
            if reset_rect.collidepoint(mouse_x, mouse_y):
                object_clicked = False
                steps.clear()
                players_1.clear()
                players_2.clear()
                for i in range(5):
                    players_1.append(Player(625, 40+50*i, i+1))
                    players_2.append(Player(700, 40+50*i, i+1))
                ball = Ball(625, 290)
                new_info = [ball]
                for i in range(5):
                    new_info.append(players_1[i])
                for i in range(5):
                    new_info.append(players_2[i])
                steps = [new_info]
                current_step = 0
            
            if previous_step_rect.collidepoint(mouse_x, mouse_y):
                if current_step > 0:
                    current_step -= 1
            
            if next_step_rect.collidepoint(mouse_x, mouse_y):
                if current_step < len(steps)-1:
                    current_step += 1
                    next_clicked = True
                else:
                    temp = deepcopy(steps[current_step])
                    steps.insert(current_step, temp)
                    current_step += 1
            
    pygame.display.flip()
    