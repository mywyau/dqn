# Pathfinding

So as a background to the project, this app uses PyGame to simulate a car/model. 
This car/model then traverses an environment littered with obstacles.

The goal is to explore the entirety of the environment space whilst avoiding all the obstacles.

This repo tests the application of the Reinforcement Learning algorithm Dqn.

The deep Q-network (DQN) algorithm is a model-free, online, off-policy reinforcement learning method. A DQN agent is a value-based reinforcement learning agent that trains a critic to estimate the expected discounted cumulative long-term reward when following the optimal policy.

See below for more details about DQN

## To install the dependencies

After activating your venv using a command like:

```
source venv/bin/activate
```

### run:

```
pip install -r requirements.txt
```

## src/michael_version/ - run the following
Running the project like from base commands
```
python3 train_dqn.py                
```

### To test Reinforcement Learning model

```
python3 test_dqn.py                
```

### Unit tests

```
python -m unittest discover -s tests
```

Or just run the convenience scripts since you need to set the PYTHONPATH etc.

```
./run_tests.sh
```

### To train the model

```
./run_train_model.sh
```

### After training once model has been created, test in a pygame simulation

```
./run_test_model.sh
```


## Advantages of DQN:
### Scalability:

- DQN can handle large and complex state spaces that would be infeasible for traditional Q-learning. By using deep neural networks, DQN can approximate the Q-value function for high-dimensional inputs, such as images.
Automated Feature Extraction:

- DQN eliminates the need for manual feature engineering by using deep learning, which automatically extracts relevant features from raw input data. This is particularly useful for tasks like playing video games, where the input is often raw pixel data.
Off-policy Learning:

- DQN is an off-policy algorithm, meaning it can learn from stored experiences (replay buffer) rather than requiring fresh interactions with the environment for every update. This makes the learning process more efficient and stable.
Experience Replay:

- Experience replay in DQN allows the algorithm to reuse past experiences, breaking the temporal correlations between consecutive experiences. This helps stabilize training and reduces the variance of updates.
Target Network:

- DQN uses a target network to stabilize training by reducing the likelihood of harmful feedback loops that can occur when both the current and target Q-values are updated based on each other.
Proven Success:

- DQN has been successfully applied to a wide range of tasks, most notably in playing Atari games at a level comparable to humans.

## Disadvantages of DQN:
### Sample Inefficiency:

- DQN requires a large number of interactions with the environment to learn effectively, making it sample-inefficient. This is particularly problematic in real-world applications where gathering data is expensive or time-consuming.
Stability and Convergence Issues:

- Despite the use of target networks and experience replay, DQN can still suffer from instability during training. Hyperparameters like learning rate, discount factor, and the frequency of target network updates need careful tuning.
Slow Learning:

- DQN's reliance on neural networks means that each update can be computationally expensive, leading to slower learning compared to simpler algorithms like tabular Q-learning.
Limited to Discrete Action Spaces:

- DQN is primarily designed for environments with discrete action spaces. For continuous action spaces, variations like Deep Deterministic Policy Gradient (DDPG) are required, which are more complex to implement and tune.
Difficulty in Handling Sparse Rewards:

- In environments where rewards are sparse or delayed, DQN may struggle to learn effectively. This is because the agent receives little feedback on its actions, making it harder to propagate useful signals back to earlier states.
Exploration Challenges:

- DQN relies on epsilon-greedy exploration, which can be inefficient in complex environments where random exploration is unlikely to discover useful states. More advanced exploration strategies are sometimes needed, adding complexity.
Overestimation Bias:

- DQN can suffer from overestimation bias, where it consistently overestimates Q-values. While techniques like Double DQN (DDQN) mitigate this, it is an issue that requires additional modifications to the basic DQN algorithm.
