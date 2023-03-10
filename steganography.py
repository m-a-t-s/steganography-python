from PIL import Image
import argparse

# Define a function to encode a message in an image using the LSB technique
def encode_image(image_path, message):
    """
    Encode the message in the image using the LSB technique
    """
    # Open the image and convert the message to binary
    img = Image.open(image_path)
    message_binary = "".join([format(ord(c), "08b") for c in message])

    # Check if the message can fit in the image
    image_size = img.size[0] * img.size[1]
    message_size = len(message_binary)
    if message_size + 32 > image_size:
        raise ValueError("Message is too large to fit in the image")

    # Add message size to the beginning of the message
    message_binary = format(message_size, "032b") + message_binary

    # Encode the message in the image
    pixels = img.load()
    message_index = 0
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if message_index < len(message_binary):
                r, g, b = pixels[x, y]
                r_binary = format(r, "08b")[:-1] + message_binary[message_index]
                g_binary = format(g, "08b")[:-1] + message_binary[message_index+1]
                b_binary = format(b, "08b")[:-1] + message_binary[message_index+2]
                pixels[x, y] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
                message_index += 3
            else:
                break

    # Save the encoded image
    encoded_image_path = "encoded_" + image_path
    img.save(encoded_image_path)
    print("Encoded image saved as", encoded_image_path)


# Define a function to decode a message from an image using the LSB technique
def decode_image(image_path):
    """
    Decode the message from the image using the LSB technique
    """
    # Open the image
    img = Image.open(image_path)

    # Decode the message from the image
    pixels = img.load()
    message_size_binary = ""
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b = pixels[x, y]
            message_size_binary += format(r, "08b")[-1] + format(g, "08b")[-1] + format(b, "08b")[-1]
            if len(message_size_binary) == 32:
                message_size = int(message_size_binary, 2)
                message_binary = ""
                for i in range(message_size * 8):
                    r, g, b = pixels[x, y]
                    message_binary += format(r, "08b")[-1] + format(g, "08b")[-1] + format(b, "08b")[-1]
                    if len(message_binary) == message_size * 8:
                        message = ""
                        for j in range(0, len(message_binary), 8):
                            message += chr(int(message_binary[j:j+8], 2))
                        return message
    raise ValueError("No message found in the image")

# Define a function to parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Encode or decode a message in an image using steganography")
    parser.add_argument("mode", choices=["encode", "decode"], help="encode a message in an image or decode a message from an image")
    parser.add_argument("image_path", help="path to the input image file")
    parser.add_argument("-m", "--message", help="message to encode in the image")
    parser.add_argument("-o", "--output", help="path to the output image file")
    args = parser.parse_args()
    return args


# Main function to run the program
def main():
    args = parse_args()

    if args.mode == "encode":
        if not args.message:
            raise ValueError("Message argument is required for encode mode")
        encode_image(args.image_path, args.message)
    elif args.mode == "decode":
        message = decode_image(args.image_path)
        print("Decoded message:", message)

    print("Done!")


if __name__ == "__main__":
    main()
