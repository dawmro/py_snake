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
        # length of snake
        self.length = 1
        # list of segments
        self.segments = []
        # permisions for directions of movement
        self.directions = {pg.K_w: True, pg.K_s: True, pg.K_a: True, pg.K_d: True}
    
    # method to let user control snake movement
    def control(self, event):
        if event.type == pg.KEYDOWN:
            # move up if allowed
            if event.key == pg.K_w and self.directions[pg.K_w]:
                self.direction = vec2(0, -self.size)
                # disallow to move down
                self.directions = {pg.K_w: True, pg.K_s: False, pg.K_a: True, pg.K_d: True}
            # move down if allowed
            if event.key == pg.K_s and self.directions[pg.K_s]:
                self.direction = vec2(0, self.size)
                # disallow to move up
                self.directions = {pg.K_w: False, pg.K_s: True, pg.K_a: True, pg.K_d: True}
            # move left if allowed
            if event.key == pg.K_a and self.directions[pg.K_a]:
                self.direction = vec2(-self.size, 0)
                # disallow to move right
                self.directions = {pg.K_w: True, pg.K_s: True, pg.K_a: True, pg.K_d: False}
            # move right if allowed
            if event.key == pg.K_d and self.directions[pg.K_d]:
                self.direction = vec2(self.size, 0)
                # disallow to move left
                self.directions = {pg.K_w: True, pg.K_s: True, pg.K_a: False, pg.K_d: True}
    
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
    
    # check if snake bites its own tail
    def check_tail_biting(self):
        # check length of segments versus length of set of coordinates for each segment
        if len(self.segments) != len(set(segment.center for segment in self.segments)):
            # if snake bit his own tail (two segments are on the same coordinate) then lenghts are different, in that case start new game
            self.game.new_game()
    
    # method to check if snake and food positions are equal
    def check_food(self):
        # if food eaten change it's position to new random tile
        if self.rect.center == self.game.food.rect.center:
            self.game.food.rect.center = self.get_random_position()
            # increase snake length
            self.length += 1
    
    # method to check if snake crossed the boundary
    def check_borders(self):
        if (self.rect.left < 0) or (self.rect.right > self.game.WINDOW_SIZE) or (self.rect.top < 0) or (self.rect.bottom > self.game.WINDOW_SIZE):
            self.game.new_game()
        
    
    # method to move snake
    def move(self):
        # move snake only after sufficient time interval
        if self.time_delta():
            self.rect.move_ip(self.direction)
            # write next snake position to list of segments
            self.segments.append(self.rect.copy())
            # cut list along snake length
            self.segments = self.segments[-self.length:]
        
    # method to update snake state  
    def update_state(self):
        self.check_tail_biting()
        self.check_borders()
        self.check_food()
        self.move()
        
    # method to draw snake object
    def draw_object(self):
        # display each snake segment
        [pg.draw.rect(self.game.screen, "green", segment) for segment in self.segments]
        
    
    
# class of game object called food
class Food:
    def __init__(self, game):
        # assing aplication instance as attribute
        self.game = game
        # assing tile size as attribute to define snake size
        self.size = game.TILE_SIZE
        # load apple
        self.apple = pg.image.load('images/apple.png').convert_alpha()
        # make food a square
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE-5, game.TILE_SIZE-5])
        # spawn food on random tile using method from Snake class
        self.rect.center = self.game.snake.get_random_position()
        
        
    # method to draw food object
    def draw_object(self):
        #pg.draw.rect(self.game.screen, "red", self.rect)
        # draw apple
        self.game.screen.blit(self.apple, self.rect)