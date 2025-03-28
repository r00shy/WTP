import os
from pymodbus.client.sync import ModbusTcpClient
import struct
from PIL import Image, PngImagePlugin
import io

# Constants
SERVER_IP = "127.0.0.1"
MODBUS_PORT = 5020
START_REGISTER = 1000
SIZE_REGISTER = START_REGISTER - 1  # Reading image size
CHUNK_SIZE = 125
MAX_IMAGE_SIZE = 10000 * 2  
RECEIVED_IMAGE_PATH = "received_encoded_image.png"

# Connecting to the server
client = ModbusTcpClient(SERVER_IP, port=MODBUS_PORT)
client.connect()

# Reading the number of registers actually written by the server
response = client.read_holding_registers(SIZE_REGISTER, 1, unit=1)

if response.isError():
    print(f"❌ Failed to read image size from Modbus: {response}")
    client.close()
    exit(1)

total_registers = response.registers[0]  # Determining how many registers were actually written
total_bytes = total_registers * 2
print(f"Reading {total_registers} registers ({total_bytes} bytes) from Modbus.")

# Reading the image from MODBUS in chunks
def read_image_from_modbus(start_register, total_registers):
    registers = []
    num_chunks = (total_registers // CHUNK_SIZE) + 1

    for i in range(num_chunks):
        start = start_register + i * CHUNK_SIZE
        count = min(CHUNK_SIZE, total_registers - len(registers))

        response = client.read_holding_registers(start, count, unit=1)

        if not response.isError():
            registers.extend(response.registers)
        else:
            print(f"Error reading registers {start}-{start + count}: {response}")
            break

    return struct.pack(f">{len(registers)}H", *registers)

# Restoring the image
img_data = read_image_from_modbus(START_REGISTER, total_registers)

# Checking PNG integrity
if not img_data.startswith(b'\x89PNG\r\n\x1a\n'):
    print("❌ Received data is not a valid PNG file!")
    client.close()
    exit(1)

# Saving the PNG
with open(RECEIVED_IMAGE_PATH, "wb") as f:
    f.write(img_data)

print(f"Encoded image saved as {RECEIVED_IMAGE_PATH}")

# Checking image opening
try:
    img = Image.open(RECEIVED_IMAGE_PATH)
    img.verify()  # Verifying integrity
    print("✅ Image successfully verified!")

    img = Image.open(RECEIVED_IMAGE_PATH)
    img.show()
    
    # Reading the secret
    secret = img.info.get("Secret", "❌ No secret found")
    print(f"✅ Secret successfully recovered: {secret}")

except Exception as e:
    print(f"❌ Failed to open image: {e}")

# Disconnecting from the server
client.close()



























































































































