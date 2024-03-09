"""
Gemini Script

This script utilizes computer vision and generative AI technologies to capture images using the default camera, 
analyze them, and verbally describe the contents of the images. It leverages OpenCV for image capture, PIL for 
image processing, and Google's generative AI model (Gemini Pro Vision) for generating descriptive text of the images. 
Text-to-Speech (TTS) functionality is used to provide an auditory response to the image analysis, making it 
accessible for visually impaired users or for applications requiring audio feedback. The script supports continuous 
image capture and analysis through a command queue system, allowing for dynamic interaction based on user input or 
automated triggers.

Requirements:
- An environment variable `GOOGLE_API_KEY` set with a valid Google API key for accessing generative AI models.
- A `.env` file in the root directory containing the Google API key, if not set as a system-wide environment variable.
- The script is designed to run continuously, processing commands to capture and describe images as they come.

Usage:
- The script is intended to be integrated into a larger application that can provide commands through a queue.
- Direct execution will require manual intervention to simulate queue inputs for capturing images.
"""

# Import necessary libraries
import TTS
import cv2
import google.generativeai as genai
import os 
import PIL.Image
from dotenv import load_dotenv 

# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')  # Retrieve Google API key from environment variables

# Configure the Google generative AI model with the API key
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the GenerativeModel with a specified model name
model = genai.GenerativeModel('gemini-pro-vision')  #multimodal model capable of understanding and generating content based on images

def capture_image():
  """Captures an image using the default camera, processes it, and uses TTS to describe the image."""
  # Initialize the camera
  cap = cv2.VideoCapture(0)  # 0 is the default camera

  # Capture a single frame
  success, image = cap.read()

  if success:
      # Save the captured image to a file
      cv2.imwrite('captured_image.jpg', image)
      img = PIL.Image.open('captured_image.jpg')
      # Inform the user that the image is being analyzed
      TTS.speak_async('Image captured. Analyzing...')
      # Use the model to generate a description of the image
      response = model.generate_content(['Describe the image as you would to a blind person.', img])
      # Speak out the generated description
      TTS.speak_async(response.text)
      print(response.text)
  else:
      # Inform the user if image capture failed
      TTS.speak_async('Failed to capture image')

  # Release the camera
  cap.release()

def run_gemini(queue):
    """Continuously checks the queue from process in main.py for commands to capture and describe images."""
    while True:
        try:
            # Wait for a command to take a picture
            take_picture = queue.get(timeout=1)  # Adjust the timeout as necessary
            print(take_picture)

            if take_picture:
                # Capture and process the image
                capture_image()
                # Inform the user to press a button to capture another image
                TTS.speak_async('Press button 2 to capture image')
        except Exception as e:  # Catch all other exceptions
            print(f"Unexpected error: {e}")
            continue
