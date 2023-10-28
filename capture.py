import cv2
from utils.constants import *



def obstacle_detection(frame):
    # Preprocess the frame if needed
    # For example, convert it to grayscale and apply filters

    # Detect obstacles in the frame
    # You can use techniques like edge detection, contour detection, or deep learning-based object detection
    # Here, we'll use a simple example with contour detection

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to create a binary image
    ret, thresh = cv2.threshold(gray, 127, 255, 0)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    obstacle_coordinates = []

    # Filter out small contours (noise) and get the coordinates of detected obstacles
    for contour in contours:
        if cv2.contourArea(contour) > min_obstacle_area:
            x, y, w, h = cv2.boundingRect(contour)
            obstacle_coordinates.append((x, y, x + w, y + h))

    return obstacle_coordinates

# Example usage
    # Open a video capture stream or load an image
def captures():
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        obstacle_coordinates = obstacle_detection(frame)
        print("Obstacle Coordinates:", obstacle_coordinates)

    cap.release()
    cv2.destroyAllWindows()
