import numpy as np
import gym
from gym import spaces
import pygame
import random

class AfloatCylinderEnv(gym.Env):
    def __init__(self):
        super(AfloatCylinderEnv, self).__init__()

        # Action space: 0 - Do nothing, 1 - Move forward, 2 - Move backward
        self.action_space = spaces.Discrete(3)

        # Observation space: (x, y, z) position of the cylinder
        self.observation_space = spaces.Box(low=np.array([-10, 0, -10]), high=np.array([10, 10, 10]))

        # Initialize cylinder's position and forces
        self.cylinder_position = np.array([0.0, 0.0, 0.0])
        self.buoyancy = np.array([0.0, 1.0, 0.0])  # Upward buoyant force
        self.velocity = np.array([0.0, 0.0, 0.0])

        # List to store obstacle positions
        self.obstacles = []

        # Set up Pygame for visualization (optional)
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))

    def _apply_buoyancy(self):
        self.velocity += self.buoyancy

    def _generate_obstacle(self):
        # Generate a random obstacle and add it to the obstacles list
        obstacle = {
            "x": random.uniform(-9, 9),
            "y": 0.5,  # Fixed y position above the water surface
            "z": random.uniform(self.cylinder_position[2] + 5, self.cylinder_position[2] + 10)
        }
        self.obstacles.append(obstacle)

    def step(self, action):
        # Generate a new obstacle with a certain probability
        if random.random() < 0.1:
            self._generate_obstacle()

        if action == 1:  # Move forward
            self.velocity[2] = 1.0
        elif action == 2:  # Move backward
            self.velocity[2] = -1.0
        else:  # Do nothing
            self.velocity[2] = 0.0

        # Update the position based on velocity
        self.cylinder_position += self.velocity

        # Check for collisions with obstacles
        for obstacle in self.obstacles:
            if abs(self.cylinder_position[0] - obstacle["x"]) < 1.0 and abs(self.cylinder_position[2] - obstacle["z"]) < 1.0:
                # Collision occurred; reset the environment
                self.reset()
                break

        # Apply buoyancy
        self._apply_buoyancy()

        # Create the observation
        observation = self.cylinder_position

        # Define a simple reward function (e.g., maximize height)
        reward = self.cylinder_position[1]

        # Check if the episode is done (for this basic example, it's never done)
        done = False

        return observation, reward, done, {}

    def reset(self):
        # Reset the environment
        self.cylinder_position = np.array([0.0, 0.0, 0.0])
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.obstacles = []  # Clear obstacles
        return self.cylinder_position

    def render(self):
        # Render the environment (optional)
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(300, 400, 200, 10))  # Water surface
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(int(obstacle["x"] * 20 + 400), 200, 20, 200))  # Obstacle
        pygame.draw.circle(self.screen, (0, 255, 0), (int(self.cylinder_position[0] * 20 + 400), int(self.cylinder_position[2] * 20 + 300)), 10)  # Cylinder
        pygame.display.flip()

    def close(self):
        pygame.quit()

def run():
    env = AfloatCylinderEnv()
    for episode in range(10):
        observation = env.reset()
        for t in range(1000):
            env.render()
            action = env.action_space.sample()  # Replace with your agent's action
            observation, reward, done, info = env.step(action)
            if done:
                print("Episode {} finished after {} timesteps".format(episode, t + 1))
                break
    env.close()
