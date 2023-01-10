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

        # method to load and rescale images (runing method in constructor of not fully initialized object, idk if it's the best idea)
        def load_and_rescale_image(name):
            image = pg.image.load(f"assets/snake/{name}.png").convert_alpha()
            return pg.transform.scale(image, (self.size, self.size))
            
        # load snake body images    
        self.head_up = load_and_rescale_image("head_up")
        self.head_down = load_and_rescale_image("head_down")
        self.head_right = load_and_rescale_image("head_right")
        self.head_left = load_and_rescale_image("head_left")
        self.body_horizontal = load_and_rescale_image("body_horizontal")
        self.body_vertical = load_and_rescale_image("body_vertical")
        self.body_down_left = load_and_rescale_image("body_down_left")
        self.body_down_right = load_and_rescale_image("body_down_right")
        self.body_up_left = load_and_rescale_image("body_up_left")
        self.body_up_right = load_and_rescale_image("body_up_right")
        self.tail_up = load_and_rescale_image("tail_up")
        self.tail_down = load_and_rescale_image("tail_down")
        self.tail_right = load_and_rescale_image("tail_right")
        self.tail_left = load_and_rescale_image("tail_left")
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
        # for each snake segment
        for index,segment in enumerate(self.segments):
            # if segment is head
            if index == len(self.segments)-1:
                # draw head image
                self.update_image_head()
                self.game.screen.blit(self.head, segment)
            # if segment is tail
            elif index == 0:
                # draw tail image
                self.update_image_tail()
                self.game.screen.blit(self.tail, segment)
            else:
                # draw body image
                # based on vectors between centers of current and previous segments decide body direction
                previous_segment_tuple = tuple(map(lambda i, j: i - j, self.segments[index + 1].center, segment.center))
                next_segment_tuple = tuple(map(lambda i, j: i - j, self.segments[index - 1].center, segment.center))
                # if first aguments of tuples are zero it means snake is moving verical
                if previous_segment_tuple[0] == next_segment_tuple[0]:
                    # draw vertical body image
                    self.game.screen.blit(self.body_vertical, segment)
                # if second aguments of tuples are zero it means snake is moving horizontal
                elif previous_segment_tuple[1] == next_segment_tuple[1]:
                    # draw horizontal body image
                    self.game.screen.blit(self.body_horizontal, segment)
                else:
                    # if tuple arguments points to up and left direction
                    if previous_segment_tuple[0] == -50 and next_segment_tuple[1] == -50 or previous_segment_tuple[1] == -50 and next_segment_tuple[0]  == -50:
                        # draw up left corner body image
                        self.game.screen.blit(self.body_up_left, segment)
                    # if tuple arguments points to up and right direction
                    elif previous_segment_tuple[0] == 50 and next_segment_tuple[1] == -50 or previous_segment_tuple[1] == -50 and next_segment_tuple[0]  == 50:
                        # draw up right corner body image
                        self.game.screen.blit(self.body_up_right, segment)
                    # if tuple arguments points to down and left direction
                    elif previous_segment_tuple[0] == -50 and next_segment_tuple[1] == 50 or previous_segment_tuple[1] == 50 and next_segment_tuple[0]  == -50:
                        # draw down left corner body image
                        self.game.screen.blit(self.body_down_left, segment)
                    # if tuple arguments points to up and right direction
                    elif previous_segment_tuple[0] == 50 and next_segment_tuple[1] == 50 or previous_segment_tuple[1] == 50 and next_segment_tuple[0]  == 50:
                        # draw down right corner body image
                        self.game.screen.blit(self.body_down_right, segment)
          
          
    # method to update direction of head image
    def update_image_head(self):
        # based on available move directions decide direction of snake head
        if self.directions[pg.K_s] == False: self.head = self.head_up
        elif self.directions[pg.K_w] == False: self.head = self.head_down
        elif self.directions[pg.K_d] == False: self.head = self.head_left
        elif self.directions[pg.K_a] == False: self.head = self.head_right
        else:
            self.head = self.head_up
           
           
    # method to update direction of tail image
    def update_image_tail(self):
        # based on vectors between centers of two first segments decide tail direction
        tail_tuple = tuple(map(lambda i, j: i - j, self.segments[1].center, self.segments[0].center))
        if tail_tuple == (0,50): self.tail = self.tail_up
        elif tail_tuple == (0,-50): self.tail = self.tail_down
        elif tail_tuple == (50,0): self.tail = self.tail_left
        elif tail_tuple == (-50,0): self.tail = self.tail_right   
        
    
    
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
