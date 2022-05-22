# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 15:19:25 2018

@author: zou
"""
import pygame
import random
import numpy as np

#Class for the settings of the game 
class Settings:
    def __init__(self):
        self.width = 28
        self.height = 28
        #Change 1: rectangular length of game is changed so that it is bigger 
        self.rect_len = 30

#Class for snake 
class Snake:
    #Constructor snake, assigns image for each head, tail  and body, sets reward as 0 
    def __init__(self):
        self.image_up = pygame.image.load('images/head_up.bmp')
        self.image_down = pygame.image.load('images/head_down.bmp')
        self.image_left = pygame.image.load('images/head_left.bmp')
        self.image_right = pygame.image.load('images/head_right.bmp')
        

        self.tail_up = pygame.image.load('images/tail_up.bmp')
        self.tail_down = pygame.image.load('images/tail_down.bmp')
        self.tail_left = pygame.image.load('images/tail_left.bmp')
        self.tail_right = pygame.image.load('images/tail_right.bmp')
            
        self.image_body = pygame.image.load('images/body.bmp')
     
        self.facing = "right"
        self.initialize()
    #Function sets up the snake at the start of the game
    def initialize(self):
        self.position = [15,15]
        self.segments = [[6 - i, 6] for i in range(3)]
        self.score = 0
        self.reward = 0 
    #function describes how the body image will show on the surface
    def blit_body(self, x, y, screen):
        screen.blit(self.image_body, (x, y))
    #function describes how the head image will show on the surface depending on the facing    
    def blit_head(self, x, y, screen):
        if self.facing == "up":
            screen.blit(self.image_up, (x, y))
        elif self.facing == "down":
            screen.blit(self.image_down, (x, y))  
        elif self.facing == "left":
            screen.blit(self.image_left, (x, y))  
        else:
            screen.blit(self.image_right, (x, y))  
     #function describes how the tail image will show on the surface         
    def blit_tail(self, x, y, screen):
        tail_direction = [self.segments[-2][i] - self.segments[-1][i] for i in range(2)]
        
        if tail_direction == [0, -1]:
            screen.blit(self.tail_up, (x, y))
        elif tail_direction == [0, 1]:
            screen.blit(self.tail_down, (x, y))  
        elif tail_direction == [-1, 0]:
            screen.blit(self.tail_left, (x, y))  
        else:
            screen.blit(self.tail_right, (x, y))  
    #shows the image on the surface
    def blit(self, rect_len, screen):
        self.blit_head(self.segments[0][0]*rect_len, self.segments[0][1]*rect_len, screen)                
        for position in self.segments[1:-1]:
            self.blit_body(position[0]*rect_len, position[1]*rect_len, screen)
        self.blit_tail(self.segments[-1][0]*rect_len, self.segments[-1][1]*rect_len, screen)                
            
    #Function changes the snake's facing depending on the user's keystroke
    def update(self):
        if self.facing == 'right':
            self.position[0] += 1
        if self.facing == 'left':
            self.position[0] -= 1
        if self.facing == 'up':
            self.position[1] -= 1
        if self.facing == 'down':
            self.position[1] += 1
        self.segments.insert(0, list(self.position))

 #Class for the strawberry(berry)       
class Strawberry():
    #constructor sets image for berry 
    def __init__(self, settings):
        self.settings = settings
        
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load('images/food' + str(self.style) + '.bmp')        
        self.initialize()
    #Function sets the position of the berry    
    def random_pos(self, snake):
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load('images/food' + str(self.style) + '.bmp')                
        
        self.position[0] = random.randint(0, self.settings.width-1)
        self.position[1] = random.randint(0, self.settings.height-1)

        self.position[0] = random.randint(9, 19)
        self.position[1] = random.randint(9, 19)
        
        if self.position in snake.segments:
            self.random_pos(snake)
    #fucntion shows the berry on the surface 
    def blit(self, screen):
        screen.blit(self.image, [p * self.settings.rect_len for p in self.position])
   
    def initialize(self):
        self.position = [15, 15]
      
#class for the game         
class Game:
    """
    """
    #constructor sets the snake, setting and strawberry and dict of what keystrokes mean
    def __init__(self):
        self.settings = Settings()
        self.snake = Snake()
        
        self.strawberry = Strawberry(self.settings)
        self.move_dict = {0 : 'up',
                          1 : 'down',
                          2 : 'left',
                          3 : 'right'}       
    #Function  re-initialize snake and strawberry when called    
    def restart_game(self):
        self.snake.initialize()
        self.strawberry.initialize()
    
    def current_state(self):  
        #this function is not called or used in main.py or game.py so no changes were made
        state = np.zeros((self.settings.width+2, self.settings.height+2, 2))
        expand = [[0, 1], [0, -1], [-1, 0], [1, 0], [0, 2], [0, -2], [-2, 0], [2, 0]]
        
        for position in self.snake.segments:
            state[position[1], position[0], 0] = 1
        
        state[:, :, 1] = -0.5        

        state[self.strawberry.position[1], self.strawberry.position[0], 1] = 0.5
        for d in expand:
            state[self.strawberry.position[1]+d[0], self.strawberry.position[0]+d[1], 1] = 0.5
        return state
        
    #converts the key stroke to direction which can be found in move_dict
    def direction_to_int(self, direction):
        direction_dict = {value : key for key,value in self.move_dict.items()}
        return direction_dict[direction]
      
    def do_move(self, move):
        eating_sound = pygame.mixer.Sound('./sound/eating.wav')
        move_dict = self.move_dict
        
        change_direction = move_dict[move]
        
        if change_direction == 'right' and not self.snake.facing == 'left':
            self.snake.facing = change_direction
        if change_direction == 'left' and not self.snake.facing == 'right':
            self.snake.facing = change_direction
        if change_direction == 'up' and not self.snake.facing == 'down':
            self.snake.facing = change_direction
        if change_direction == 'down' and not self.snake.facing == 'up':
            self.snake.facing = change_direction

        self.snake.update()
        
        if self.snake.position == self.strawberry.position:
            self.strawberry.random_pos(self.snake)
            pygame.mixer.Sound.play(eating_sound)
            reward = random.randint(2,4)
            #Change 2: increase the score by 10 instead of 1
            self.snake.score += 10
            #Change 3: Give bonus points, 2 and 5, for every 10th berry eaten by the snake
            true_score = self.snake.score - self.snake.reward
            if true_score % 100 == 0:
                self.snake.score +=  reward
                self.snake.reward += reward

        else:
            self.snake.segments.pop()
            reward = 0
                
        if self.game_end():
            return -1
                    
        return reward
    
    def game_end(self):
        end = False
        if self.snake.position[0] >= self.settings.width or self.snake.position[0] < 0:
            end = True
        if self.snake.position[1] >= self.settings.height or self.snake.position[1] < 0:
            end = True
        if self.snake.segments[0] in self.snake.segments[1:]:
            end = True

        return end
    
    def blit_score(self, color, screen):
        #change 4: Font of the score is the same as the rest of the game
        font = pygame.font.SysFont("Corbel", 25)
        text = font.render('Score: ' + str(self.snake.score), True, color)
        #change 5: Position of the score is moved from the left of the screen to the centre
        screen.blit(text, (400, 10))


