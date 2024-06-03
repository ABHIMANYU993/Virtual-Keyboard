Overview

The provided Python script implements a virtual keyboard controlled through hand gestures using OpenCV, MediaPipe (via the custom handdetect module), and the pynput library for keyboard input.
The virtual keyboard captures video input, detects hand landmarks to identify key presses, and simulates typing actions accordingly.

Key Components

	1. Libraries and Initialization
		o OpenCV: Captures video input and processes frames.
		o NumPy: Handles array operations.
		o Custom handdetect Module: Detects hand landmarks using MediaPipe.
		o pynput.keyboard.Controller: Simulates keyboard presses.
		o PyAutoGUI: Provides additional keyboard control, such as pressing and holding keys.
		o Keyboard: Detects specific keyboard key presses, like ending the program with "F2".
	2. Video Capture Setup
		o Initializes video capture with a resolution of 1280x720 pixels.
	3. Keyboard Layouts
		o Defines three keyboard layouts: standard keys, lowercase keys, and symbol keys.
	4. Drawing Buttons
		o A function, drawAll, draws all keys on the image with their respective positions and sizes, handling special cases for "ENTER," "CAP," and "DEL" buttons to fit text properly.
	5. Hand Detection and Key Presses
		o Detects hand landmarks and identifies fingertip positions.
		o Determines if a fingertip is within a key s bounding box, triggering a key press.
		o Handles key functionalities such as typing characters, pressing "ENTER," "DELETE," and toggling "CAP" (Caps Lock), "CTRL," and "SHIFT."
	6. Main Loop
		o Continuously captures frames from the camera, processes hand landmarks, and checks for key presses.
		o Displays the typed text on the screen.
		o Calculates and displays FPS.
		o Exits the loop and ends the program when "F2" is pressed.

Key Functions and Features

	* Hand Detection: Utilizes MediaPipe for detecting and tracking hand landmarks.
	* Virtual Keyboard Drawing: Dynamically draws keys on the video frame, adjusting sizes for specific keys.
	* Gesture-Based Typing: Maps hand gestures to key presses, including support for special keys like "CTRL" and "SHIFT."
	* Real-Time Feedback: Displays the typed text and provides visual feedback for key presses.

Code Execution

	* Run the VirtualKeyboard.py to start the virtual keyboard application.
	* Use hand gestures to type, with keys highlighted when selected.
	* Press "F2" to terminate the program.
