To use this steganography tool, follow these steps:

Save the code in a Python file, e.g. steganography.py.

Open a terminal or command prompt and navigate to the directory containing the Python file.

Run the following command to encode a message in an image:

`python steganography.py encode image_path -m "message to encode" -o output_image_path`

Replace image_path with the path to the input image file, "message to encode" with the message you want to encode, and output_image_path with the desired path to the output image file. If the -o parameter is not provided, the encoded image will be saved as encoded_image_path in the same directory as the input image file.

Run the following command to decode a message from an image:

`python steganography.py decode image_path`

Replace image_path with the path to the input image file. The decoded message will be printed to the console.
