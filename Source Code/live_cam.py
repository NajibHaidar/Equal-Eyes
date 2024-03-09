"""
Camera Feed Display Script (for debugging)

This script is designed to test and demonstrate how to display live video feed from the default camera device using OpenCV.
It continuously captures frames from the camera and displays them in a window. The script checks if the camera is 
opened correctly and handles the case where frames cannot be captured. The live video feed is displayed in a window 
titled 'Live Video Feed', and the script exits when the user presses the 'q' key.

Requirements:
- OpenCV library installed.
- Access to a default camera device.

Usage:
- Run the script in an environment where OpenCV is installed and a camera is available.
- Press 'q' to quit the script and close the video feed window.
"""

import cv2  # Import the OpenCV library

# Initialize the video capture object to capture video from the default camera
cap = cv2.VideoCapture(0)  # 0 typically refers to the default camera

# Verify that the camera was successfully opened
if not cap.isOpened():
    raise IOError("Cannot open webcam")  # Raise an error if the camera cannot be opened

# Continuously capture and display frames from the camera
while True:
    ret, frame = cap.read()  # Read the current frame
    if not ret:
        print("Failed to grab frame")  # Print an error message if the frame cannot be captured
        break  # Exit the loop if no frame is captured

    # Display the captured frame in a window named 'Live Video Feed'
    cv2.imshow('Live Video Feed', frame)

    # Exit the loop and close the video feed when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
