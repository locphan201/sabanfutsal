import pygame
from color import *
from ball import Ball
from player import Player
from fps import *

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
info = [ball.pos()]
for player in players_1:
    info.append(player)
for player in players_2:
    info.append(player)
steps.append(info)
current_step = 0

clock = pygame.time.Clock()
running = True

def draw_players():
    info = steps[current_step]
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
    pygame.draw.circle(screen, BLACK, ball.pos(), 10)
    pygame.draw.circle(screen, BALL_COLOR, ball.pos(), 8)

def move_object(x, y):
    if object_clicked == False:
        return
    
    if object_num == 0:
        ball.move(x, y)
        return
    
    if object_num <= 5:
        players_1[object_num-1].move(x, y)
    else:
        players_2[object_num-6].move(x, y)

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

while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    clock.tick(fps)
    
    draw_basic_UI()
    step_index()
    draw_reset_button()
    draw_players()
    draw_ball()
    move_object(mouse_x, mouse_y)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if object_clicked == False:
                x, y = mouse_x, mouse_y
                dis = (x-ball.pos()[0])**2 + (y-ball.pos()[1])**2
                if dis <= 100:
                    object_clicked = True
                    object_num = 0
                for player in players_1:
                    dis = (x-player.pos()[0])**2 + (y-player.pos()[1])**2
                    if dis <= 225:
                        object_clicked = True
                        object_num = player.shirt_num()
                for player in players_2:
                    dis = (x-player.pos()[0])**2 + (y-player.pos()[1])**2
                    if dis <= 225:
                        object_clicked = True
                        object_num = player.shirt_num() + 5
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
                new_info = [ball.pos()]
                for i in range(5):
                    new_info.append(players_1[i])
                for i in range(5):
                    new_info.append(players_2[i])
                steps = [new_info]
                current_step = 0
                    
    pygame.display.flip()
    