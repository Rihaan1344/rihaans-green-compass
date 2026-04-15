import pygame
import time
import serial

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Platformer")

player_sprite_sheet = pygame.image.load("player.png").convert_alpha()

running = True
clock = pygame.time.Clock()

yinterval = 115
xinterval = 80
size = 80

ser = serial.Serial('/dev/cu.usbmodem1101', 115200, timeout=1)
time.sleep(2)

class Player:
    def __init__(self):

        # Idle frame
        player_idle = player_sprite_sheet.subsurface((0, 0, size, size))
        player_idle = pygame.transform.scale(player_idle, (140, 140))

        # Moving left frames
        frames = []
        for i in range(6):
            frame = player_sprite_sheet.subsurface((i * xinterval, yinterval, size, size))
            frame = pygame.transform.scale(frame, (140, 140))
            frame = pygame.transform.flip(frame, True, False)
            frames.append(frame)

        self.idle_frame = player_idle
        self.moving_left_frames = tuple(frames)

        frames = []
        for frame in self.moving_left_frames:
            frames.append(pygame.transform.flip(frame, True, False))

        self.moving_right_frames = tuple(frames)
        self.current_frame = self.idle_frame

        self.rect = self.current_frame.get_rect()
        self.rect.x = 400
        self.rect.y = 556

        self.velocity = 1
        self.frame_index = 0
        self.animation_speed = 0.2
        self.moving_left = False
        self.moving_right = False

    def update(self):
        if self.moving_left:
            self.rect.y = 556 + 25
            self.move_left()
        elif self.moving_right:
            self.rect.y = 556 + 25
            self.move_right()
        else:
            self.current_frame = self.idle_frame
            self.rect.y = 556

    def draw(self, surface):
        surface.blit(self.current_frame, self.rect)

    def move_left(self):
        self.frame_index += self.animation_speed
        self.rect.x -= self.velocity
        if self.frame_index >= len(self.moving_left_frames):
            self.frame_index = 0
        self.current_frame = self.moving_left_frames[int(self.frame_index)]
    
    def move_right(self):
        self.frame_index += self.animation_speed
        self.rect.x += self.velocity
        if self.frame_index >= len(self.moving_right_frames):
            self.frame_index = 0

        self.current_frame = self.moving_right_frames[int(self.frame_index)]

player = Player()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ser.close()
            running = False
            
    data = ser.readline().decode().strip()
    if data.startswith("LEFT"):
            player.moving_left = True
            player.moving_right = False
            try:
                player.velocity = float(data[5:].strip())
            except ValueError:
                pass  # ignore bad data
    elif data.startswith("RIGHT"):
            player.moving_right = True
            player.moving_left = False
            try:
                player.velocity = float(data[6:].strip())
            except ValueError:
                pass  # ignore bad data
    elif data == "STOP":
            player.velocity = 0
            player.moving_left = False
            player.moving_right = False


    player.update()

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (0, 700, 1524, 10))

    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)