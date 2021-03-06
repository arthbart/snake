##########IMPORT##########
from torch import nn
import copy

##########NETZWERK##########
class SnakeNet(nn.Module):

    def __init__(self, input_dim, output_dim):
        super().__init__()

        self.online = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.ReLU(),
            nn.Linear(512, output_dim)
        )

        self.target = copy.deepcopy(self.online)

        for p in self.target.parameters():
            p.requires_grad = False

    def forward(self, input, model):
        if model == 'online':
            return self.online(input)
        elif model == 'target':
            return self.target(input)
