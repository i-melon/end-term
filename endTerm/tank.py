import pygame
import random
from enum import Enum
from pygame import mixer

pygame.init()
pygame.display.set_caption("Tanks")
screen = pygame.display.set_mode((800, 600))
mixer.music.load("Music/1.wav")
mixer.music.play(-1)

GG = mixer.Sound("Music/GG_tank.wav")
shoot = mixer.Sound("Music/shoot.wav")


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class shot(Enum):
    SHOT = 1


class Tank:
    def __init__(self, color, color1, Place_x, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP,
                 d_down=pygame.K_DOWN):
        self.x = random.randint(200, 600)
        self.y = random.randint(200, 400)
        self.Place_x = Place_x
        self.speed = 3
        self.color = color
        self.color1 = color1
        self.width = 50
        self.life_count = 3
        self.direction = Direction.RIGHT
        self.KEYS = {d_right: Direction.RIGHT, d_left: Direction.LEFT,
                     d_up: Direction.UP, d_down: Direction.DOWN}

    def draw(self):
        Centre_tank = (self.x + self.width // 2, self.y + self.width // 2)
        pygame.draw.rect(screen, self.color, (self.x-5, self.y-5, self.width+10, self.width+10))
        pygame.draw.circle(screen, self.color1, Centre_tank, self.width // 2, 5)

        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen, self.color1,
                             (Centre_tank[0] + 19, Centre_tank[1]),
                             (self.x + self.width + self.width // 2, self.y + self.width // 2), 4)
        if self.direction == Direction.LEFT:
            pygame.draw.line(screen, self.color1,
                             (Centre_tank[0] - 19, Centre_tank[1]),
                             (self.x - self.width // 2, self.y + self.width // 2), 4)
        if self.direction == Direction.UP:
            pygame.draw.line(screen, self.color1,
                             (Centre_tank[0], Centre_tank[1] - 20),
                             (self.x + self.width // 2, self.y - self.width // 2), 4)
        if self.direction == Direction.DOWN:
            pygame.draw.line(screen, self.color1,
                             (Centre_tank[0], Centre_tank[1] + 19),
                             (self.x + self.width // 2, self.y + self.width + self.width // 2), 4)

    def Change_dir(self, direction):
        self.direction = direction

    def random_pos(self):
        self.x = random.randint(200, 600)
        self.y = random.randint(200, 400)

    def life_counter(self):
        font = pygame.font.Font('freesansbold.ttf', 36)
        text = font.render("Lives: " + str(self.life_count), 1, self.color)
        place = text.get_rect(center=(self.Place_x, 50))
        screen.blit(text, place)

    def move(self):
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed

        if self.x > screen.get_size()[0]:
            self.x = 0 - self.width
        if self.x < 0 - self.width:
            self.x = screen.get_size()[0]
        if self.y > screen.get_size()[1]:
            self.y = 0 - self.width
        if self.y < 0 - self.width:
            self.y = screen.get_size()[1]

        self.draw()


class Bullet:
    def __init__(self, tank, shoot=pygame.K_RETURN):
        self.bullet_x = -100
        self.bullet_y = -100
        self.bullet_speed = 15
        self.tank = tank
        self.bullet_width = 20
        self.bullet_height = 4
        self.is_fired = False
        self.direction = Direction.RIGHT

        self.KEYS = {shoot: shot.SHOT}

    def bullet_pos(self):
        if self.direction == Direction.RIGHT and self.is_fired == False:
            self.bullet_x = self.tank.x + self.tank.width + self.tank.width // 2
            self.bullet_y = self.tank.y + self.tank.width // 2
            self.bullet_width = 20
            self.bullet_height = 4
        if self.direction == Direction.LEFT and self.is_fired == False:
            self.bullet_x = self.tank.x - self.tank.width // 2
            self.bullet_y = self.tank.y + self.tank.width // 2
            self.bullet_width = 20
            self.bullet_height = 4
        if self.direction == Direction.UP and self.is_fired == False:
            self.bullet_x = self.tank.x + self.tank.width // 2
            self.bullet_y = self.tank.y - self.tank.width // 2
            self.bullet_width = 4
            self.bullet_height = 20
        if self.direction == Direction.DOWN and self.is_fired == False:
            self.bullet_x = self.tank.x + self.tank.width // 2
            self.bullet_y = self.tank.y + self.tank.width + self.tank.width // 2
            self.bullet_width = 4
            self.bullet_height = 20

    def draw_bullet(self):
        if self.is_fired:
            if self.direction == Direction.RIGHT:
                pygame.draw.rect(screen, self.tank.color,
                                 (self.bullet_x, self.bullet_y, self.bullet_width, self.bullet_height))
            if self.direction == Direction.LEFT:
                pygame.draw.rect(screen, self.tank.color, (
                self.bullet_x - self.bullet_width, self.bullet_y, self.bullet_width, self.bullet_height))
            if self.direction == Direction.UP:
                pygame.draw.rect(screen, self.tank.color, (
                self.bullet_x, self.bullet_y - self.bullet_height, self.bullet_width, self.bullet_height))
            if self.direction == Direction.DOWN:
                pygame.draw.rect(screen, self.tank.color,
                                 (self.bullet_x, self.bullet_y, self.bullet_width, self.bullet_height))

    def fire_false(self):
        if self.bullet_x >= screen.get_size()[0]:
            self.is_fired = False
        if self.bullet_x <= 0:
            self.is_fired = False
        if self.bullet_y >= screen.get_size()[1]:
            self.is_fired = False
        if self.bullet_y <= 0:
            self.is_fired = False

    def direction_bullet(self):
        if self.is_fired == False:
            if self.tank.direction == Direction.RIGHT:
                self.direction = Direction.RIGHT
            if self.tank.direction == Direction.LEFT:
                self.direction = Direction.LEFT
            if self.tank.direction == Direction.UP:
                self.direction = Direction.UP
            if self.tank.direction == Direction.DOWN:
                self.direction = Direction.DOWN

    def move_bullet(self):
        if self.direction == Direction.RIGHT:
            self.bullet_x += self.bullet_speed
        if self.direction == Direction.LEFT:
            self.bullet_x -= self.bullet_speed
        if self.direction == Direction.UP:
            self.bullet_y -= self.bullet_speed
        if self.direction == Direction.DOWN:
            self.bullet_y += self.bullet_speed

        self.draw_bullet()
        self.direction_bullet()
        self.fire_false()

    def collision_tank(self, tank_enemy):
        lx1 = self.bullet_x
        lx2 = tank_enemy.x
        rx1 = self.bullet_x + self.bullet_width
        rx2 = tank_enemy.x + tank_enemy.width
        ty1 = self.bullet_y
        ty2 = tank_enemy.y
        by1 = self.bullet_y + self.bullet_height
        by2 = tank_enemy.y + tank_enemy.width
        lx = max(lx1, lx2)
        rx = min(rx1, rx2)
        ty = max(ty1, ty2)
        by = min(by1, by2)
        if lx <= rx and ty <= by:
            return True
        return False


game = True
music_gg = False
tt = 0

tank0 = Tank((17, 57, 187), (0, 0, 255), 80)
tank1 = Tank((255, 35, 35), (255, 0, 15), 720, pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)

tanks = [tank0, tank1]

bullet0 = Bullet(tank0)
bullet1 = Bullet(tank1, pygame.K_SPACE)

bullets = [bullet0, bullet1]

FPS = 60

clock = pygame.time.Clock()

while game:
    mills = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                game = False
            for tank in tanks:
                if event.key in tank.KEYS.keys():
                    tank.Change_dir(tank.KEYS[event.key])

            for bullet in bullets:

                if event.key in bullet.KEYS.keys():
                    bullet.direction_bullet()
                    bullet.bullet_pos()
                    if bullet.is_fired == False:
                        shoot.play()
                    bullet.is_fired = True

    screen.fill((100,100,100))

    for tank in tanks:
        tank.move()
        tank.life_counter()

        if tank.life_count == 0:
            tank0.speed = 0
            tank1.speed = 0
            bullet0.bullet_speed = 0
            bullet1.bullet_speed = 0
            bullet0.is_fired = True
            bullet1.is_fired = True
            bullet0.bullet_x = 1100
            bullet1.bullet_x = 1100
            mixer.music.stop()
            music_gg = True

            font = pygame.font.Font('freesansbold.ttf', 80)
            text = font.render("Game Over", 1, (237, 20, 0))
            place = text.get_rect(center=(400, 275))
            screen.blit(text, place)

            font = pygame.font.Font('freesansbold.ttf', 40)
            text = font.render("Press ESC to Exit", 1, (0, 22, 255))
            place = text.get_rect(center=(400, 335))
            screen.blit(text, place)

    if music_gg == True and tt == 0:
        GG.play()
        tt = 1

    for bullet in bullets:
        bullet.move_bullet()

    if bullet0.collision_tank(tank1):
        tank1.random_pos()
        tank1.life_count -= 1
        bullet0.bullet_x = -100
        bullet0.bullet_y = -100
        bullet0.is_fired = False

    if bullet1.collision_tank(tank0):
        tank0.random_pos()
        tank0.life_count -= 1
        bullet1.bullet_x = -100
        bullet1.bullet_y = -100
        bullet1.is_fired = False

    pygame.display.flip()