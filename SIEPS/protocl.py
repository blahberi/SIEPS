import cv2
import numpy as np

class Protocol:
    def __init__(self, use_more_bits=False, encrypt=False, use_different_encoding=False, encoding=None):
        self.use_more_bits = use_more_bits  # use the 2 lsb instead of just 1 lsb
        self.encrypt = encrypt  # encrypt with AES 256
        self.use_different_encoding = use_different_encoding  # use an encoding different from the default(ASCII)
        self.encoding = None
        self.encodings = ["base64", "png", "jpg", "mp4", "pdf" "exe", "zip", "custom"]
        if self.use_different_encoding:
            self.encoding = encoding

    def read_protocol(self, image):
        pixels = image[0][0], image[0][1]

        self.use_more_bits = np.binary_repr(pixels[0][2])[-1]
        self.encrypt = np.binary_repr(pixels[0][1])[-1]
        self.use_different_encoding = np.binary_repr(pixels[0][0])[-1]

        if self.use_different_encoding:
            r = np.binary_repr(pixels[1][2])[-1]
            g = np.binary_repr(pixels[1][1])[-1]
            b = np.binary_repr(pixels[1][0])[-1]

            self.encoding = self.encodings[int(r+g+b, 2)]

    def write_protocol(self, image):
        pixels = image[0][0], image[0][1]

        r = np.binary_repr(pixels[0][2])
        g = np.binary_repr(pixels[0][1])
        b = np.binary_repr(pixels[0][0])

        r[-1] = self.use_more_bits
        g[-1] = self.encrypt
        b[-1] = self.use_different_encoding

        r = int(r, 2)
        g = int(g, 2)
        b = int(b, 2)

        pixels[0][2] = r
        pixels[0][1] = g
        pixels[0][0] = b

        if self.use_different_encoding:
            r = list(np.binary_repr(pixels[1][2]))
            g = list(np.binary_repr(pixels[1][1]))
            b = list(np.binary_repr(pixels[1][0]))

            encoding_index = self.encodings.index(self.encoding)
            rgb = np.binary_repr(encoding_index)
            r[-1] = rgb[0]
            g[-1] = rgb[1]
            b[-1] = rgb[2]

            r = "".join(r)
            g = "".join(g)
            b = "".join(b)

            r = int(r, 2)
            g = int(g, 2)
            b = int(b, 2)

            pixels[1][2] = r
            pixels[1][1] = g
            pixels[1][0] = b
