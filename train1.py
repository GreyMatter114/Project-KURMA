import neat
import pickle
from utils.simulation import *  # Import your Gym environment
from infra import Robot  # Import your robot class
from capture import captures  # Import your captures function
from utils.constants import *
# Set up NEAT configuration
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, 'config.txt')

# Create the Gym environment
env = AfloatCylinderEnv()  # Initialize your Gym environment

# Create the population
p = neat.Population(config)

# Define the fitness function
def fitness_function(robot,robot_position):
    initial_position = robot_position  # Capture the initial position
    total_distance = 0  # Initialize the total distance traveled

    for _ in range(num_generations):
        # Capture a frame from the camera and update the robot's position
        obstacle_info = captures()
        robot_position = robot.move(obstacle_info)

        # Calculate the distance traveled in this step and add it to the total distance
        step_distance = abs(robot_position - initial_position)  # Assuming linear movement
        total_distance += step_distance

        # Update the initial position for the next step
        initial_position = robot_position

    return total_distance


# Run NEAT evolution
def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        robot = Robot()  # Create a robot object for each agent
        genome.fitness = 0  # Initialize fitness

        # Implement training and obstacle avoidance logic
        for _ in range(num_generations):
             # Capture a frame from the camera
            obstacle_info = captures()
            robot_position = robot.move(obstacle_info)
            genome.fitness += fitness_function(robot,robot_position)

# Main NEAT evolution loop
def main():
    winner = p.run(eval_genomes)
    with open('kurma_model.pkl', 'wb+') as output:
        pickle.dump(winner, output)

    # Optional: Implement robot control logic using the winning genome to test and visualize the trained robot.
    observation = env.reset()
    robot = Robot()  # Initialize your robot
    for _ in range(env.max_episode_steps):
        action = winner.compute_action(observation)
        observation, _, done, _ = env.step(action)
        if done:
            break

if __name__ == "__main__":
    main()
