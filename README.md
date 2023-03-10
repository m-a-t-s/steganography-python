Open a terminal or command prompt and navigate to the directory where the steganography.py script is saved.

To encode a message in an image, use the following command:
`python steganography.py encode <image_path> -m <message>`

Replace <image_path> with the path to the image file that you want to encode the message in, and replace <message> with the message that you want to encode. For example:
`python steganography.py encode my_image.png -m "Hello, world!"`

This will encode the message "Hello, world!" into the image file my_image.png and save the encoded image as encoded_my_image.png in the same directory.

To decode a message from an encoded image, use the following command:
`python steganography.py decode <image_path>`

Replace <image_path> with the path to the encoded image file that you want to decode the message from. For example:
`python steganography.py decode encoded_my_image.png`

This will decode the message from the encoded image file encoded_my_image.png and print the decoded message in the terminal.

That's it! Just follow these steps to use the steganography tool with terminal input using parameters.
