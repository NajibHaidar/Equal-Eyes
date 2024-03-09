"""
Serial Port Communication Script (for debugging)

This script is designed to test and demonstrate basic serial port communication functionality using Python's `serial` library. 
It opens a specified serial port at a given baud rate, continuously listens for incoming data, and prints the received data 
to the console. This is useful for testing serial port connections and ensuring data can be successfully transmitted and 
received between devices.

Note: This script is intended for demonstration purposes and may need adjustments based on the specific serial device and 
operating system being used.

Requirements:
- PySerial package installed.
- Access to a valid serial port (e.g., `/dev/ttyS0` for Linux).

Usage:
- Update `serialPort` and `baudRate` variables as needed to match your setup.
- Run the script and send data to the specified serial port from another device or application.
"""

import serial  # Import the PySerial library for serial port communication

# Configuration: Serial port and baud rate settings
serialPort = '/dev/ttyS0'  # Serial port to use (e.g., COM3 for Windows or /dev/ttyUSB0 for Linux)
baudRate = 9600  # Communication speed in bits per second

try:
    # Attempt to open the specified serial port with the set baud rate and a timeout
    ser = serial.Serial(serialPort, baudRate, timeout=1)
    print(f"Opened {serialPort} at {baudRate} baud rate.")

    # Continuously listen for data on the serial port
    while True:
        if ser.in_waiting > 0:  # Check if data is waiting in the serial buffer
            data = ser.readline().decode().strip()  # Read the data and decode it to a string

            if data:  # If data was received, print it
                print(f"Received: {data}")

except serial.SerialException as e:
    # Handle errors in opening the serial port
    print(f"Error opening serial port: {e}")

except KeyboardInterrupt:
    # Handle the user pressing CTRL+C to interrupt the script
    print("Exiting...")

finally:
    # Ensure the serial port is closed when the script ends or an error occurs
    if 'ser' in locals() or 'ser' in globals():
        ser.close()
