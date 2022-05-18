# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018

@author: zou
"""
from email.mime import image
import numpy as np
import pygame
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT

from game import Game

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
green = pygame.Color(0, 200, 0)
bright_green = pygame.Color(0, 255, 0)
red = pygame.Color(200, 0, 0)
bright_red = pygame.Color(255, 0, 0)
blue = pygame.Color(32, 178, 170)
bright_blue = pygame.Color(32, 200, 200)
yellow = pygame.Color(255, 205, 0)
bright_yellow = pygame.Color(255, 255, 0)
image1=pygame.image.load('./images/forest.jpg')
count1=0
game = Game()
rect_len = game.settings.rect_len
snake = game.snake
pygame.init()
fpsClock = pygame.time.Clock()
#Change 1
screen = pygame.display.set_mode((game.settings.width * 30, game.settings.height * 30))
pygame.display.set_caption('GLUTTONOUS')
#change
home_sound = pygame.mixer.Sound('./sound/homesound.mp3')
crash_sound = pygame.mixer.Sound('./sound/crash.wav')
game_sound = pygame.mixer.Sound('./sound/gametune.mp3')
eating_sound = pygame.mixer.Sound('./sound/eating.mp3')


def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, x, y, color,font_size):
    large_text = pygame.font.SysFont('Corbel', font_size)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()


def button(msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            if parameter != None:
                action(parameter)
            else:
                action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    smallText = pygame.font.SysFont('Corbel', 30)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect)


def quitgame():
    pygame.quit()
    quit()      

#change 
def crash():
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.Sound.stop(game_sound)
    message_display('GAME OVER !', game.settings.width / 2 * 30, game.settings.height / 3 * 30, black ,50)
    message_display(f'Your Score: {game.snake.score}', game.settings.width / 2 * 30, game.settings.height / 3 * 45, black, 50)
    time.sleep(3)
    pygame.mixer.Sound.play(home_sound)

def how_to_play():
    screen.fill(black)
    global count1
    count1=1

    message_display('The game is Simple:', game.settings.width / 2 *30, game.settings.height / 3 * 15, white, 20)
    message_display('Moving the Snake: Move the Snake with the arrow keys on the keyboard', game.settings.width / 2 * 30, game.settings.height / 3 * 25, white, 20)
    message_display('What to do?: Try to feed the snake as much food as possible, the snake will keep on increasing in length', game.settings.width / 2 * 30, game.settings.height / 3 * 35, white, 20)
    message_display('GOAL: Keep going as long as possible and avoid hitting the walls or the snake itself', game.settings.width / 2 * 30, game.settings.height / 3 * 45, white, 20)
    message_display('ALL THE BEST !!!', game.settings.width / 2 * 30, game.settings.height / 3 * 55, white, 40)
    time.sleep(5)
    
    initial_interface()

    

def initial_interface():
    intro = True
    screen.fill(black)
    if count1==0:
        pygame.mixer.Sound.play(home_sound)
    else:
        pass
    while intro:
        

        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                pygame.quit()

        
        #change
        message_display('GLUTTONOUS', game.settings.width / 2 * 30, game.settings.height / 4 * 30, white, 50)

        #change
        button('Start Game !', 160, 480, 180, 80, blue, bright_blue, game_loop, 'human')
        button('Leave Game !', 540, 480, 180, 80, red, bright_red, quitgame)

        button('How to Play?', 335, 625, 200, 80, yellow, bright_yellow, how_to_play)

        pygame.display.update()
        pygame.time.Clock().tick(15)


def game_loop(player, fps=5):
    #change : fps intitally set to 5
    game.restart_game()
    pygame.mixer.Sound.stop(home_sound)
    pygame.mixer.Sound.play(game_sound)
    

    while not game.game_end():
        


        pygame.event.pump()

        move = human_move()

        game.do_move(move)
        #screen.blit(image1, (0, 0))

        screen.fill(yellow)

        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(black, screen)

        pygame.display.flip()

        fpsClock.tick(fps)

    crash()
    initial_interface()


def human_move():
    direction = snake.facing

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        elif event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == ord('d'):
                direction = 'right'
            if event.key == K_LEFT or event.key == ord('a'):
                direction = 'left'
            if event.key == K_UP or event.key == ord('w'):
                direction = 'up'
            if event.key == K_DOWN or event.key == ord('s'):
                direction = 'down'
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    move = game.direction_to_int(direction)
    return move


if __name__ == "__main__":
    initial_interface()
