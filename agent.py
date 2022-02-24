##########IMPORT##########
import torch
import random, numpy as np
from pathlib import Path
from collections import deque

from network import SnakeNet

##########AGENT##########
class Agent:

    def __init__(self, state_dim, action_dim, save_dir, checkpoint = None):
        self.state_dim = state_dim # Dimension Eingaben
        self.action_dim = action_dim # Dimension Ausgaben
        self.memory = deque(maxlen=100000) # Speicher für Wahrnehmungen, Aktionen, Belohnungen
        self.batch_size = 1000 # Anzahl der pro Lernvorgang verwendeten Erinnerungen

        self.exploration_rate = 0.5 # Anfängliches Verhältnis Problem-Generator zu Ausführendem Part
        self.exploration_rate_decay = 0.99975 # Pro Durchlauf * x weniger Problem-Generator
        self.exploration_rate_min = 0 # Minimaler Anteil Problem-Generator
        self.gamma = 0.9 # Unterschied Momentan zu Ziel beim Training

        self.curr_step = 0 # Schrittzähler
        self.burnin = 1e3 # Für die ersten x Runden nicht lernen
        self.learn_every = 1 # Jeden x Schritt lernen
        self.sync_every = 1 # Ziel nach jedem x Schritt aktualisieren

        self.save_every = 5e5 # Netz nach jedem x Schritt speichern
        self.save_dir = save_dir # Speicherort Netz

        self.use_cuda = torch.cuda.is_available() # Grafikkarte verwenden

        # init Netzwerk
        self.net = SnakeNet(self.state_dim, self.action_dim).float()
        if self.use_cuda:
            self.net = self.net.to(device='cuda')
        if checkpoint:
            self.load(checkpoint)

        self.optimizer = torch.optim.Adam(self.net.parameters(), lr=0.001)
        self.loss_fn = torch.nn.SmoothL1Loss()

    # Aktion
    def act(self, state):
        # Problem-Generator
        if np.random.rand() < self.exploration_rate:
            action_idx = np.random.randint(self.action_dim)
        # Ausführender Part
        else:
            state = torch.FloatTensor(state).cuda() if self.use_cuda else torch.FloatTensor(state)
            state = state.unsqueeze(0)
            action_values = self.net(state, model='online')
            action_idx = torch.argmax(action_values, axis=1).item()

        self.exploration_rate *= self.exploration_rate_decay
        self.exploration_rate = max(self.exploration_rate_min, self.exploration_rate)

        self.curr_step += 1
        return action_idx

    # Speichern
    def cache(self, state, next_state, action, reward, done):
        state = torch.FloatTensor(state).cuda() if self.use_cuda else torch.FloatTensor(state)
        next_state = torch.FloatTensor(next_state).cuda() if self.use_cuda else torch.FloatTensor(next_state)
        action = torch.LongTensor([action]).cuda() if self.use_cuda else torch.LongTensor([action])
        reward = torch.DoubleTensor([reward]).cuda() if self.use_cuda else torch.DoubleTensor([reward])
        done = torch.BoolTensor([done]).cuda() if self.use_cuda else torch.BoolTensor([done])

        self.memory.append((state, next_state, action, reward, done,))

    # Gespeichertes fürs Lernen abrufen
    def recall(self):
        batch = random.sample(self.memory, self.batch_size)
        state, next_state, action, reward, done = map(torch.stack, zip(*batch))
        return state, next_state, action.squeeze(), reward.squeeze(), done.squeeze()

    # Netz momentan
    def td_estimate(self, state, action):
        current_Q = self.net(state, model='online')[np.arange(0, self.batch_size), action]
        return current_Q

    @torch.no_grad() # Gradientenrechner ausschalten für bessere Performance
    # Netz Ziel
    def td_target(self, reward, next_state, done):
        next_state_Q = self.net(next_state, model='online')
        best_action = torch.argmax(next_state_Q, axis=1)
        next_Q = self.net(next_state, model='target')[np.arange(0, self.batch_size), best_action]
        return (reward + (1 - done.float()) * self.gamma * next_Q).float()

    # Gewichte aktualisieren
    def update_Q_online(self, td_estimate, td_target):
        loss = self.loss_fn(td_estimate, td_target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return loss.item()

    # Gewichte gleichsetzen Ziel
    def sync_Q_target(self):
        self.net.target.load_state_dict(self.net.online.state_dict())

    # Lernen
    def learn(self):
        if self.curr_step % self.sync_every == 0:
            self.sync_Q_target()

        if self.curr_step % self.save_every == 0:
            self.save()

        if self.curr_step < self.burnin:
            return None, None

        if self.curr_step % self.learn_every != 0:
            return None, None

        state, next_state, action, reward, done = self.recall()
        td_est = self.td_estimate(state, action)
        td_tgt = self.td_target(reward, next_state, done)
        loss = self.update_Q_online(td_est, td_tgt)

        return (td_est.mean().item(), loss)

    # Netz speichern
    def save(self):
        save_path = self.save_dir / f"snake_net_{int(self.curr_step // self.save_every)}.chkpt"
        torch.save(
            dict(
                model = self.net.state_dict(),
                exploration_rate = self.exploration_rate
            ),
            save_path
        )
        print(f"Netz gespeichert unter {save_path} an Schritt {self.curr_step}.")

    # Netz laden
    def load(self, load_path):
        if not load_path.exists():
            raise ValueError(f"{load_path} existiert nicht!")

        ckp = torch.load(load_path, map_location=('cuda' if self.use_cuda else 'cpu'))
        exploration_rate = ckp.get('exploration_rate')
        state_dict = ckp.get('model')

        print(f"Netz von {load_path} mit exploration_rate {exploration_rate} laden.")
        self.net.load_state_dict(state_dict)
        self.exploration_rate = exploration_rate
