import pywinauto
import time
import threading

# Function to press F3 every 2 seconds
def press_f3():
    app = pywinauto.Application().connect(title_re="Tibia - Don Kichot")
    window = app.window(title_re="Tibia - Don Kichot")
    while True:
        window.send_keystrokes('{F3}')
        time.sleep(2)

# Function to press F2 every 1 second
def press_f2():
    app = pywinauto.Application().connect(title_re="Tibia - Don Kichot")
    window = app.window(title_re="Tibia - Don Kichot")
    while True:
        window.send_keystrokes('{F2}')
        time.sleep(1)

# Create threads to run both functions simultaneously
thread_f2 = threading.Thread(target=press_f2)
thread_f3 = threading.Thread(target=press_f3)

# Start both threads
thread_f2.start()
thread_f3.start()

# This ensures that the program continues running indefinitely
thread_f2.join()
thread_f3.join()
