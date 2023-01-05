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
        
        
    # method to update snake state  
    def update_state(self):
        pass
        
    # method to draw snake object
    def draw_object(self):
        # display snake
        pg.draw.rect(self.game.screen, "green", self.rect)
        
    
    
# class of game object called food
class Food:
    def __init__(self, game):
        pass
        
    # method to draw food object
    def draw_object(self):
        pass