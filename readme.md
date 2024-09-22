# Tibia Key Presser

This is a **Tibia Key Presser** application designed to automate repetitive key presses within the Tibia game. It allows users to configure up to 8 key-delay pairs, specifying which keys to press and the delay between each key press. The tool is intended to streamline gameplay by simulating key presses at regular intervals based on user-defined settings.

## Features

- **Add up to 8 key-delay pairs**  
  Users can define up to 8 different keys, each paired with a custom delay (in seconds) between presses.

- **Customizable delays**  
  Delays can be set from **0 to 10 seconds**, with precision down to one decimal point, allowing for flexible automation.

- **Reset and delete functionality**  
  Each key-delay pair can be individually reset or deleted, providing full control over the input configuration.

- **Start/Stop controls**  
  The key pressing script can be easily started or stopped with intuitive buttons. Once started, the defined keys will be automatically pressed with the set delays.

- **Connects to the Tibia window**  
  The application automatically detects the Tibia game window and sends key presses directly to it. When window is properly found, window name will change to "Tibia Key Presser - YOUR CHAR NAME"

- **Visual feedback**  
  The application provides status updates and visual cues, such as highlighting the selected key entry and showing messages for user actions.

- **Dynamic user interface**  
  The interface adjusts based on user input, hiding or showing the "Add Key" button as needed depending on the number of configured key-delay pairs.

## Requirements

- Python 3.x
- `tkinter` for the GUI
- `pywinauto` for interacting with the Tibia game window

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SkorczanFFF/tibia-key-presser.git
   cd tibia-key-presser

   ```

2. Install the required Python packages:

   ```bash
   pip install pywinauto

   ```

3. Run the application:
   ```bash
   python bot.py
   ```

## Usage

1. Launch the application and configure the keys and delays.
2. Press **Start** to begin the key pressing automation.
3. The application will send the key presses to the Tibia window based on your configuration.
4. You can add up to 8 keys, set delays between key presses, and remove or reset individual key configurations as needed.
5. Press **Stop** to end the key pressing sequence at any time.

## Background

This tool was created to help automate the process of training **magic level** (MLVL) while the character is on trainers in Tibia. The idea is to simplify repetitive key presses used for this type of training. The application has been tested on **[Eloria](https://www.eloria.pl)**, a private Open Tibia Server.

---

_Note: This tool is intended for personal use and may violate the terms of service of some Tibia servers._
