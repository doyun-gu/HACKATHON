import asyncio
from tkinter import Tk, Label
from bleak import BleakClient
import keyboard

# Define the Bluetooth device address and the characteristic UUID
DEVICE_ADDRESS = "Your_Device_Address_Here"
COMMAND_CHARACTERISTIC_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

class SimpleRoverControlApp:
    def __init__(self, root):
        self.root = root
        self.client = BleakClient(DEVICE_ADDRESS)
        self.setup_gui()

    def setup_gui(self):
        self.root.title("ROVER Control")
        label = Label(self.root, text="Press W, A, S, D to control the ROVER", font=("Consolas", 12))
        label.pack(pady=20)

    async def send_command(self, command):
        try:
            if not self.client.is_connected:
                await self.client.connect()
            await self.client.write_gatt_char(COMMAND_CHARACTERISTIC_UUID, command.encode())
        except Exception as e:
            print(f"Failed to send command {command}: {e}")

    def send_command_sync(self, command):
        asyncio.run(self.send_command(command))

def on_key_event(event):
    if event.name in ["w", "a", "s", "d"]:
        app.send_command_sync(event.name)

def main():
    global app
    root = Tk()
    app = SimpleRoverControlApp(root)
    keyboard.on_press(on_key_event)
    root.mainloop()

if __name__ == "__main__":
    main()
