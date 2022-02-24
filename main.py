##########IMPORT##########
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

import random, datetime
from pathlib import Path
import matplotlib.pyplot as plt

from environment import Game
from agent import Agent

##########GLOBALS##########
X = 21
Y = 21
SPEED = 20

##########INIT##########
env = Game(X, Y, SPEED)

save_dir = Path('trainingsdaten') / datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
save_dir.mkdir(parents=True)
checkpoint = None

snake = Agent(state_dim=11, action_dim=3, save_dir=save_dir, checkpoint=checkpoint)

episodes = 1000
scores = []

##########GRAPH##########
plt.ion()

def plot(scores):
    plt.clf()
    plt.xlabel('Spiele')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.show()
    plt.pause(.1)

##########LOOP##########
for e in range(episodes):

    env.reset()

    while True:
        state = env.perceive()
        action = snake.act(state)
        reward, done, info = env.play(action)
        next_state = env.perceive()
        snake.cache(state, next_state, action, reward, done)

        if done:
            snake.learn()
            scores.append(info)
            plot(scores)
            break
