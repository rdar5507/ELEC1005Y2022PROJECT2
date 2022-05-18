# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018

@author: zou
"""
# All the necessary Modules have been added here

from email.mime import image
import numpy as np
import pygame
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT

#The second code required to run the game has been imported here

from game import Game

#All the colors and the sounds have been initialised here as Global variables so that they can be accessed anywhere

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
#Change 10- Added Images to the initial Page
image1 = pygame.image.load('./images/snake1.jpg')
image2 = pygame.image.load('./images/snake2.jpg')
count1=0
game = Game()
rect_len = game.settings.rect_len
snake = game.snake
pygame.init()
fpsClock = pygame.time.Clock()
#Change 1 - Changed the Dimensions of the Screen.
screen = pygame.display.set_mode((game.settings.width * 30, game.settings.height * 30))
pygame.display.set_caption('GLUTTONOUS')
#Change 2 - Added various sounds for more fun and user participation
home_sound = pygame.mixer.Sound('./sound/homesound.mp3')
crash_sound = pygame.mixer.Sound('./sound/crash.wav')
game_sound = pygame.mixer.Sound('./sound/gametune.mp3')
eating_sound = pygame.mixer.Sound('./sound/eating.mp3')
sad_sound = pygame.mixer.Sound('./sound/sadsound.mp3')

# Text Rendering Function

def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


# Message Display Function 

def message_display(text, x, y, color,font_size):
    #Change 3 - Changed all font styles to Corbel as it looks better
    large_text = pygame.font.SysFont('Corbel', font_size)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()

# Message that renders the buttons on the screen

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

# Initialises the quiting procedure

def quitgame():
    pygame.quit()
    quit()

# This Function mentions what happens when the snake Crashes

def crash():
    #Change 4 - Added new Sounds and stopped the gameplay sound to make it more fun
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.Sound.stop(game_sound)
    pygame.mixer.Sound.play(sad_sound)
    #Change 5 - Changed the crash page and displayed the score as well with the Crash Message.
    screen.fill(black)
    message_display('GAME OVER :(', game.settings.width / 2 * 30, game.settings.height / 3 * 30, white ,50)
    message_display(f'Your Score: {game.snake.score}', game.settings.width / 2 * 30, game.settings.height / 3 * 45, white, 50)
    time.sleep(3)
    pygame.mixer.Sound.play(home_sound)

# This Function is for the How TO play manual
#Change 6 - Made a whole new fucntion to display the manual to the game 
#The message stays on for 5 seconds and automatically goes off.
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

# This function sets up the initial home page

def initial_interface():
    intro = True
    screen.fill(white)
    #Added Images
    screen.blit(image1,(0,0))
    screen.blit(image2,(game.settings.width / 2 * 27, game.settings.height / 4 * 30))
    # Did this so that if this function is called again the music should not be played again and again 
    if count1==0:
        pygame.mixer.Sound.play(home_sound)
    else:
        pass
    while intro:
        

        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                pygame.quit()

        
        #Change 7- Changed the message according to the screen size and also incresed the font size and changed color.
        #Also added a new Message 
        message_display('GLUTTONOUS', game.settings.width / 2 * 30, game.settings.height / 4 * 30, black, 70)
        message_display('The Snake Game', game.settings.width / 2 * 30, game.settings.height / 4 * 45, black, 25)

        # Change 8- Changed the buttons a little bit and also added a new button to see the manual of the game
        button('Start Game !', 160, 480, 180, 80, blue, bright_blue, game_loop, 'human')
        button('Leave Game !', 540, 480, 180, 80, red, bright_red, quitgame)
        button('How to Play?', 335, 625, 200, 80, yellow, bright_yellow, how_to_play)

        pygame.display.update()
        pygame.time.Clock().tick(15)

# Loop and Functions running the game are in the function below

def game_loop(player, fps = 5):
    # Changing the Music when the screen changes
    game.restart_game()
    pygame.mixer.Sound.stop(home_sound)
    pygame.mixer.Sound.play(game_sound)
    # Chnage 9 - The Fps of the game increases with the increase of the score making it harder and harder.
    while not game.game_end():
        if game.snake.score >= 50 and game.snake.score < 100:
            fps=7
        elif game.snake.score >= 100 and game.snake.score < 150:
            fps = 9
        elif game.snake.score >= 150 and game.snake.score < 200:
            fps = 10
        elif game.snake.score >= 200 and game.snake.score < 250:
            fps = 15
        elif game.snake.score >= 250:
            fps = 20
        pygame.event.pump()

        move = human_move()
        #change
        

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

#This Function sets up the Movement criterias

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
