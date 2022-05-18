# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 15:19:25 2018

@author: zou
"""
import pygame, random
import numpy as np
 
class Settings:
    def __init__(self):
        #the width and height of the game has been set 
        self.width = 28
        self.height = 28
        #Change length of screen from 15 to 30
        self.rect_len = 30

class Snake:
    def __init__(self):
        #images related to snake's body part has loaded 
        self.image_up = pygame.image.load('images/head_up.bmp')
        self.image_down = pygame.image.load('images/head_down.bmp')
        self.image_left = pygame.image.load('images/head_left.bmp')
        self.image_right = pygame.image.load('images/head_right.bmp')

        self.tail_up = pygame.image.load('images/tail_up.bmp')
        self.tail_down = pygame.image.load('images/tail_down.bmp')
        self.tail_left = pygame.image.load('images/tail_left.bmp')
        self.tail_right = pygame.image.load('images/tail_right.bmp')
            
        self.image_body = pygame.image.load('images/body.bmp')
        # the game starts with snake facing right
        self.reward = 0
        self.facing = "right"
        self.initialize()

    def initialize(self):
    #sets position of snake during the start of the game 
        self.position = [15,15]
        self.segments = [[6 - i, 6] for i in range(3)]
        self.score = 0
        self.reward = 0
    #defines how each part of the snake's body is displayed
    def blit_body(self, x, y, screen):
        screen.blit(self.image_body, (x, y))
        
    def blit_head(self, x, y, screen):
        if self.facing == "up":
            screen.blit(self.image_up, (x, y))
        elif self.facing == "down":
            screen.blit(self.image_down, (x, y))  
        elif self.facing == "left":
            screen.blit(self.image_left, (x, y))  
        else:
            screen.blit(self.image_right, (x, y))  
            
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
    def blit(self, rect_len, screen):
        #displays the snake on screen 
        self.blit_head(self.segments[0][0]*rect_len, self.segments[0][1]*rect_len, screen)                
        for position in self.segments[1:-1]:
            self.blit_body(position[0]*rect_len, position[1]*rect_len, screen)
        self.blit_tail(self.segments[-1][0]*rect_len, self.segments[-1][1]*rect_len, screen)                
            
    
    def update(self):
        #changes position of snake depending on the facing  
        if self.facing == 'right':
            self.position[0] += 1
        if self.facing == 'left':
            self.position[0] -= 1
        if self.facing == 'up':
            self.position[1] -= 1
        if self.facing == 'down':
            self.position[1] += 1
        self.segments.insert(0, list(self.position))
        
class Strawberry():
    def __init__(self, settings):
        #declare all attributes of class
        self.settings = settings 
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load('images/food' + str(self.style) + '.bmp')        
        self.initialize()
       
    def random_pos(self, snake):
        #random position of berry is found and assigned  
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load('images/food' + str(self.style) + '.bmp')                
        
        self.position[0] = random.randint(0, self.settings.width-1)
        self.position[1] = random.randint(0, self.settings.height-1)

        self.position[0] = random.randint(9, 19)
        self.position[1] = random.randint(9, 19)
        
        if self.position in snake.segments:
            self.random_pos(snake)
    
    def blit(self, screen):
        #shows the berry on the screen
        screen.blit(self.image, [p * self.settings.rect_len for p in self.position])
   
    def initialize(self):
        self.position = [15, 15]
      
        
class Game:
    def __init__(self):
        #sets the game attributes 
        self.settings = Settings()
        self.snake = Snake()
        self.strawberry = Strawberry(self.settings)
        self.move_dict = {0 : 'up',
                          1 : 'down',
                          2 : 'left',
                          3 : 'right'}       
        
    def restart_game(self):
        #if game is restared the snake and strawberry classes are reset
        self.snake.initialize()
        self.strawberry.initialize()

    def current_state(self):
        #
        state = np.zeros((self.settings.width+2, self.settings.height+2, 2))
        expand = [[0, 1], [0, -1], [-1, 0], [1, 0], [0, 2], [0, -2], [-2, 0], [2, 0]]
        
        for position in self.snake.segments:
            state[position[1], position[0], 0] = 1
        
        state[:, :, 1] = -0.5        

        state[self.strawberry.position[1], self.strawberry.position[0], 1] = 0.5
        for d in expand:
            state[self.strawberry.position[1]+d[0], self.strawberry.position[0]+d[1], 1] = 0.5
        return state
    
    def direction_to_int(self, direction):
        #changes key values to element in self.move_dict dictionary 
        direction_dict = {value : key for key,value in self.move_dict.items()}
        return direction_dict[direction]
        
    def do_move(self, move):
        #schanges facing of snake based on the direction the user has inputed
        eating_sound = pygame.mixer.Sound('./sound/eating.mp3')
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
        
        if self.snake.position == self.strawberry.position and self.strawberry.image!="images/food4.bmp":
            pygame.mixer.Sound.play(eating_sound)
            self.strawberry.random_pos(self.snake)
            reward = random.randint(2,4)
            #Change 2: the score is set to increase by 10 each time the snake eats the berry
            self.snake.score += 10
            #change 3: reward is set to random integer between 2 and 5
            #        : adds reward to snake score if the true score is multiple of 100(or 10 berries are)
            true_score = self.snake.score - self.snake.reward
            if true_score % 100 == 0: 
                self.snake.score += reward
                self.snake.reward += reward 
        else:

            self.snake.segments.pop()
            reward = 0
                
        if self.game_end():
            return -1
                    
        return reward
    
    def game_end(self):
        #conditions for the game to end and returns end value which changes if any of the conditions are met
        end = False
        if self.snake.position[0] >= self.settings.width or self.snake.position[0] < 0:
            end = True
        if self.snake.position[1] >= self.settings.height or self.snake.position[1] < 0:
            end = True
        if self.snake.segments[0] in self.snake.segments[1:]:
            end = True

        return end
    
    def blit_score(self, color, screen):
        #shows the score(text) on the screen with the corbel font and 25 size.
        font = pygame.font.SysFont("Corbel", 25)
        #change 4: the font form None to Corbel
        text = font.render('Score: ' + str(self.snake.score), True, color)
        #Change 5: location of score is changed from (0,0) to(400,10)  
        screen.blit(text, (400,10))


