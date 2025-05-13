# Tibia Key Presser

A simple utility application to automate key presses in Tibia. This tool allows you to set up multiple keys with custom delay intervals between key presses.

## Features

- Configure up to 8 different keys with custom delay intervals
- Easy-to-use graphical interface
- Automatic detection of Tibia window
- Start/stop functionality with a single click
- Real-time key binding

## Prerequisites

- Python 3.6+
- pywinauto 0.6.8+

## Installation

1. Clone this repository:

   ```
   git clone <repository-url>
   cd tibia-key-presser
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

Run the application with Python:

```
python -m src.main
```

### Using the Key Presser

1. Launch Tibia and login to your character
2. Launch the Tibia Key Presser
3. Click on a key input field and press the key you want to automate
4. Set the delay interval in seconds
5. Add more keys if needed (up to 8)
6. Click "Start" to begin the key pressing
7. Click "Stop" when you want to stop the automation

## Building an Executable

You can build a standalone executable using PyInstaller:

```
pip install pyinstaller
pyinstaller --onefile src/main.py --name tibia_key_presser
```

The executable will be available in the `dist` directory.

## Project Structure

```
tibia-key-presser/
├── src/                     # Source code
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── ui/                  # User interface
│   │   ├── __init__.py
│   │   ├── app_window.py    # Main window class
│   │   └── components/      # UI components
│   │       ├── __init__.py
│   │       └── key_entry.py # Key entry component
│   ├── core/                # Core functionality
│   │   ├── __init__.py
│   │   ├── key_presser.py   # Key pressing logic
│   │   └── window_manager.py # Tibia window connection
│   └── utils/               # Utilities
│       ├── __init__.py
│       └── constants.py     # Constants and configurations
├── requirements.txt         # Dependencies
└── README.md                # Documentation
```

## License

This project is licensed under the MIT License.
