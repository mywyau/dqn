import random
from collections import deque
import torch
import torch.nn as nn
import torch.optim as optim
from noisy_linear import NoisyLinear  # Ensure this is your custom NoisyLinear class

class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = NoisyLinear(state_size, 64)
        self.fc2 = NoisyLinear(64, 64)
        self.fc3 = NoisyLinear(64, action_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

    def reset_noise(self):
        self.fc1.reset_noise()
        self.fc2.reset_noise()
        self.fc3.reset_noise()

class DQNAgent:
    def __init__(self, state_size, action_size, epsilon=1.0, epsilon_min=0.05, epsilon_decay=0.9995):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # discount rate
        self.learning_rate = 0.001
        self.batch_size = 32
        self.train_start = 1000
        self.epsilon = epsilon  # Initial epsilon value for epsilon-greedy
        self.epsilon_min = epsilon_min  # Minimum epsilon value
        self.epsilon_decay = epsilon_decay  # Decay rate for epsilon

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = DQN(state_size, action_size).to(self.device)
        self.target_model = DQN(state_size, action_size).to(self.device)
        self.update_target_model()

        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()

    def update_target_model(self):
        self.target_model.load_state_dict(self.model.state_dict())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if random.random() <= self.epsilon:  # Epsilon-greedy decision
            return random.randrange(self.action_size)  # Random action
        else:
            state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            self.model.reset_noise()  # Reset noise before choosing an action
            with torch.no_grad():  # Disable gradient calculation
                act_values = self.model(state)
            return torch.argmax(act_values[0]).item()

    def replay(self):
        if len(self.memory) < self.train_start:
            return

        minibatch = random.sample(self.memory, min(len(self.memory), self.batch_size))

        for state, action, reward, next_state, done in minibatch:
            state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            next_state = torch.FloatTensor(next_state).unsqueeze(0).to(self.device)

            target = self.model(state).detach()
            if done:
                target[0][action] = reward
            else:
                t = self.target_model(next_state).detach()
                target[0][action] = reward + self.gamma * torch.max(t[0])

            output = self.model(state)
            loss = self.criterion(output, target)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        self.model.reset_noise()  # Reset noise after each training step

        # Decay epsilon to reduce the probability of random actions over time
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_state_dict(torch.load(name))

    def save(self, name):
        torch.save(self.model.state_dict(), name)
