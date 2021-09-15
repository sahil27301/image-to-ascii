import numpy as np
from PIL import Image
from pyngrok import ngrok
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.

http_tunnel = ngrok.connect()


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/imageUpload',)


# Create server
with SimpleXMLRPCServer((http_tunnel.public_url),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    def imageToAscii(str):
        return str
    server.register_function(imageToAscii, 'imageToAscii')

    # Run the server's main loop
    server.serve_forever()

print("NGROK SERVER:", http_tunnel.public_url)


class ImageConverter:
    """
    A class to convert an image file to ASCII art.
    """
    @staticmethod
    def get_average_grayscale_value(image: Image) -> np.double:
        """
        Parameters
        ----------

        image: Image

            An Image object whose average grayscale value needs to be found.

        Returns
        -------

        average: np.double

            The average grayscale value of the image, between 0 and 255.
        """

        # Convert image to numpy array
        image_array = np.array(image)
        width, height = image_array.shape

        return np.average(image_array.reshape(width*height))

    @staticmethod
    def get_ascii_art(image_path: str, columns: int = 80, scale: float = 0.43, lightweight: bool = False) -> str:
        """
        Parameters
        ----------

        image_path: str

            Contains the image file location.

        columns: int

            Specifies the width of each row in ASCII image.

            Default is 80.

        scale: float

            Specifies the scale of the image, and expects a value in the range (0, 1]

            Default is 0.43, which suits the Courier Font.

        lightweight: bool

            If set to True, limits the ascii characters to 10 symbols.

            If set to False, uses 70 ascii characters.

            Default value is False.

        Returns
        -------

        ascii_art: str

            A string containing the ASCII art representation of the image.
        """

        gscale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
        gscale_light = "@%#*+=-:. "

        # Convert the image to grayscale
        image = Image.open(image_path).convert('L')

        total_width, total_height = image.size[0], image.size[1]

        # compute width of each tile
        tile_width = int(total_width/columns)
        tile_height = int(tile_width/scale)

        rows = int(total_height/tile_height)

        if columns > total_width or rows > total_height:
            return "Error: Invalid dimensions. Try reducing the number of columns or enlarging the image."

        # To hold the ASCII image as a list of strings, each string representing one row
        ascii_image = ["" for _ in range(rows)]

        for i in range(rows):
            y1 = i * tile_height
            y2 = (i + 1) * tile_height

            # Correction for last row
            if i == rows-1:
                y2 = total_height

            for j in range(columns):

                x1 = j * tile_width
                x2 = (j + 1) * tile_width

                # Correction for last column
                if j == columns - 1:
                    x2 = total_width

                # Exctract tile by cropping image
                img = image.crop((x1, y1, x2, y2))

                average_luminance = ImageConverter.get_average_grayscale_value(img)

                if lightweight:
                    grayscale_value = gscale_light[round(average_luminance*9/255)]
                else:
                    grayscale_value = gscale[round(average_luminance*69/255)]

                ascii_image[i] += grayscale_value

        return "\n".join(ascii_image)


def main():
    image_converter = ImageConverter()
    print(image_converter.get_ascii_art("sample_image.jpg"))


if __name__ == "__main__":
    main()
