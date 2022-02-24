##########IMPORT##########
import pygame
import sys
import numpy as np
from random import randint

########PYGAME-INIT########
pygame.init()

##########GLOBALS##########
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

###########SPIEL###########
class Game(object):

    # Initialisieren
    def __init__(self, size_x, size_y, speed):
        self.size_x = size_x
        self.size_y = size_y
        self.speed = speed
        self.snake_init()
        self.food_init()
        self.score = 0
        self.trys = 0
        self.iterations = 0
        self.display = pygame.display.set_mode((self.size_x * 12, self.size_y * 12), 0, 32)
        self.clock = pygame.time.Clock()

    # Umfeld zurücksetzen
    def reset(self):
        self.snake_init()
        self.food_init()
        self.score = 0
        self.trys = 0

    # Snake Initialisieren
    def snake_init(self):
        self.snake_positions = [(5, 10), (4, 10), (3, 10)]
        self.snake_direction = RIGHT

    # Food Initialisieren
    def food_init(self):
        while True:
            self.food_position = ((randint(0, self.size_x - 1), randint(0, self.size_y - 1)))
            if self.food_position not in self.snake_positions:
                break

    # Aktion machen, Gameover? Belohnung und Score zurück
    def play(self, action):
        reward = 0 # Reward setzen
        self.trys += 1 # Schritte zählen
        # Bewegen
        self.move(action)
        # Essen?
        if self.snake_positions[0] == self.food_position:
            self.trys = 0
            reward = 10 # Reward erhöhen
            self.score += 1 # Score erhöhen
            self.food_init() # Essen neu platzieren
        else:
            self.snake_positions.pop() # Letzten Block Schlange löschen
        # Game over?
        if self.snake_positions[0] in self.snake_positions[1:-1] \
        or self.snake_positions[0][0] < 0 \
        or self.snake_positions[0][1] < 0 \
        or self.snake_positions[0][0] >= self.size_x \
        or self.snake_positions[0][1] >= self.size_y \
        or self.trys > (self.size_x * self.size_y):
            self.iterations += 1
            reward = -10 # Reward senken
            return reward, True, self.score
        # Pause
        self.clock.tick(self.speed)
        # Zeichnen
        self.draw()
        pygame.display.set_caption("score: " + str(self.score))
        # Return
        return reward, False, self.score

    # Hindernis an P?
    def hindernis(self, p):
        if p in self.snake_positions[1:-1] \
        or p[0] < 0 \
        or p[1] < 0 \
        or p[0] >= self.size_x \
        or p[1] >= self.size_y:
            return True
        else:
            return False

    # Umfeld Wahrnehmen
    def perceive(self):
        return np.array([
            # Richtung
            self.snake_direction == UP,
            self.snake_direction == DOWN,
            self.snake_direction == LEFT,
            self.snake_direction == RIGHT,
            # Essen
            self.food_position[0] < self.snake_positions[0][0],
            self.food_position[0] > self.snake_positions[0][0],
            self.food_position[1] < self.snake_positions[0][1],
            self.food_position[1] > self.snake_positions[0][1],
            # Hindernis links
            (self.snake_direction == UP and self.hindernis((self.snake_positions[0][0] + LEFT[0], self.snake_positions[0][1] + LEFT[1]))) or \
            (self.snake_direction == LEFT and self.hindernis((self.snake_positions[0][0] + DOWN[0], self.snake_positions[0][1] + DOWN[1]))) or \
            (self.snake_direction == DOWN and self.hindernis((self.snake_positions[0][0] + RIGHT[0], self.snake_positions[0][1] + RIGHT[1]))) or \
            (self.snake_direction == RIGHT and self.hindernis((self.snake_positions[0][0] + UP[0], self.snake_positions[0][1] + UP[1]))),
            # Hindernis geradeaus
            (self.snake_direction == UP and self.hindernis((self.snake_positions[0][0] + UP[0], self.snake_positions[0][1] + UP[1]))) or \
            (self.snake_direction == LEFT and self.hindernis((self.snake_positions[0][0] + LEFT[0], self.snake_positions[0][1] + LEFT[1]))) or \
            (self.snake_direction == DOWN and self.hindernis((self.snake_positions[0][0] + DOWN[0], self.snake_positions[0][1] + DOWN[1]))) or \
            (self.snake_direction == RIGHT and self.hindernis((self.snake_positions[0][0] + RIGHT[0], self.snake_positions[0][1] + RIGHT[1]))),
            # Hindernis rechts
            (self.snake_direction == UP and self.hindernis((self.snake_positions[0][0] + RIGHT[0], self.snake_positions[0][1] + RIGHT[1]))) or \
            (self.snake_direction == LEFT and self.hindernis((self.snake_positions[0][0] + UP[0], self.snake_positions[0][1] + UP[1]))) or \
            (self.snake_direction == DOWN and self.hindernis((self.snake_positions[0][0] + LEFT[0], self.snake_positions[0][1] + LEFT[1]))) or \
            (self.snake_direction == RIGHT and self.hindernis((self.snake_positions[0][0] + DOWN[0], self.snake_positions[0][1] + DOWN[1]))),
        ], dtype = int)

    # Spielzug
    def move(self, action):
        if action == 1:
            self.snake_positions.insert(0, (self.snake_positions[0][0] + self.snake_direction[0], self.snake_positions[0][1] + self.snake_direction[1]))
            return
        elif action == 0:
            if self.snake_direction == UP:
                self.snake_direction = RIGHT
            elif self.snake_direction == RIGHT:
                self.snake_direction = DOWN
            elif self.snake_direction == DOWN:
                self.snake_direction = LEFT
            elif self.snake_direction == LEFT:
                self.snake_direction = UP
            self.snake_positions.insert(0, (self.snake_positions[0][0] + self.snake_direction[0], self.snake_positions[0][1] + self.snake_direction[1]))
            return
        elif action == 2:
            if self.snake_direction == UP:
                self.snake_direction = LEFT
            elif self.snake_direction == LEFT:
                self.snake_direction = DOWN
            elif self.snake_direction == DOWN:
                self.snake_direction = RIGHT
            elif self.snake_direction == RIGHT:
                self.snake_direction = UP
            self.snake_positions.insert(0, (self.snake_positions[0][0] + self.snake_direction[0], self.snake_positions[0][1] + self.snake_direction[1]))
            return

    # Grafik zeichnen
    def draw(self):
        self.display.fill((1, 2, 20))
        for index, i in enumerate(self.snake_positions):
            pygame.draw.rect(self.display, (255, 255, 255), pygame.Rect((i[0] * 12 + 1, i[1] * 12 + 1), (10, 10)))
        #pygame.draw.rect(self.display, (205, 44, 62), pygame.Rect((self.food_position[0] * 12 + 1, self.food_position[1] * 12 + 1), (10, 10)))
        pygame.draw.rect(self.display, (0, 192, 255), pygame.Rect((self.food_position[0] * 12 + 1, self.food_position[1] * 12 + 1), (10, 10)))
        pygame.display.flip()
