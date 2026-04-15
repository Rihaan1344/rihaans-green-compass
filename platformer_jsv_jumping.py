import pygame
import serial
import time
import math

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Platformer")

player_sprite_sheet = pygame.image.load("player.png").convert_alpha()

running = True
clock = pygame.time.Clock()

gravity = 0.09

yinterval = 115
xinterval = 80
size = 80

ser = serial.Serial('/dev/cu.usbmodem1101', 115200, timeout=1)
time.sleep(2)

class Player:
    def __init__(self):
        """INITIALIZE ALL PLAYER FRAMES"""

        #IDLE
        player_idle = player_sprite_sheet.subsurface((0, 0, size, size))
        player_idle = pygame.transform.scale(player_idle, (140, 140))
        self.idle_frame = player_idle

        #SHOOTING
        player_shoot = player_sprite_sheet.subsurface((0, 3.2 * yinterval + 10, size, size))
        player_shoot = pygame.transform.scale(player_shoot, (140, 140))
        self.shooting_frame = player_shoot

        #MOVING LEFT
        frames = []
        for i in range(6):
            frame = player_sprite_sheet.subsurface((i * xinterval, yinterval, size, size))
            frame = pygame.transform.scale(frame, (140, 140))
            frame = pygame.transform.flip(frame, True, False)
            frames.append(frame)

        self.moving_left_frames = list(frames)

        #MOVING RIGHT
        frames = []
        for frame in self.moving_left_frames:
            frames.append(pygame.transform.flip(frame, True, False))

        self.moving_right_frames = tuple(frames)

        #MOVING LEFT AND SHOOTING
        frames = []
        for i in range(6):
            frame = player_sprite_sheet.subsurface((i * xinterval, 200, size, size))
            frame = pygame.transform.scale(frame, (140, 140))
            frame = pygame.transform.flip(frame, True, False)
            frames.append(frame)
        
        self.moving_left_shooting_frames = list(frames)

        #MOVING RIGHT AND SHOOTING
        frames = []
        for frame in self.moving_left_shooting_frames:
            frames.append(pygame.transform.flip(frame, True, False))
        
        self.moving_right_shooting_frames = tuple(frames)

        #JUMPING
        frames = []
        for i in range(3):
            frame = player_sprite_sheet.subsurface((i * xinterval, 295, size, size))
            frame = pygame.transform.scale(frame, (140, 140))
            frame = pygame.transform.flip(frame, True, False)
            frames.append(frame)

        self.jumping_frames = list(frames)

        #VARIABLES
        self.current_frame = self.idle_frame #current frame starts as idle frame
        self.rect = self.current_frame.get_rect() #rect coords
        self.rect.x = 400 
        self.rect.y = 556
        self.jumping_right = False #keep track of which way jump frames are facing
        self.idle_right = True #keep track of which way idle frame is facing to know which way to flip jump frames when jumping from idle position
        self.frame_index = 0 #keep track of which frame in the animation sequence we are on
        self.animation_speed = 0.2 #how fast the animation should play (higher is faster)
        self.velocity = 1 #how fast the player should move in left and right direction
        self.jump_power = 1.5 #how high the player should jump (higher is higher)

    def move_left(self):
        self.facing_right = False #keep track of which way player is facing for idle frame
        self.frame_index += self.animation_speed # increase by a decimal value for slow increament
        self.rect.x -= self.velocity # move in left direction
        if self.frame_index >= len(self.moving_left_frames):
            self.frame_index = 0 #if frame is out of range, reset to 0
        self.current_frame = self.moving_left_frames[int(self.frame_index)] # set current frame to the correct frame in the animation sequence based on the frame index
        self.rect.y = 556 + 25 # adjust y position for moving animation because the frames are slightly different than the idle frame

    def move_right(self):
        self.facing_right = True #keep track of which way player is facing for idle frame
        self.frame_index += self.animation_speed # increase by a decimal value for slow increament
        self.rect.x += self.velocity   # move in right direction
        if self.frame_index >= len(self.moving_right_frames): 
            self.frame_index = 0 # if frame is out of range, reset to 0
        self.current_frame = self.moving_right_frames[int(self.frame_index)] # set current frame to the correct frame in the animation sequence based on the frame index
        self.rect.y = 556 + 25 # adjust y position for moving animation because the frames are slightly different than the idle frame

    def jump(self, l: bool, r: bool):
        self.rect.y -= 1 # move up slightly to trigger the jump animation frames
        if (self.jumping_right and self.current_frame in self.moving_left_frames) \
            or (not self.jumping_right and self.current_frame in self.moving_right_frames):
            #if the player is currently facing the opposite direction of the jump frames, flip the jump frames to the correct direction
            for i in range(len(self.jumping_frames)):
                self.jumping_frames[i] = pygame.transform.flip(self.jumping_frames[i], True, False)
            self.jumping_right = not self.jumping_right # flip the jump frames to the correct direction based on which way the player is facing
        if (self.idle_right and not self.jumping_right) or (not self.idle_right and self.jumping_right):
            #if we're jumping right but facing left or jumping left but facing right(in idle), flip idle frame
            self.idle_frame = pygame.transform.flip(self.idle_frame, True, False)
            self.idle_right = not self.idle_right # flip idle frame to the correct direction
            
        while self.rect.y < 556:
            self.frame_index += self.animation_speed # increase by a decimal value for slow increament
            self.rect.y -= self.jump_power # move in up direction
            self.jump_power -= gravity # decrease jump power by gravity to create a parabolic jump

            if l:
                self.rect.x -= self.velocity # move in left direction while jumping
            elif r:
                self.rect.x += self.velocity # move in right direction while jumping

            if self.frame_index > 2:
                self.frame_index = 2 #make it stay in the jump position instead of cyclying through frames
            self.current_frame = self.jumping_frames[int(self.frame_index)] # set current frame to the correct frame in the animation sequence based on the frame index

            screen.fill((255, 255, 255))
            pygame.draw.rect(screen, (0, 0, 0), (0, 700, 1524, 10)) #draw ground
            screen.blit(self.current_frame, self.rect)
            pygame.display.flip()
            clock.tick(60)
            
        self.current_frame = self.idle_frame # reset to idle frame after jump is finished
        self.rect.y = 556 
        self.jump_power = 0.5 # reset jump power for next jump
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (0, 700, 1524, 10)) #draw ground
        screen.blit(self.current_frame, self.rect)
        pygame.display.flip()
        clock.tick(60)
        global running
        running = True #unpause the game loop after the jump is finished to allow for input again


player = Player()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    data = ser.readline().decode().strip()
    if data.startswith("LEFT"):
        player.move_left()
        try:
            player.velocity = float(data[5:].strip())
        except ValueError:
            pass  # ignore bad data
    elif data.startswith("RIGHT"):
        player.move_right()
        try:
            player.velocity = float(data[6:].strip())
        except ValueError:  
            pass  # ignore bad data
    elif data == "JUMP":
        player.jump(player.current_frame in player.moving_left_frames, player.current_frame in player.moving_right_frames)
        

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (0, 700, 1524, 10)) #draw ground
    screen.blit(player.current_frame, player.rect)
    pygame.display.flip()
    clock.tick(60)