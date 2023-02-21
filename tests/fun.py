import pyautogui
import keyboard

def on_key_press(key):
    if key.name == 'm':
        screenshot = pyautogui.screenshot()
        screenshot.save('screenshot.png')
        print("Screenshot saved!")

# Set up a listener for key presses
keyboard.on_press(on_key_press)

# Wait for user input
input("Press any key to exit...")
