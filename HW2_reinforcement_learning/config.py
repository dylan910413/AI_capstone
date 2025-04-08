# config.py

CartPole = {
    "env_name": "cartpole",
    "n_actions": 2,
    "gamma": 0.99,
    "lr": 1e-3,
    "epsilon_start": 1.0,
    "epsilon_final": 0.01,
    "epsilon_decay": 500,
    "n_episodes": 500,
    "memory_size": 10000,
    "batch_size": 64,
    "train_frequency": 1,
    "target_update_frequency": 100,
}

Pong = {
    "env_name": "pong",
    "n_actions": 3,  # mapped to real Pong actions
    "gamma": 0.99,
    "lr": 1e-4,
    "epsilon_start": 1.0,
    "epsilon_final": 0.05,
    "epsilon_decay": 10000,
    "n_episodes": 1000,
    "memory_size": 100000,
    "batch_size": 32,
    "train_frequency": 4,
    "target_update_frequency": 1000,
}
