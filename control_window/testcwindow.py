import asyncio
import tkinter as tk
from tkinter import ttk
from bleak import BleakScanner, BleakClient
import keyboard
import threading

# This code is to control the rover robot via bluetooth
# Keyboard (w, a, s, d) is used to control the robot
# w: forward, a: left, s: backward, d: right
# When the key is not pressed, for a while, it will send the stop signal to the robot

# The code is tested on Arduino Uno and External Bluetooth Module will receive the signal from the computer
class RoverControlApp:
    def __init__(self, root):
        self.root = root
        self.setup_gui()
        self.device_address = None
        self.client = None

        self.command_characteristic_uuid = "0000ffe1-0000-1000-8000-00805f9b34fb"

    def setup_gui(self):
        self.root.title("ROVER 11 Control Manager")
        self.root.configure(background="black")
        self.root.geometry("400x200")

        # Font similar to VS Code's default
        self.font = ("Consolas", 12)

        self.scan_button = tk.Button(self.root, text="Scan for Devices", font=self.font, bg="black", fg="white", command=self.scan_for_devices)
        self.scan_button.pack(pady=20)

        self.status_label = tk.Label(self.root, text="Status: Not connected", font=self.font, bg="black", fg="white")
        self.status_label.pack(pady=10)

        self.direction_label = tk.Label(self.root, text="Direction: N/A", font=self.font, bg="black", fg="white")
        self.direction_label.pack(pady=10)

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
        self.direction_label.config(text=f"Direction: {direction}")
        # Here you would add the code to send the command to the rover via Bluetooth

def on_key_event(event):
    direction = {
        "w": "Forward",
        "a": "Left",
        "s": "Backward",
        "d": "Right",
    }.get(event.name, "N/A")
    app.update_direction(direction)

def main():
    global app
    root = tk.Tk()
    app = RoverControlApp(root)
    keyboard.on_press(on_key_event)
    root.mainloop()

if __name__ == "__main__":
    main()