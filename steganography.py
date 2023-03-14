# Python program implementing Image Steganography

# PIL module is used to extract
# pixels of image and modify it
from PIL import Image

def gen_data(data):
    """
    Convert encoding data into 8-bit binary form using ASCII value of characters.
    :param data: str
    :return: list
    """
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd


def modify_pixels(pix, data):
    """
    Modify pixels according to the 8-bit binary data and yield pixel values.
    :param pix: tuple
    :param data: str
    :return: tuple
    """
    datalist = gen_data(data)
    lendata = len(datalist)
    imdata = iter(pix)
    for i in range(lendata):
        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] + imdata.__next__()[:3] + imdata.__next__()[:3]]
        # Pixel value should be made odd for 1 and even for 0
        for j in range(0, 8):
            if datalist[i][j] == '0' and pix[j] % 2 != 0:
                pix[j] -= 1
            elif datalist[i][j] == '1' and pix[j] % 2 == 0:
                if pix[j] != 0:
                    pix[j] -= 1
                else:
                    pix[j] += 1
        # Eighth pixel of every set tells whether to stop or read further. 0 means keep reading; 1 means the message is over.
        if i == lendata - 1:
            if pix[-1] % 2 == 0:
                if pix[-1] != 0:
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if pix[-1] % 2 != 0:
                pix[-1] -= 1
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encode_image(newimg, data):
    """
    Encode the data into the image by modifying the pixels.
    :param newimg: PIL Image object
    :param data: str
    """
    w = newimg.size[0]
    (x, y) = (0, 0)
    for pixel in modify_pixels(newimg.getdata(), data):
        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1

# Encode data into image
def encode():
    # Open the image file
    img = Image.open(input("Enter image name(with extension) : "), 'r')

    # Get the data to be encoded
    data = input("Enter data to be encoded : ").strip()
    if not data:
        raise ValueError('Data is empty')

    # Make a copy of the image
    newimg = img.copy()

    # Encode the data in the image
    encode_image(newimg, data)

    # Save the new image
    new_img_name = input("Enter the name of new image(with extension) : ")
    newimg.save(new_img_name, new_img_name.split(".")[-1].upper())

    # Output message to indicate encoding success
    print(f"The data has been encoded in the image: {new_img_name}")


# Decode the data in the image
def decode():
    # Open the image file
    img = Image.open(input("Enter image name(with extension) : "), 'r')

    # Initialize variables
    data = ''
    imgdata = iter(img.getdata())

    while True:
        # Get the next 3 pixels
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        # Convert the pixel values to binary
        binstr = ''.join(['0' if i % 2 == 0 else '1' for i in pixels[:8]])

        # Convert the binary string to ASCII and add to data
        data += chr(int(binstr, 2))

        # Check if the last pixel is odd, which indicates the end of the message
        if pixels[-1] % 2 != 0:
            return data


def main():
    # Ask user for choice
    choice = int(input(":: Welcome to Steganography ::\n"
                       "1. Encode\n2. Decode\n"))

    # Check user choice
    if choice == 1:
        # If user wants to encode, call encode function
        encode()
    elif choice == 2:
        # If user wants to decode, call decode function and print the decoded message
        decoded_message = decode()
        print(f"Decoded Word: {decoded_message}")
    else:
        # If user enters an invalid choice, raise an exception
        raise ValueError("Enter correct input")

# Driver Code
if __name__ == '__main__' :

	# Calling main function
	main()
