"""
Text Detection Script

This script captures images using a camera, checks for blur, performs Optical Character Recognition (OCR) using PyTesseract 
on clear images, and uses Text-To-Speech (TTS) to read out the OCR results. It's designed for applications that require 
real-time image capture and processing, with auditory feedback for the results. This script can be particularly useful in 
assistive technologies or automated systems needing visual text recognition and vocal feedback.

The script checks if captured images are blurry using the Laplacian variance method and only proceeds with OCR on sharp images. 
Blurry images prompt the user to retake the photo. The OCR results are saved to a text file and read aloud.

Requirements:
- OpenCV (cv2) for image capture and processing.
- PyTesseract for OCR.
- A custom TTS module for Text-To-Speech functionality.
- A camera connected to the device running the script.

Usage:
- Ensure PyTesseract and OpenCV are properly installed and configured.
- The TTS module should be capable of asynchronous speech operations.
- The script uses a queue system for managing capture commands, allowing integration into larger systems.
"""

import cv2
import pytesseract
import TTS
import time

def check_blur(image):
    """Check if the captured image is blurry using Laplacian variance."""
    threshold = 100  # Variance threshold for determining blur

    # Convert image to grayscale for processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('gray_img.jpg', gray)  # Optional: Save the grayscale image for review

    # Calculate Laplacian variance
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    print(laplacian_var)  # Debug: Print the Laplacian variance
    
    # Determine if the image is blurry
    blurry = laplacian_var < threshold
    if blurry:
        print("The image is blurry.")
    else:
        print("The image is sharp.")
    return laplacian_var, blurry
    
def process_image(frame):
    """Process the captured image for OCR and TTS feedback."""
    cv2.imwrite('captured_image.jpg', frame)  # Save the captured frame
    laplacian_variance, blurry = check_blur(frame)
    print("Laplacian Variance:", laplacian_variance)
    
    if blurry:
        TTS.speak_async('Image is blurry, press button 2 to retake it.')
    else:
        # Perform OCR on the sharp image
        text = pytesseract.image_to_string(frame)
        with open('text_result.txt', 'w') as file:  # Save OCR results
            file.write(text)
        TTS.speak_async(text)  # Read the OCR results aloud

    return blurry

def run_text(queue):
    """Main loop to capture images and process them based on queue commands."""
    cap = None
    while True:
        try:
            if not cap:
                cap = cv2.VideoCapture(0)  # Initialize the default camera
            
            take_picture = queue.get(timeout=1)  # Wait for a command to capture an image
            print(take_picture)

            if take_picture:
                print("image captured")
                ret, frame = cap.read()  # Capture a frame
                TTS.speak_async('Image captured. Analyzing...')
                blurry = process_image(frame)  # Process the captured image
                
                if not blurry:
                    TTS.speak_async('Text to speech complete.')
                    TTS.speak_async('Press button 2 to capture another image')
        except BaseException as e:  # Handle unexpected errors
            print(f"Unexpected error: {e}")
            continue
