import pygame
import time
import serial
import math

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Platformer")

player_sprite_sheet = pygame.image.load("player.png").convert_alpha()

running = True
clock = pygame.time.Clock()

yinterval = 115
xinterval = 80
size = 80

gravity = 0.09

ser = serial.Serial('/dev/cu.usbmodem11101', 115200, timeout=1)
time.sleep(2)


class Player:
    def __init__(self):

        player_idle = player_sprite_sheet.subsurface((0, 0, size, size))
        player_idle = pygame.transform.scale(player_idle, (140, 140))

        player_shoot = player_sprite_sheet.subsurface((0, 3.2 * yinterval + 10, size, size))
        player_shoot = pygame.transform.scale(player_shoot, (140, 140))

        frames = []
        for i in range(6):
            frame = player_sprite_sheet.subsurface((i * xinterval, yinterval, size, size))
            frame = pygame.transform.scale(frame, (140, 140))
            frame = pygame.transform.flip(frame, True, False)
            frames.append(frame)

        self.idle_frame = player_idle
        self.shooting_frame = player_shoot
        self.moving_left_frames = tuple(frames)

        frames = []
        for frame in self.moving_left_frames:
            frames.append(pygame.transform.flip(frame, True, False))

        self.moving_right_frames = tuple(frames)
        self.current_frame = self.idle_frame

        self.rect = self.current_frame.get_rect()
        self.rect.x = 400
        self.rect.y = 556

        self.frame_index = 0
        self.animation_speed = 0.2
        self.velocity = 1
        self.moving_left = False
        self.moving_right = False

        self.bullet = Bullet(self.rect.centerx, self.rect.centery, 45, 10)
        self.shooting = False

    def update(self):

        if self.moving_left:
            self.rect.y = 556 + 25
            self.move_left()

        elif self.moving_right:
            self.rect.y = 556 + 25
            self.move_right()

        elif self.shooting:
            self.current_frame = self.shooting_frame
            self.rect.y = 556

        else:
            self.current_frame = self.idle_frame
            self.rect.y = 556

        screen.blit(self.current_frame, self.rect)

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


class Bullet:
    def __init__(self, x, y, angle, power):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.angle = angle
        self.power = power
        self.radius = 5
        self.state = None

        self.velocity_x = 0
        self.velocity_y = 0

    def reset(self, x, y):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y

        self.velocity_x = math.cos(math.radians(self.angle)) * self.power
        self.velocity_y = math.sin(math.radians(self.angle)) * self.power

    def update(self):
        if self.state == "trajectory":

            sim_x = self.start_x
            sim_y = self.start_y
            sim_vx = math.cos(math.radians(self.angle)) * self.power
            sim_vy = math.sin(math.radians(self.angle)) * self.power

            while sim_y < 706 and 0 < sim_x < 1524:
                pygame.draw.circle(screen, (0, 0, 255), (int(sim_x), int(sim_y)), 3)
                sim_x += sim_vx
                sim_y -= sim_vy
                sim_vy -= gravity

        elif self.state == "shoot":
            
            speed_multipier = 10

            self.x += self.velocity_x * speed_multipier
            self.y -= self.velocity_y * speed_multipier
            self.velocity_y -= gravity * speed_multipier

            pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius)

            if self.y >= 706:
                self.state = None


player = Player()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ser.close()
            running = False

    data = ser.readline().decode().strip()

    if data == "LEFT":
        player.moving_left = True
        player.moving_right = False
        player.velocity = 5
        player.bullet.state = None

    elif data == "RIGHT":
        player.moving_right = True
        player.moving_left = False
        player.velocity = 5
        player.bullet.state = None

    elif data == "STOP":
        player.moving_left = False
        player.moving_right = False
        player.velocity = 0

    elif data.startswith("ANGLE: "):
        value = int(data.replace("ANGLE: ", ""))
        angle = 20 + (value / 1023) * 60
        player.bullet.angle = int(angle)

        player.bullet.reset(player.rect.centerx, player.rect.centery)
        player.bullet.state = "trajectory"

    elif data.startswith("POWER: "):
        value = int(data.replace("POWER: ", ""))
        player.bullet.power = int(value) 

        player.bullet.reset(player.rect.centerx, player.rect.centery)
        player.bullet.state = "trajectory"

    elif data == "SHOOT":
        player.bullet.reset(player.rect.centerx, player.rect.centery)
        player.bullet.state = "shoot"

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (0, 700, 1524, 10))

    player.update()
    player.bullet.update()

    pygame.display.flip()
    clock.tick(120)