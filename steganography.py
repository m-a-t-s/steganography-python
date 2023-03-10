# Import necessary modules
import argparse
from PIL import Image

# Define a function to encode a message into an image using the LSB technique
def encode_image(image_path, message):
    """
    Encode the given message into the image using the LSB technique
    """
    # Open the image
    img = Image.open(image_path)

    # Check if the message can fit in the image
    width, height = img.size
    pixels = img.load()
    message_length = len(message)
    if message_length * 8 > width * height * 3:
        raise ValueError("Message too large to fit in image")

    # Encode the message into the image
    message += "~" * ((width * height * 3 // 8) - message_length)
    message_bits = "".join([format(ord(c), '08b') for c in message])
    bit_index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if bit_index < len(message_bits):
                pixels[x, y] = (r & 0b11111110 | int(message_bits[bit_index]), g & 0b11111110 | int(message_bits[bit_index+1]), b & 0b11111110 | int(message_bits[bit_index+2]))
            bit_index += 3

    # Save the encoded image
    img.save("encoded_" + image_path)

# Define a function to decode a message from an image using the LSB technique
def decode_image(image_path):
    """
    Decode the message from the image using the LSB technique
    """
    # Open the image
    img = Image.open(image_path)

    # Decode the message from the image
    width, height = img.size
    pixels = img.load()
    message_bits = ""
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            message_bits += bin(r)[-1] + bin(g)[-1] + bin(b)[-1]
    message = ""
    for i in range(0, len(message_bits), 8):
        if message_bits[i:i+8] != "01111110":
            message += chr(int(message_bits[i:i+8], 2))
        else:
            break

    return message

# Define the main function to handle command-line arguments
def main():
    # Define the command-line arguments
    parser = argparse.ArgumentParser(description='Steganography tool for hiding messages in images.')
    parser.add_argument('mode', choices=['encode', 'decode'], help='The mode of operation: "encode" or "decode".')
    parser.add_argument('image', help='The path of the image file.')
    parser.add_argument('-m', '--message', help='The message to encode in the image.')
    args = parser.parse_args()

    # Check the mode of operation
    if args.mode == 'encode':
        # Check if a message argument is provided
        if not args.message:
            print('Error: message argument is required in encode mode')
            return
        # Call the encode_image function with the image path and message
        encode_image(args.image, args.message)
        print('Message encoded in the image.')
    else:
        # Call the decode_image function with the image path and print the decoded message
        message = decode_image(args.image)
        print('Decoded message:', message)

# Call the main function if this is the main module
if __name__ == '__main__':
    main()
    