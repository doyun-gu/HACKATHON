import asyncio
from bleak import BleakScanner, BleakClient

device_address = "98:D3:41:F6:EA:D4"

async def discover_services_and_characteristics(address):
    async with BleakClient(address) as client:
        await client.connect()
        print(f"Connected: {client.is_connected}")
        
        for service in client.services:
            print(f"Service: {service.uuid}")
            for char in service.characteristics:
                print(f"  Characteristic: {char.uuid} - Properties: {char.properties}")

asyncio.run(discover_services_and_characteristics(device_address))
