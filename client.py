import base64
from io import BytesIO
from PIL import Image
from tkinter import filedialog, Tk
from xmlrpc.client import ServerProxy


def main():
    root = Tk()
    root.title("Image Viewer")

    root.filename = filedialog.askopenfilename(title="Select an image", filetypes=(
        ("jpg files", "*.JPG"), ("png files", "*.png"), ("jpeg files", "*.jpeg")))
    image_obj = Image.open(root.filename)

    im_file = BytesIO()
    image_obj.save(im_file, format="JPEG")
    im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
    im_b64 = base64.b64encode(im_bytes)
    with ServerProxy('http://localhost:3000') as proxy:
        result = proxy.get_ascii_art(im_b64, 100, 0.43, False)
        print(result)


if __name__ == "__main__":
    main()
