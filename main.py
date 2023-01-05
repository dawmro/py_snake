# py_snake main file

import pygame as pg
from game_objects import *



# class of main game 
class Game: 
    def __init__(self):
        pg.init()
        # set window size
        self.WINDOW_SIZE = 800 
        # create rendering surface as square
        self.screen = pg.display.set_mode([self.WINDOW_SIZE, self.WINDOW_SIZE])
        # create instance of clock class to be able to set number of frames per second
        self.clock = pg.time.Clock()
    
    # method to create new game
    def new_game(self):
        pass
    
    # method to update game state
    def update_state(self):
        # update rendering surface
        pg.display.flip()
        # set number of frames per second
        self.clock.tick(60)
    
    # method to draw game object
    def draw_object(self):
        # paint work surface black
        self.screen.fill("black")
        
    # method to check for events
    def event_check(self):
        pass
        
    # method to start new game run
    def run(self):
        pass
    
    
if __name__ == "__main__":
    game = Game()
    game.run()