# py_snake main file

import pygame as pg
from game_objects import *
import sys


# class of main game 
class Game: 
    def __init__(self):
        pg.init()
        # set window and tile size
        self.WINDOW_SIZE = 800 
        self.TILE_SIZE = 50
        # create rendering surface as square
        self.screen = pg.display.set_mode([self.WINDOW_SIZE, self.WINDOW_SIZE])
        # create instance of clock class to be able to set number of frames per second
        self.clock = pg.time.Clock()
        self.new_game()
        
    # method to draw grid on work surface
    def draw_grid(self):
        # draw vertical lines
        [pg.draw.line(self.screen, [64] * 3, (x, 0), (x, self.WINDOW_SIZE)) for x in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]
        # draw horizontal lines
        [pg.draw.line(self.screen, [64] * 3, (0, y), (self.WINDOW_SIZE, y)) for y in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]
    
    # method to create new game
    def new_game(self):
        # create instance of Snake
        self.snake = Snake(self)
        # create instance of Food
        self.food = Food(self)
    
    # method to update game state
    def update_state(self):
        # update snake state
        self.snake.update_state()
        # update rendering surface
        pg.display.flip()
        # set number of frames per second
        self.clock.tick(60)
    
    # method to draw game object
    def draw_object(self):
        # paint work surface black
        self.screen.fill("black")
        self.draw_grid()
        # display snake
        self.snake.draw_object()
        # display food
        self.food.draw_object()
        
    # method to check for events
    def event_check(self):
        for event in pg.event.get():
            # close game if QUIT button pressed 
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        
    # method to start new game run
    def run(self):
        # run all methods in a loop
        while True:
            self.event_check()
            self.update_state()
            self.draw_object()
    
    
if __name__ == "__main__":
    game = Game()
    game.run()