# game objects file

import pygame as pg
import random
from random import randrange
import pathlib


# two dimentional vector
vec2 = pg.math.Vector2

# food sprites location
FOOD_SPRITES_DIR = 'assets/food'


# class of game object called snake
class Snake:
    def __init__(self, game):
        # assing aplication instance as attribute
        self.game = game
        # assing tile size as attribute to define snake size
        self.size = game.TILE_SIZE
        # load snake body images
        self.head_up = pg.image.load('assets/snake/head_up.png').convert_alpha()
        self.head_down = pg.image.load('assets/snake/head_down.png').convert_alpha()
        self.head_right = pg.image.load('assets/snake/head_right.png').convert_alpha()
        self.head_left = pg.image.load('assets/snake/head_left.png').convert_alpha()
        self.body_horizontal = pg.image.load('assets/snake/body_horizontal.png').convert_alpha()
        self.body_vertical = pg.image.load('assets/snake/body_vertical.png').convert_alpha()
        self.body_down_left = pg.image.load('assets/snake/body_down_left.png').convert_alpha()
        self.body_down_right = pg.image.load('assets/snake/body_down_right.png').convert_alpha()
        self.body_up_left = pg.image.load('assets/snake/body_up_left.png').convert_alpha()
        self.body_up_right = pg.image.load('assets/snake/body_up_right.png').convert_alpha()
        self.tail_up = pg.image.load('assets/snake/tail_up.png').convert_alpha()
        self.tail_down = pg.image.load('assets/snake/tail_down.png').convert_alpha()
        self.tail_right = pg.image.load('assets/snake/tail_right.png').convert_alpha()
        self.tail_left = pg.image.load('assets/snake/tail_left.png').convert_alpha()
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
        # load eating sound
        self.eating_sound = pg.mixer.Sound('assets/sound/mlem.wav')
        # load game over bitten sound
        self.game_over_bitten_sound = pg.mixer.Sound('assets/sound/game_over_bitten.wav')
        # load game over bounds sound
        self.game_over_bounds_sound = pg.mixer.Sound('assets/sound/game_over_bounds.wav')
    
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
            self.play_game_over_bitten_sound()
            self.game.new_game()
            
    # method to play eating sound
    def play_eating_sound(self):
        self.eating_sound.play()
        
    # method to play game over bitten sound
    def play_game_over_bitten_sound(self):
        self.game_over_bitten_sound.play()
      
    # method to play game over bounds sound
    def play_game_over_bounds_sound(self):
        self.game_over_bounds_sound.play()
    
    # method to check if snake and food positions are equal
    def check_food(self):
        # if food eaten change it's position to new random tile
        if self.rect.center == self.game.food.rect.center:
            self.game.food.rect.center = self.get_random_position()
            # increase snake length
            self.length += 1
            # change food image
            self.game.food.select_random_image()
            # play eating sound
            self.play_eating_sound()
    
    # method to check if snake crossed the boundary
    def check_borders(self):
        if (self.rect.left < 0) or (self.rect.right > self.game.WINDOW_SIZE) or (self.rect.top < 0) or (self.rect.bottom > self.game.WINDOW_SIZE):
            self.play_game_over_bounds_sound()
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
        #[pg.draw.rect(self.game.screen, "green", segment) for segment in self.segments]
        # for each snake segment
        for index,segment in enumerate(self.segments):
            # if segment is head
            if index == 0:
                # draw head image
                self.game.screen.blit(self.head_up, self.rect)
            else:
                # draw standard rectangle
                pg.draw.rect(self.game.screen, "green", segment)
        
    
    
# class of game object called food
class Food:
    def __init__(self, game):
        # assing aplication instance as attribute
        self.game = game
        # assing tile size as attribute to define snake size
        self.size = game.TILE_SIZE
        # load all food images
        self.images = self.load_food_images()
        # select random food image
        self.image = random.choice(self.images)
        # make food a square
        #self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE, game.TILE_SIZE])
        # make food as chosen image
        self.rect = self.image.get_rect()
        # spawn food on random tile using method from Snake class
        self.rect.center = self.game.snake.get_random_position()
    
    # select random fruit image
    def select_random_image(self):
        self.image = random.choice(self.images)
    
    # method to load food images  
    def load_food_images(self):
        # get all png files
        files = [item for item in pathlib.Path(FOOD_SPRITES_DIR).rglob('*.png') if item.is_file()]
        # load images via pygame library tool
        images = [pg.image.load(file).convert_alpha() for file in files]
        # scale images to the size of tile
        images = [pg.transform.scale(image, (self.size, self.size)) for image in images]
        return images
        
    # method to draw food object
    def draw_object(self):
        #pg.draw.rect(self.game.screen, "red", self.rect)
        # draw random food
        self.game.screen.blit(self.image, self.rect)
