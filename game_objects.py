# game objects file

import pygame as pg
from random import randrange


# two dimentional vector
vec2 = pg.math.Vector2


# class of game object called snake
class Snake:
    def __init__(self, game):
        # assing aplication instance as attribute
        self.game = game
        # assing tile size as attribute to define snake size
        self.size = game.TILE_SIZE
        # make snake a square
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE, game.TILE_SIZE])
        # spawn snake on random tile
        self.rect.center = self.get_random_position()  
        # set direction of snake movement to the right
        self.direction = vec2(0, 0)
        # set delay between snake moves 
        self.move_delay = 200 # miliseconds
        # time reference variable
        self.time = 0
    
    # method to let user control snake movement
    def control(self, event):
        if event.type == pg.KEYDOWN:
            # move up
            if event.key == pg.K_w:
                self.direction = vec2(0, -self.size)
            # move down
            if event.key == pg.K_s:
                self.direction = vec2(0, self.size)
            # move left
            if event.key == pg.K_a:
                self.direction = vec2(-self.size, 0)
            # move right
            if event.key == pg.K_d:
                self.direction = vec2(self.size, 0)
    
    # method to calculate time delta
    def time_delta(self):
        time_now = pg.time.get_ticks()
        # return True if time greater than move_delay has elapsed
        if time_now - self.time > self.move_delay:
            self.time = time_now
            return True
        return False
        
    # method to get random tile on board
    def get_random_position(self):
        return [randrange(self.size // 2, self.game.WINDOW_SIZE - self.size // 2, self.size)] * 2
    
    # method to check if snake and food positions are equal
    def check_food(self):
        # if food eaten change it's position to new random tile
        if self.rect.center == self.game.food.rect.center:
            self.game.food.rect.center = self.get_random_position()
    
    # method to move snake
    def move(self):
        # move snake only after sufficient time interval
        if self.time_delta():
            self.rect.move_ip(self.direction)
        
    # method to update snake state  
    def update_state(self):
        self.check_food()
        self.move()
        
    # method to draw snake object
    def draw_object(self):
        # display snake
        pg.draw.rect(self.game.screen, "green", self.rect)
        
    
    
# class of game object called food
class Food:
    def __init__(self, game):
        # assing aplication instance as attribute
        self.game = game
        # assing tile size as attribute to define snake size
        self.size = game.TILE_SIZE
        # make food a square
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE, game.TILE_SIZE])
        # spawn food on random tile using method from Snake class
        self.rect.center = self.game.snake.get_random_position()  
        
    # method to draw food object
    def draw_object(self):
        pg.draw.rect(self.game.screen, "red", self.rect)