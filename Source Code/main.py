"""
Main Control Script for Equal Eyes

This script orchestrates the operation of Equal Eyes, switching between different modes of operation including 
object detection, image classification, text detection, and assistant functionalities based on physical button inputs. It 
utilizes subprocesses to manage the execution of separate scripts for each feature, allowing for asynchronous operation and 
real-time user interaction through a serially connected input device. Each feature is designed to run in its own process, 
which can be dynamically started or stopped based on user input, facilitating a versatile and interactive user experience.

The script communicates with external hardware via a serial port, listening for button press events to switch modes or 
trigger actions within the current mode. It also integrates text-to-speech feedback to inform the user of the current state 
or actions being performed, enhancing the application's accessibility and ease of use.

Requirements:
- Python 3.9 (had library versioning issues on RaspPi 4B above Python 3.9)
- External libraries: PySerial for serial communication, subprocess for process management, and any other libraries required by the feature scripts.
- External scripts: detect.py, classify.py, gemini.py, text.py corresponding to the application's features.
- A serially connected device configured to send specific commands for mode switching and action triggering.
- Properly configured environment for running TTS, OpenCV, and any other required technologies.
"""

import serial
import subprocess
import TTS  # Assuming this is a custom or third-party library for text-to-speech functionality

# Paths to the Python scripts for different features
detect_script = 'detect.py'
classify_script = 'classify.py'
gemini_script = 'gemini.py'
text_script = 'text.py'

# Function to run a script in a subprocess and return the process object
def run_script(script):
    """
    Executes a given script in a separate subprocess.

    Args:
        script (str): The path to the script to be executed.

    Returns:
        subprocess.Popen: The subprocess object for the executed script.
    """
    return subprocess.Popen(['python', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Initialize control variables to manage the application state and modes
button_press = False  # Flag to detect button press
current_mode = 0  # Current mode of operation
feature_count = 4  # Total number of features or modes available
kill_everything = False  # Flag to signal application shutdown
target = 'gemini_worker'  # Current target worker, if applicable

# Setup serial port for listening to button press events
serialPort = '/dev/ttyS0'  # Serial port to use
baudRate = 9600  # Baud rate for serial communication
ser = serial.Serial(serialPort, baudRate, timeout=0.1)  # Serial port object

# Import multiprocessing essentials for managing separate worker processes for features
from multiprocessing import Process, Queue
from gemini import run_gemini as gemini_worker
from text import run_text as text_worker

# Initialize queues and processes for multiprocessing
q1 = Queue()  # Queue for gemini_worker process communication
p1 = Process(target=gemini_worker, args=(q1,))  # Process for gemini_worker

q2 = Queue()  # Queue for text_worker process communication
p2 = Process(target=text_worker, args=(q2,))  # Process for text_worker

def check_serial_input():
    """
    Checks the serial input for button press commands and handles mode switching,
    process management, and application termination based on the received commands.
    """
    global button_press, current_mode, feature_count, kill_everything, target, q1, p1, q2, p2

    # Check if there's incoming data on the serial port
    if ser.inWaiting() > 0:
        data = ser.readline().decode().strip()  # Read and decode the incoming data

        # Handle "Button 1" press: Mode change
        if data == "Button 1":
            button_press = True  # Set flag to indicate button press
            if button_press:
                button_press = False  # Reset button press flag
                current_mode += 1  # Increment the current mode
                current_mode %= feature_count  # Ensure current_mode wraps around feature_count
                print(f"Mode changed to {current_mode}")  # Log mode change
                
                # Terminate and clean up the gemini_worker process if it's running
                if p1 is not None and p1.is_alive():
                    p1.terminate()
                    p1.join()  # Ensure the process is properly cleaned up
                    print('p1 was terminated')
                    # Reinitialize the process and its communication queue
                    q1 = Queue()
                    p1 = Process(target=gemini_worker, args=(q1,))
                
                # Terminate and clean up the text_worker process if it's running
                if p2 is not None and p2.is_alive():
                    p2.terminate()
                    p2.join()  # Ensure the process is properly cleaned up
                    print('p2 was terminated')
                    # Reinitialize the process and its communication queue
                    q2 = Queue()
                    p2 = Process(target=text_worker, args=(q2,))

        # Handle "Button 2" press: Activate current mode's function
        elif data == "Button 2":
            # For gemini_worker mode
            if current_mode == 2:
                # Start the gemini_worker process if it's not already running
                if p1 and not p1.is_alive():
                    p1.start()
                # Send a signal to the gemini_worker process to activate its functionality
                q1.put(1)

            # For text_worker mode
            elif current_mode == 0:
                # Start the text_worker process if it's not already running
                if p2 and not p2.is_alive():
                    p2.start()
                # Send a signal to the text_worker process to activate its functionality
                q2.put(1)
                
        # Handle "Button 3" press: Terminate all processes and close the application
        elif data == "Button 3":
            kill_everything = True  # Set flag to indicate application should terminate
            # Terminate gemini_worker process if it's running
            if p1 and p1.is_alive():
                p1.terminate()
            # Terminate text_worker process if it's running
            if p2 and p2.is_alive():
                p2.terminate()
            ser.close()  # Close the serial port
            return False  # Indicate to the calling loop that it should exit


try:
    # Confirm the serial port is open and display the baud rate
    print(f"Opened {serialPort} at {baudRate} baud rate.")
    # Main loop that continues until a shutdown is initiated
    while not kill_everything:

        # Text Detection Mode
        if current_mode == 0:
            print(f'Im in mode: {current_mode}')

            # Start the text detection script as a subprocess
            current_process = run_script(text_script)
            text = "Running Text Detection"
            TTS.speak_async(text)  # Inform the user about the mode and next steps
            TTS.speak_async('Press button 2 to capture image')
            print(text)

            # Continuous check for mode change or shutdown command
            while True:
                check_serial_input()
                if current_mode != 0 or kill_everything:
                    current_process.kill()
                    break

        # Image Classification Mode (Not currently suppported with glasses, used as idle state in demo)
        elif current_mode == 1:
            print(f'Im in mode: {current_mode}')

            # Start the image classification script as a subprocess
            current_process = run_script(classify_script)
            text = "Running Image Classification"
            # TTS.speak_async(text)  # Uncomment if you want TTS feedback for this mode
            print(text)

            # Continuous check for mode change or shutdown command
            while True:
                check_serial_input()
                if current_mode != 1 or kill_everything:
                    current_process.kill()
                    break

        # Gemini Assistant Mode
        elif current_mode == 2:
            print(f'Im in mode: {current_mode}')

            # Start the Gemini assistant script as a subprocess
            current_process = run_script(gemini_script)
            text = "Running Gemini Assistant"
            TTS.speak_async(text)  # Inform the user about the mode
            TTS.speak_async('Press button 2 to capture image')
            print(text)

            # Continuous check for mode change or shutdown command
            while True:
                check_serial_input()
                if current_mode != 2 or kill_everything:
                    current_process.kill()
                    break

        # Object Detection Mode
        elif current_mode == 3:
            print(f'Im in mode: {current_mode}')

            # Start the object detection script as a subprocess
            current_process = run_script(detect_script)
            text = "Running Object Detection"
            TTS.speak_async(text)  # Provide auditory feedback about the current mode
            print(text)

            # Continuous check for mode change or shutdown command
            while True:
                check_serial_input()
                if current_mode != 3 or kill_everything:
                    current_process.kill()  # Terminate the subprocess if mode changes or shutdown initiated
                    break

except Exception as e:
    # Log any errors that occur during the main loop execution
    print(f"Error occurred: {e}")

# Cleanup and shutdown operations
print("Shutting Down...")
TTS.speak_async('Shutting Down...')  # Provide auditory feedback that the application is shutting down
