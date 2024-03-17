import asyncio
import tkinter as tk
from tkinter import ttk
from bleak import BleakScanner, BleakClient
import keyboard
import threading
import cv2
from PIL import Image, ImageTk
import time

# This code is to control the rover robot via bluetooth
# Keyboard (w, a, s, d) is used to control the robot
# w: forward, a: left, s: backward, d: right
# When the key is not pressed, for a while, it will send the stop signal to the robot

# The code is tested on Arduino Uno and External Bluetooth Module will receive the signal from the computer
class RoverControlApp:
    def __init__(self, root):
        self.root = root
        self.device_address = None
        self.client = None
        self.led_state = False  # False means LED is OFF, True means ON
        self.setup_gui()
        # Example UUID for the rover's command characteristic
        self.command_characteristic_uuid = "0000ffe1-0000-1000-8000-00805f9b34fb"

    def setup_gui(self):
        self.root.title("ROVER 11 Control Manager")
        self.root.configure(background="black")

        # Geometry
        self.root.geometry("800x600")
        
        # Set up the video frame
        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        self.font = ("Consolas", 12)

        self.scan_button = tk.Button(self.root, text="Scan for Devices", font=self.font, bg="black", fg="white", command=self.scan_for_devices)
        self.scan_button.pack(pady=20)

        self.status_label = tk.Label(self.root, text="Status: Not connected", font=self.font, bg="black", fg="white")
        self.status_label.pack(pady=10)

        self.direction_label = tk.Label(self.root, text="Direction: N/A", font=self.font, bg="black", fg="white")
        self.direction_label.pack(pady=10)

        self.led_status_label = tk.Label(self.root, text="LED: OFF", font=self.font, bg="black", fg="white")
        self.led_status_label.pack(pady=10)

    async def discover_devices(self):
        devices = await BleakScanner.discover()
        for device in devices:
            if device.name == "rover11":
                self.device_address = device.address
                break
        if self.device_address:
            await self.connect_to_device()

    def scan_for_devices(self):
        threading.Thread(target=lambda: asyncio.run(self.discover_devices()), daemon=True).start()


    async def connect_to_device(self):
        self.client = BleakClient(self.device_address)
        try:
            await self.client.connect()
            self.status_label.config(text="Status: Connected to rover11")
        except Exception as e:
            self.status_label.config(text=f"Status: Failed to connect ({e})")

    def update_direction(self, direction):
        directions = {
            "w": "Forward",
            "a": "Left",
            "s": "Backward",
            "d": "Right",
        }
        if direction.lower() in directions:
            self.direction_label.config(text=f"Direction: {directions[direction.lower()]}")
            # Send command to the rover
            self.send_command(direction.lower())
        elif direction.lower() == "l":
            self.toggle_led()
        else:
            self.direction_label.config(text="Direction: N/A")

    def update_led(self):
        self.led_state = not self.led_state
        led_status = "ON" if self.led_state else "OFF"
        self.led_status_label.config(text=f"LED: {led_status}")
        # Send "l" command to the rover to toggle LED
        self.send_command("l")

    def send_command(self, command):
        # Check if client is connected and send command
        if self.client and self.client.is_connected:
            asyncio.run(self.client.write_gatt_char(self.command_characteristic_uuid, command.encode()))

    def stream_video(self, video_url):
        while True:
            cap = cv2.VideoCapture(video_url)
            if not cap.isOpened():
                print("Unable to connect to camera. Retrying in 5 seconds...")
                time.sleep(5)
                continue

            while True:
                ret, frame = cap.read()

                if ret:
                    # Resize frame to fit the application window
                    frame = cv2.resize(frame, (320, 240))  # Adjust size as needed
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    im = Image.fromarray(frame)
                    img = ImageTk.PhotoImage(image=im)

                    self.video_label.configure(image=img)
                    self.video_label.image = img

                else:
                    print("Failed to grab frame. Reconnecting...")
                    break  # Break the inner loop to attempt reconnection

                cv2.waitKey(30)
            cap.release()  # Release the capture before reconnecting


    def start_video_stream(self):
        video_url = "http://192.168.137.233/"
        threading.Thread(target=self.stream_video, args=(video_url,), daemon=True).start()


def on_key_event(event):
    if event.name in ["w", "a", "s", "d"]:
        direction = {
            "w": "Forward",
            "a": "Left",
            "s": "Backward",
            "d": "Right",
        }.get(event.name, "N/A")
        app.update_direction(event.name)  # Directly pass the key for direction control
    elif event.name == "l":  # Use the new method for LED control
        app.update_led()

def main():
    global app
    root = tk.Tk()
    app = RoverControlApp(root)
    app.start_video_stream()
    keyboard.on_press(on_key_event)
    root.mainloop()

if __name__ == "__main__":
    main()