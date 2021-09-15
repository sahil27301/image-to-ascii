import base64
from io import BytesIO
from PIL import Image
from tkinter import filedialog, Tk

root = Tk()
root.title("Image Viewer")

root.filename = filedialog.askopenfilename(
    initialdir="/", title="Select an image", filetypes=(("png files", "*.png"), ("jpeg files", "*.jpeg"), ("jpg files", "*.JPG")))
image_obj = Image.open(root.filename)

im_file = BytesIO()
image_obj.save(im_file, format="JPEG")
im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
im_b64 = base64.b64encode(im_bytes)
