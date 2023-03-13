from PIL import Image
import argparse

def encode_image(image_path, message):
    image = Image.open(image_path)
    image = image.convert('RGB')
    width, height = image.size
    pixel_index = 0
    message_index = 0
    message += "\n"
    binary_message = ''.join([format(ord(i), "08b") for i in message])
    message_length = len(binary_message)
    if message_length > (width * height):
        raise ValueError("Message is too long to encode in the provided image.")
    for row in range(height):
        for col in range(width):
            r, g, b = image.getpixel((col, row))
            if message_index < message_length:
                pixel_binary = f"{r:08b}{g:08b}{b:08b}"
                new_pixel_binary = pixel_binary[:7] + binary_message[pixel_index] + pixel_binary[8:]
                new_r = int(new_pixel_binary[:8], 2)
                new_g = int(new_pixel_binary[8:16], 2)
                new_b = int(new_pixel_binary[16:], 2)
                image.putpixel((col, row), (new_r, new_g, new_b))
                pixel_index += 1
                message_index += 1
            else:
                break
        if message_index >= message_length:
            break
    image.save("encoded_image.png")
    print("Message encoded successfully in the provided image.")

def decode_image(image_path):
    image = Image.open(image_path)
    image = image.convert('RGB')
    width, height = image.size
    binary_message = ""
    for row in range(height):
        for col in range(width):
            r, g, b = image.getpixel((col, row))
            binary_message += f"{r:08b}"[-1] + f"{g:08b}"[-1] + f"{b:08b}"[-1]
    message = ""
    for i in range(0, len(binary_message), 8):
        message += chr(int(binary_message[i:i+8], 2))
        if message[-1] == "\n":
            break
    print("Decoded message:", message[:-1])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encode or decode a message in an image using LSB steganography.")
    parser.add_argument("action", choices=["encode", "decode"], help="Whether to encode or decode a message in an image.")
    parser.add_argument("image_path", help="The path to the image to be used.")
    parser.add_argument("message", nargs="?", default="", help="The message to be encoded. Required for encoding, optional for decoding.")
    args = parser.parse_args()
    action = args.action
    image_path = args.image_path
    message = args.message
    if action == "encode" and message == "":
        parser.error("Message is required for encoding.")
    try:
        if action == "encode":
            encode_image(image_path, message)
        else:
            decode_image(image_path)
    except ValueError as e:
        print("Error:", e)
