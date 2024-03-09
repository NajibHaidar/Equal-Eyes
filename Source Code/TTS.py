"""
Asynchronous Text-To-Speech Script

This script converts text into speech asynchronously, leveraging the `pico2wave` tool for speech synthesis 
and `aplay` for audio playback on Linux-based systems. It creates a temporary WAV file containing the 
generated speech from the input text, plays the audio file, and then cleans up by deleting the temporary file. 
This is suitable for applications requiring background speech operations without blocking the main program execution.

Requirements:
- `pico2wave` installed for speech synthesis.
- `aplay` (part of the ALSA project) for playing audio files.
- Linux-based operating system.

Usage:
- Call `speak_async(text)` with the desired text string to be spoken.
"""

import subprocess
import tempfile
import os

def speak_async(text):
    """
    Generates and plays speech from text asynchronously.
    
    Args:
        text (str): Text to convert to speech.
    """
    # Create a temporary file to hold the speech audio
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmpfile:
        tmp_filename = tmpfile.name  # Store the name of the temporary file

    # Use pico2wave to generate speech from text and save it to the temporary file
    subprocess.run(['pico2wave', '--wave=' + tmp_filename, text])
    
    # Play the generated speech audio file
    subprocess.run(['aplay', tmp_filename])
    
    # Clean up by removing the temporary file after playback
    os.remove(tmp_filename)
