from io import BytesIO
from PIL import Image
from tkinter import filedialog, Tk
import Pyro4
import argparse


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--columns",
        help="Specify the number of columns in the generated ASCII art image.",
        type=int,
        default=100
    )
    parser.add_argument(
        "-s",
        "--scale",
        help="Specify the scale of the image, between (0, 1].",
        type=float,
        default=0.43
    )
    parser.add_argument(
        "-l",
        "--lightweight",
        help="Limit the ASCII character used to 10 symbols.",
        action="store_true"
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-q",
        "--quiet",
        help="The output is printed to a default file image.txt instead of the command line.",
        action="store_true"
    )
    group.add_argument(
        "-o",
        "--output",
        help="Specify the path of the file to print the output to.",
    )

    args = parser.parse_args()

    if not 0.3 <= args.scale <= 1:
        print("Warning: scale cannot lie outside the range [0.3, 1]. Defaulting to 0.43.")
        args.scale = 0.43

    # Image Selection Dialog
    root = Tk()
    root.title("Image Viewer")
    root.filename = filedialog.askopenfilename(title="Select an image", filetypes=(
        ("jpg files", "*.JPG"), ("png files", "*.png"), ("jpeg files", "*.jpeg")))
    image_object = Image.open(root.filename)

    # Get image bytes
    image_file = BytesIO()
    image_object.save(image_file, format="JPEG")
    image_bytes = image_file.getvalue()

    imageConverter = Pyro4.Proxy('PYRONAME:example.image.converter')
    print(imageConverter.get_ascii_art(image_bytes, args.columns, args.scale, args.lightweight))


if __name__ == "__main__":
    main()
