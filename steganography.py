# Required Libraries
from PIL import Image

# Function to convert a string to binary
def string_to_binary(message):
    binary_message = ''.join(format(ord(i), '08b') for i in message)
    return binary_message

# Function to convert binary to string
def binary_to_string(binary):
    message = ""
    for i in range(0, len(binary), 8):
        message += chr(int(binary[i:i+8], 2))
    return message

# Function to embed a message in an image
def embed_message(image_path, message):
    # Open the image
    image = Image.open(image_path)

    # Convert message to binary
    binary_message = string_to_binary(message)

    # Check if the image is large enough to embed the message
    if len(binary_message) > image.size[0] * image.size[1]:
        raise ValueError("Image not large enough to embed message")

    # Iterate through each pixel in the image
    pixel_index = 0
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            # Get the pixel at the current location
            pixel = list(image.getpixel((x, y)))

            # Embed the message in the least significant bit of each color channel
            if pixel_index < len(binary_message):
                pixel[0] = pixel[0] & ~1 | int(binary_message[pixel_index])
                pixel[1] = pixel[1] & ~1 | int(binary_message[pixel_index+1])
                pixel[2] = pixel[2] & ~1 | int(binary_message[pixel_index+2])

            # Update the pixel in the image
            image.putpixel((x, y), tuple(pixel))

            # Increment the pixel index
            pixel_index += 3

    # Save the modified image
    image.save("embedded.png")

    print("Message embedded successfully")

# Function to extract a message from an image
def extract_message(image_path):
    # Open the image
    image = Image.open(image_path)

    # Initialise a variable to hold the binary message
    binary_message = ""

    # Iterate through each pixel in the image
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            # Get the pixel at the current location
            pixel = list(image.getpixel((x, y)))

            # Extract the least significant bit from each color channel
            binary_message += str(pixel[0] & 1)
            binary_message += str(pixel[1] & 1)
            binary_message += str(pixel[2] & 1)

    # Convert the binary message to text
    message = binary_to_string(binary_message)

    print("Message extracted successfully:")
    print(message)

# User Instructions
print("Welcome to Steganography tool! Please choose one of the following options:")
print("1. Embed message in an image")
print("2. Extract message from an image")

# Get user input
option = input("Enter your choice (1 or 2): ")

if option == "1":
    # Get image path and message from user
    image_path = input("Enter the path of the image file: ")
    message = input("Enter the message to embed: ")

    # Embed the message in the image
    embed_message(image_path, message)

elif option == "2":
    # Get image path from user
    image_path = input("Enter the path of the image file: ")

    # Extract the message from the image
    extract_message(image_path)

