import sys
from train_dqn import train_dqn
from test_dqn import test_dqn

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [train|test]")
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "train":
        train_dqn(1000)  # Train for 1000 episodes
    elif mode == "test":
        test_dqn()  # Test the trained model
    else:
        print("Invalid mode. Choose 'train' or 'test'.")
        sys.exit(1)
