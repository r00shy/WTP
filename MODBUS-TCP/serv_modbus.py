import os
import random
import string
import struct
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext
from PIL import Image, PngImagePlugin
import io

# Constants
MODBUS_PORT = 5020
IMAGE_PATH = "cat.png"
ENCODED_IMAGE_PATH = "encoded_image.png"
START_REGISTER = 1000
SIZE_REGISTER = START_REGISTER - 1  # Storing image size
CHUNK_SIZE = 125
MAX_REGISTERS = 10000
MAX_IMAGE_SIZE = MAX_REGISTERS * 2  # 20000 bytes

# Generating a random secret

def generate_secret():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Encoding the secret in PNG metadata

def encode_secret_in_image(secret, input_file, output_file):
    img = Image.open(input_file).convert("RGB")

    # Adding the secret to PNG metadata
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Secret", secret)

    with io.BytesIO() as output:
        img.save(output, format="PNG", pnginfo=meta)
        img_data = output.getvalue()

    # **Making the number of bytes even**
    if len(img_data) % 2 != 0:
        img_data += b"\x00"  # Adding 1 byte of padding

    if len(img_data) > MAX_IMAGE_SIZE:
        print(f"Image size ({len(img_data)} bytes) exceeds MODBUS limit ({MAX_IMAGE_SIZE} bytes)")
        return None

    with open(output_file, "wb") as f:
        f.write(img_data)

    print(f"Image encoded with secret: {secret}")
    print(f"First 20 bytes of encoded image: {img_data[:20]}")
    
    return img_data

# Loading the image into MODBUS

def load_image_to_modbus(context, image_data, start_register):
    if len(image_data) % 2 != 0:
        print("Error: Image data length is odd after processing. This should not happen!")
        return

    registers = list(struct.unpack(f">{len(image_data) // 2}H", image_data))

    for i, value in enumerate(registers):
        context[0].setValues(3, start_register + i, [value])

    # Storing the number of written registers in a special register
    context[0].setValues(3, SIZE_REGISTER, [len(registers)])

    print(f"Image loaded into MODBUS registers {start_register}-{start_register + len(registers)}")
    print(f"First 20 registers: {registers[:20]}")

# Starting the MODBUS TCP server

def run_modbus():
    print(f"Starting Modbus TCP Server on port {MODBUS_PORT}...")

    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0] * MAX_REGISTERS),
        co=ModbusSequentialDataBlock(0, [0] * MAX_REGISTERS),
        hr=ModbusSequentialDataBlock(0, [0] * MAX_REGISTERS),
        ir=ModbusSequentialDataBlock(0, [0] * MAX_REGISTERS),
    )
    context = ModbusServerContext(slaves=store, single=True)

    # Generating and embedding the secret into the image
    current_secret = generate_secret()
    print(f"New Secret: {current_secret}")

    encoded_image_data = encode_secret_in_image(current_secret, IMAGE_PATH, ENCODED_IMAGE_PATH)
    if encoded_image_data:
        load_image_to_modbus(context, encoded_image_data, START_REGISTER)
        StartTcpServer(context, address=("0.0.0.0", MODBUS_PORT))
    else:
        print("Failed to encode image, exiting.")

if __name__ == "__main__":
    run_modbus()

























































































