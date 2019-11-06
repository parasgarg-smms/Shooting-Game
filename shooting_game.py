import math
import random
import timeit
import pygame

x_min = 0
y_min = 0
x_max = 800
y_max = 600
pygame.init()
gameDisplay = pygame.display.set_mode((x_max, y_max))
score_x = 10
score_y = 10
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
temp = (172, 223, 191)
FPS = 20
font = pygame.font.SysFont(None, 25)
bullets_x = 780
bullets_y = 10
pygame.display.set_caption("SShooting board")
clock = pygame.time.Clock()
score = 0

initial_enemies = 15
enemy_generation_count = 3


# pygame.display.flip()

class gun_reload:
    def __init__(self):
        self.x = 380
        self.y = 540
        self.width = 75
        self.height = 25
        self.bullets = 12
        self.time_take_fire = 1
        self.color = temp

    def draw(self):
        pygame.draw.rect(gameDisplay, black, [self.x, self.y, self.width, self.height])
        screen_score = font.render("RELOAD", True, temp)
        gameDisplay.blit(screen_score, [self.x, self.y])

    def on_reload(self):
        self.bullets = 12

    def check_reload_hits(self, x, y):
        if (x >= self.x and x < self.x + self.width) and (y >= self.y and y < self.y + self.width):
            return True


button = gun_reload()


def display_bullets_left(countBullets):
    screen_score = font.render("{}".format(countBullets), True, blue)
    gameDisplay.blit(screen_score, [bullets_x, bullets_y])


def display_score():
    screen_score = font.render("{}".format(score), True, blue)
    gameDisplay.blit(screen_score, [score_x, score_y])


class enemy:
    def __init__(self):
        self.x = random.randrange(20, 780)
        self.y = random.randrange(20, 580)
        self.width = 30
        self.height = 30
        self.color = random.choice([black, red, green, blue])
        self.time_attack = random.randrange(1, 5)

    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.width, self.height])

    def check_target_hits(self, x, y):
        if (x >= self.x and x < self.x + self.width) and (y >= self.y and y < self.y + self.width):
            return True
        else:
            return False


def creating_enemies(enemyobjects):
    duplicateobjects = list(enemyobjects)
    for objects in duplicateobjects:
        objects.draw()
    pygame.display.update()


def hits_enemy_from_all_objects(enemyObjects, x, y):
    global score
    duplicateobjects = list(enemyObjects)

    for object in duplicateobjects:
        value = object.check_target_hits(x, y)
        if value == True:
            score += 5
            enemyObjects.remove(object)


time = math.floor(timeit.default_timer())


def mainLoop():
    gameExit = False
    global time
    enemyobjects = [enemy() for i in range(initial_enemies)]

    while not gameExit:
        new = math.floor(timeit.default_timer())
        if new == time:
            new_objects = [enemy() for i in range(enemy_generation_count)]
            enemyobjects = enemyobjects + new_objects
            time += 2
        gameDisplay.fill(white)
        creating_enemies(enemyobjects)
        # creating_enemies(3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    if button.check_reload_hits(x, y):
                        button.on_reload()
                        continue
                    if button.bullets > 0:
                        button.bullets -= 1
                        hits_enemy_from_all_objects(enemyobjects, x, y)
                    else:
                        pass

        button.draw()
        display_score()
        display_bullets_left(button.bullets)
        pygame.display.update()
        clock.tick(FPS)
    print(score)

    pygame.quit()
    quit()


if __name__ == '__main__':
    mainLoop()
