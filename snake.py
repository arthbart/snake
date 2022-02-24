##########IMPORTS##########
import pygame
import sys
from random import randint

##########GLOBALS##########
SPEED = 20

SIZE_X = 21
SIZE_Y = 21

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

##########SNAKE##########
class snake(object):

    def __init__(self):
        self.score = 0
        self.positions = [(5, 10), (4, 10), (3, 10)]
        self.directions = [RIGHT]

    # Richtung ändern
    def turn(self, direction):
        if direction == self.directions[-1] or (direction[0] * -1, direction[1] * -1) == self.directions[-1] or len(self.directions) > 2:
            return
        else:
            self.directions.append(direction)

    # Bewegen
    def move(self):
        current = self.positions[0]
        if len(self.directions) > 1:
            self.directions.pop(0)
        x, y = self.directions[0]
        new = ((current[0] + x), (current[1] + y))
        if new in self.positions[1:-1] or new[0] < 0 or new[1] < 0 or new[0] >= SIZE_X or new[1] >= SIZE_Y:
            self.reset()
        else:
            self.positions.insert(0, new)
            if not self.positions[0] == food.position:
                self.positions.pop()
            else:
                self.score += 1
                food.randomize_position()
    # Reset
    def reset(self):
        self.score = 0
        self.positions = [(5, 10), (4, 10), (3, 10)]
        self.directions = [RIGHT]

	# Input von Tasten
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

    # Grafik zeichnen
    def draw(self, display):
        for index, i in enumerate(self.positions):
            pygame.draw.rect(display, (255, 255, 255), pygame.Rect((i[0] * 12 + 1, i[1] * 12 + 1), (10, 10)))

##########FOOD##########
class food(object):
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
    def randomize_position(self):
        while True:
            self.position = (randint(0, SIZE_X - 1), randint(0, SIZE_Y - 1))
            if self.position not in snake.positions:
                break
    def draw(self, display):
        pygame.draw.rect(display, (205, 44, 62), pygame.Rect((self.position[0] * 12 + 1, self.position[1] * 12 + 1), (10, 10)))

##########FILL##########
def fill(surface):
    r = pygame.Rect((0, 0), (SIZE_X * 12, SIZE_Y * 12))
    pygame.draw.rect(surface, (1, 2, 20), r)

##########LOOP##########
pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SIZE_X * 12, SIZE_Y * 12), 0, 32)
pygame.display.set_caption("")

surface = pygame.Surface(screen.get_size())
surface = surface.convert()

snake = snake()
food = food()

score = 0
while True:
    clock.tick(SPEED)

    snake.handle_keys()
    snake.move()
    pygame.display.set_caption(str(snake.score))

    fill(surface)
    snake.draw(surface)
    food.draw(surface)

    screen.blit(surface, (0, 0))
    pygame.display.update()

main()
