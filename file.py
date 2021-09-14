import base64
from io import BytesIO
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from xmlrpc.client import ServerProxy

root = Tk()
root.title("Image Viewer")

root.filename = filedialog.askopenfilename(
    initialdir="/", title="Select an image", filetypes=(("png files", "*.png"), ("jpeg files", "*.jpeg"), ("jpg files", "*.JPG")))
label = Label(root, text=root.filename).pack()
image_obj = Image.open(root.filename)
image = ImageTk.PhotoImage(Image.open(root.filename))
image_label = Label(image=image).pack()
# print(image_obj)

im_file = BytesIO()
image_obj.save(im_file, format="JPEG")
im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
im_b64 = base64.b64encode(im_bytes)
print(im_b64)


#myBtn = Button(root, text="Open File", command=open).pack()
root.mainloop()
