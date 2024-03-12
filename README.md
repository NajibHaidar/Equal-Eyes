# Equal Eyes
#### Embedded Systems Capstone project. Run on Raspberry Pi 4B and STM32F as required. 
#### Group of 5 students: Najib Haidar, Jonathan Birchman, Eric Eng, Adam Klein, Gavin Bullock.
#### Najib Haidar wrote the source code you see here. Parts were done in paired programming with Jonathan Birchman and Eric Eng.

## Demo Video
# [View the Demo Video](https://drive.google.com/file/d/1N5RvK88AtiRNaVfF_4NZJ8ooWWDmi8Y3/view?usp=sharing)


## Overview
Equal Eyes is an innovative solution designed to assist visually impaired individuals in becoming more acquainted with their surroundings through audio output. Utilizing an embedded camera for visual input, this project leverages state-of-the-art technologies in image processing, object detection, image classification, and text detection. By converting visual stimuli into descriptive audio feedback, Equal Eyes aims to enhance the spatial awareness and daily life navigation of individuals with visual impairments.

## Features
- **Gemini Assistant**: A specialized mode that provides a general description of the scene using Gemini model capabilities.
- **Object Detection**: Identifies and describes objects in the camera's field of view (modified to detect person, chair, keyboard, and mouse).
- **Text Detection**: Recognizes and reads out text found within the image.
- **Image Classification**: (Not currently suppported with glasses, used as idle state in demo)

## Installation

### Prerequisites
- A Linux-based system with camera support (Raspberry Pi 4B).
- Python 3.9 installed.
- Access to a serially connected device configured for button inputs (STM32F).

### Dependencies
Install the required Python packages:
```bash
pip install opencv-python pytesseract serial subprocess
```
**Note:** Some features might require the installation of additional software or libraries, such as `pico2wave` for speech synthesis and ALSA utilities (`aplay`) for audio playback.

### Setup
1. Clone the Equal Eyes repository:
   ```bash
   git clone https://github.com/NajibHaidar/Equal-Eyes/
   ```
2. Navigate to the cloned directory:
   ```bash
   cd Equal-Eyes
   ```
3. Install any additional dependencies as required by the specific modules you intend to use.

## Usage
To start Equal Eyes, run the main script from the terminal:
```bash
python main.py
```
Interact with the system using the connected device's buttons to switch between modes and trigger actions.

## Configuration
- **Serial Port Configuration**: Modify `main.py` to specify the correct serial port and baud rate for your device.
- **Mode Selection**: Use the physical buttons connected through the serial port to switch between different operational modes.

## Acknowledgments
Equal Eyes integrates various open-source tools and libraries, including OpenCV for image processing, PyTesseract for OCR capabilities, and Google's Gemini Chatbot. Special thanks to the developers and contributors of these projects for their valuable work.
