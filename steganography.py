import argparse
from PIL import Image

# Define command line arguments
parser = argparse.ArgumentParser(description='Encode or decode a message in an image using steganography.')
parser.add_argument('mode', choices=['encode', 'decode'], help='Select whether to encode or decode a message.')
parser.add_argument('input_file', help='Path to the input image file.')
parser.add_argument('-m', '--message', help='The message to be encoded in the image.')
parser.add_argument('-o', '--output_file', help='Path to the output image file.')
args = parser.parse_args()

# Define the function to encode a message into an image
def encode_message(image, message):
    # Convert the message into binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    # Get the dimensions of the image
    width, height = image.size
    # Calculate the maximum number of bits we can encode in the image
    max_bits = width * height * 3 // 8
    # Make sure the message can fit in the image
    if len(binary_message) > max_bits:
        raise ValueError("Message is too long to be encoded in the image.")
    # Add a sentinel at the end of the message to indicate the end of the message
    binary_message += '1111111100000000'
    # Encode the message into the image
    pixels = list(image.getdata())
    # Replace the least significant bit of each color channel with a bit of the message
    for i, pixel in enumerate(pixels):
        red, green, blue = pixel
        if i < len(binary_message):
            red = red & ~1 | int(binary_message[i])
        if i+1 < len(binary_message):
            green = green & ~1 | int(binary_message[i+1])
        if i+2 < len(binary_message):
            blue = blue & ~1 | int(binary_message[i+2])
        pixels[i] = (red, green, blue)
    # Create a new image with the encoded message
    encoded_image = Image.new(image.mode, image.size)
    encoded_image.putdata(pixels)
    return encoded_image

# Define the function to decode a message from an image
def decode_message(image):
    # Get the pixel data from the image
    pixels = list(image.getdata())
    # Extract the least significant bit of each color channel to get the message
    binary_message = ''
    for pixel in pixels:
        red, green, blue = pixel
        binary_message += str(red & 1)
        binary_message += str(green & 1)
        binary_message += str(blue & 1)
    # Convert the binary message back into text
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))
        if message[-16:] == '1111111100000000':
            message = message[:-16]
            break
    return message

# Load the input image
image = Image.open(args.input_file)

if args.mode == 'encode':
    # Make sure a message was provided
    if not args.message:
        raise ValueError("You must provide a message to encode.")
    # Encode the message into the image
    encoded_image = encode_message(image, args.message)
    # Save the encoded image to the output file
    output_file = args.output_file or 'encoded.png'
    encoded_image.save(output_file)
    print(f"Message successfully encoded in {output_file}.")
elif args.mode == 'decode':
    # Decode the message from the image
    message = decode_message(image)
    # Print the decoded message to the console
    print(f"Decoded message: {message}")

