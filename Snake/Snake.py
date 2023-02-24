import os
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import os.path
from os import path
import pygame
import time
import random
import sys
import pickle

pygame.init()

#display proportions
display_width = 800
display_height = 600


#colors
blue = (16, 142, 233)
red = (88, 24, 69)
white = (255,255,255)
black = (0,0,0)
violet = (111, 24, 215)
yellow = (231, 223, 16)
green = (9, 228, 22)
grass_green = (10, 233, 76)
apple_red = (226, 34, 104)

clock = pygame.time.Clock()

#game options
snake_color = blue
snake_head_color = yellow
food_color = apple_red
bg_color = black
text_color = white
score_color = yellow

#game variables
global highest
highest = 0
global foo
foo = ["15","0"] #0 = game_difficulity, 1 = highscore
global game_difficulity
game_difficulity = 25
global setting_game_difficulity
global snake_head



#snake options
snake_width = 20




#fonts
font_stylish = pygame.font.SysFont("comicsans", 30)
font_you_lost = pygame.font.SysFont("comicsans", 60, True)
font_score = pygame.font.SysFont("comicsans", 25)
font_pause = pygame.font.SysFont("comicsans", 30, True)
font_buttons = pygame.font.SysFont("comicsans",40, True)


#food options
food_width = 20.0

#button options
button_bg = white
button_text = black
button_width = 250
button_height = 60



#Game start

dis = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snake game')

def message(msg,color, x, y, font):
    mesg = font.render(msg,True,color)
    dis.blit(mesg, [x, y])

def the_snake(snake_width, snake_list):
    global snake_head
    for x in snake_list:
        if x == snake_head:
            pygame.draw.rect(dis, snake_head_color, [x[0], x[1], snake_width, snake_width])
        else:
            pygame.draw.rect(dis, snake_color, [x[0], x[1], snake_width, snake_width])

def game_score(score):
    value = font_score.render("Your Score: " + str(score), True, score_color)
    dis.blit(value, [0,0])

def high_score(score):
    global highest
    if score > highest:
        highest = score
        new = font_score.render( "NEW ", True, red)
        dis. blit(new, [display_width - 195, 0])
    value = font_score.render( "High Score: " + str(highest), True, score_color)
    dis. blit(value, [display_width - 150, 0])
    foo[1] = str(highest)

def save_settings():#foo ir masīvs ar detaļām, kā highscore, un settings
    f = open("savegame.txt", "w+")
    f.write(foo[0] + "\n")
    f.write(foo[1])
    f.close()

def load_settings():
    global highest
    global game_difficulity
    if os.path.exists("savegame.txt"):
        if os.path.getsize("savegame.txt") > 0:
            f=open("savegame.txt", "r",)
            f1 = f.readlines()
            if int(f1[0]) is not None:
                game_difficulity = int(f1[0])
                if game_difficulity > 65:
                    game_difficulity = 65
                elif game_difficulity < 15:
                    game_difficulity = 15
            else:
                game_difficulity = 15
            
            if int(f1[1]) is not None:
                highest = int(f1[1])
            else:
                highest = 0
        else:
            game_difficulity = 15
            highest = 0
    else:
        game_difficulity = 15
        highest = 0
    foo[0] = str(game_difficulity)
    foo[1] = str(highest)

def game_quit():
    if foo != ["0","0"] or foo != [] or foo[0] != "0":
        save_settings()
    pygame.quit()
    quit()
    

def game_diffiulity_setting():
    difficulity = setting_game_difficulity - 15
    difficulity = difficulity/5
    difficulity = int(difficulity)
    x = 0
    x_position = display_width/2 - 160
    while x <= difficulity:
        if x < 3:
           pygame.draw.rect(dis, green, [x_position, display_height/2 - 15, 30, 30])
        elif x < 6:
            pygame.draw.rect(dis, yellow, [x_position, display_height/2 - 15, 30, 30])
        else:
            pygame.draw.rect(dis, red, [x_position, display_height/2 - 15, 30, 30])
        x += 1
        x_position = x_position + 30
        pygame.display.update()

def start_window():
    dis.fill(bg_color) 
    button_x = (display_width - button_width)/2
    button_y = (display_height - button_height)/2 
    pygame.draw.rect(dis, button_bg, [button_x, button_y - (button_height * 1.3) , button_width, button_height])#button START
    message("START", button_text, button_x + button_width/2 -70 , button_y - (button_height * 1.3), font_buttons)
    pygame.draw.rect(dis, button_bg, [button_x, button_y , button_width, button_height])#button SETTINGS
    message("SETTINGS", button_text, button_x + button_width/2 - 105, button_y , font_buttons)
    pygame.draw.rect(dis, button_bg, [button_x, button_y + (button_height * 1.3), button_width, button_height])#button EXIT
    message("EXIT", button_text, button_x + button_width/2 - 50, button_y + (button_height * 1.3), font_buttons)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    position = pygame.mouse.get_pos()
                    if position[0]> button_x and position[0] < button_x + button_width:
                        if position[1] > button_y - (button_height * 1.3) and position[1] < button_y - (button_height * 1.3) + button_height:
                            game_replay()
                        elif position[1] > button_y and position[1] < button_y + button_height:
                            open_settings()
                        elif position[1] > button_y + (button_height * 1.3) and position[1] < button_y + (button_height * 1.3) + button_height:
                            game_quit()
                elif event.type == pygame.QUIT:
                    game_quit()
def setting_window():
    dis.fill(bg_color)
    button_x = display_width/2
    button_y = display_height - button_height - 10
    message("Settings",text_color,0,0,font_stylish)

    #pygame.draw.rect(dis, button_bg, [1,1,74,24])#Mēru burtu izmēru Vārdam ar 1u lielo un 4iem mazajie, 1 lielais = 20, 3 mazie = 54, katrs 9i 
    #message("Back", button_text, 1,1, font_buttons)
    
    pygame.draw.rect(dis, button_bg, [button_x - button_width - 10 , button_y , button_width, button_height])#button Back
    message("Back", button_text, (button_x  - button_width - 10) + button_width/2 - 37 , button_y, font_buttons)
    
    pygame.draw.rect(dis, button_bg, [button_x + 10 , button_y , button_width, button_height])#button Save
    message("Save", button_text, (button_x + 10) + button_width/2 - 37, button_y, font_buttons)
    
   # pygame.draw.rect(dis, white, [display_width/2 - 150, display_height/2 - 15, 300, 30])
    
    pygame.draw.rect(dis, white, [display_width/2 - 190, display_height/2 -15, 30, 30])
    message("-", black, display_width/2 - 188, display_height/2 -33, font_buttons)
    
    pygame.draw.rect(dis, white, [display_width/2 + 160, display_height/2 -15, 30, 30])
    message("+", black, display_width/2 + 162, display_height/2 -33, font_buttons)
    #pygame.draw.rect(dis, red, [display_width/2, 0, 2, display_height]) #veido krustu uz ekrāna, lai regulētu ekrāna izvietojumu 
    #pygame.draw.rect(dis, red, [0, display_height/2, display_width, 2])

def open_settings():
    global setting_game_difficulity
    global game_difficulity
    setting_game_difficulity =  game_difficulity 
    button_x = display_width/2
    button_y = display_height - button_height - 10

    setting_window()
    game_diffiulity_setting()

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                position = pygame.mouse.get_pos()
                if position[1]> button_y and position[1] < button_y + button_height:
                    if position[0] > button_x - button_width - 10 and position[0] < button_x - 10:#Back
                        start_window()
                    elif position[0] > button_x  + 10 and position[0] < button_x + button_width + 10:#Save
                        game_difficulity = setting_game_difficulity
                        foo[0] = str(game_difficulity)
                        start_window()
                elif position[1]> display_height/2 -25 and position[1] < display_height/2 + 13:
                    if position[0] > display_width/2 -190 and position[0] < display_width/2 -160:
                        if setting_game_difficulity > 15:
                            setting_game_difficulity -= 5
                            setting_window()
                            game_diffiulity_setting()
                    elif position[0] > display_width/2 + 160 and position[0] < display_width/2 + 190:
                        if setting_game_difficulity < 65:
                            setting_game_difficulity += 5
                            game_diffiulity_setting()

            elif event.type == pygame.QUIT:
                game_quit()
   
    

def game_replay():
    snake_speed = int(game_difficulity)

    global snake_head
    game_over = False
    game_close = False
    game_over_screen = True
   
    x1 = display_width/2
    y1 = display_height/2

    x1_change = 0
    y1_change = 0

    snake_list = []
    paused_snake_list = []
    snake_lenght = 1
    paused = False
    foodx = round(random.randrange(0, display_width - snake_width)/food_width)*food_width
    foody = round(random.randrange(0, display_height - snake_width)/food_width)*food_width



    while not game_close:

        while game_over:
            if game_over_screen:
                dis.fill(bg_color)  
                message("You Lost!", text_color,300, 150, font_you_lost)
                game_score(snake_lenght-1)
                high_score(snake_lenght-1)
                message("Q - Quit", text_color,325, 210, font_stylish)
                message("R - Restart", text_color,325, 240, font_stylish)
                message("P - Pause", text_color,325, 270, font_stylish)
                message("B - Back to Main Menu", text_color,325, 300, font_stylish)
                #pygame.draw.rect(dis, red, [display_width - 150, 0, 2, display_height]) # H veido krustu uz ekrāna, lai regulētu ekrāna izvietojumu 
                #pygame.draw.rect(dis, red, [0, display_height/2, display_width, 2]) # W
                pygame.display.update()
                game_over_screen = False
                

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_close = True
                        game_over = False
                    if event.key == pygame.K_r:
                        game_replay()
                    if event.key == pygame.K_b:
                        start_window()
                elif event.type == pygame.QUIT:
                    game_close = True
                    game_over = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True
                game_over = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_width
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_width
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -snake_width
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = snake_width
                elif event.key == pygame.K_p:
                    paused_snake_list = snake_list
                    paused = True
                   
        if x1 >= display_width or x1 <= 0 or y1 >= display_height or y1 <= 0:
            game_over = True            
        x1 += x1_change
        y1 += y1_change
        dis.fill(bg_color)        
        pygame.draw.rect(dis, food_color ,[foodx, foody, food_width, food_width])
        
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list)>snake_lenght:
            del snake_list[0]

        
        for x in snake_list[:-1]:
            if x == snake_head:
                game_over = True

        the_snake(snake_width, snake_list)
        game_score(snake_lenght-1)

        pygame.display.update()

        if (x1 == foodx and y1 == foody) or (x1 + 5 == foodx and y1 + 5 == foody) or (x1 - 5 == foodx and y1 - 5 == foody):
            foodx = round(random.randrange(0, display_width - snake_width)/food_width)*food_width
            foody = round(random.randrange(0, display_height - snake_width)/food_width)*food_width
            snake_lenght += 1
        while paused:
            message("PAUSED", red, 130, 0, font_pause)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False    
                        snake_list = paused_snake_list
        clock.tick(snake_speed)
    
    game_quit()
#Beidzas funkciju definēšana un sākas izvadey
load_settings()
start_window()
game_replay()
