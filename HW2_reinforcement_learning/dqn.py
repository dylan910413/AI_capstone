# dqn.py
import torch
import torch.nn as nn
import random
from collections import deque
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class DQN(nn.Module):
    def __init__(self, env_config):
        super().__init__()
        self.env_config = env_config
        self.conv = nn.Sequential(
            nn.Conv2d(4, 32, 8, 4),
            nn.ReLU(),
            nn.Conv2d(32, 64, 4, 2),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, 1),
            nn.ReLU()
        )
        self.fc = nn.Sequential(
            nn.Linear(7 * 7 * 64, 512),
            nn.ReLU(),
            nn.Linear(512, env_config["n_actions"])
        )
        self.epsilon = env_config["epsilon_start"]

    def forward(self, x):
        x = x / 255.0
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)

    def act(self, state):
        if random.random() < self.epsilon:
            return torch.tensor(random.randint(0, self.env_config["n_actions"] - 1), device=device)
        with torch.no_grad():
            return self.forward(state).max(1)[1]

class ReplayMemory:
    def __init__(self, capacity):
        self.memory = deque(maxlen=capacity)

    def push(self, state, action, next_state, reward):
        self.memory.append((state, action, next_state, reward))

    def sample(self, batch_size):
        batch = random.sample(self.memory, batch_size)
        state, action, next_state, reward = map(torch.cat, zip(*batch))
        return state, action, next_state, reward

    def __len__(self):
        return len(self.memory)

def optimize(dqn, dqn_target, memory, optimizer, env_config):
    if len(memory) < env_config["batch_size"]:
        return

    state, action, next_state, reward = memory.sample(env_config["batch_size"])

    q_values = dqn(state).gather(1, action.unsqueeze(1)).squeeze()
    with torch.no_grad():
        max_next_q_values = dqn_target(next_state).max(1)[0]
        target_q_values = reward + env_config["gamma"] * max_next_q_values

    loss = nn.MSELoss()(q_values, target_q_values)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
