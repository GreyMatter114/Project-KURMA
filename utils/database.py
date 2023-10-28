import json

# Define the path to the JSON file created by Octave
json_file_path = "data.json"

try:
    # Open and read the JSON file
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

        # Check if the JSON data contains obstacle information
        if "obstacles" in data:
            obstacle_data = data["obstacles"]

            # Process obstacle data
            for obstacle in obstacle_data:
                if "x" in obstacle and "y" in obstacle and "z" in obstacle:
                    x_coord = obstacle["x"]
                    y_coord = obstacle["y"]
                    z_coord = obstacle["z"]

                    # Process or use the obstacle coordinates
                    print(f"Obstacle: X = {x_coord}, Y = {y_coord}, Z = {z_coord}")
                else:
                    print("Invalid obstacle data format. Missing coordinates.")

        else:
            print("No obstacle data found in the JSON file.")

except FileNotFoundError:
    print(f"JSON file '{json_file_path}' not found.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON data: {str(e)}")
