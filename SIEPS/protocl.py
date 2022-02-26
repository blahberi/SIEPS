import cv2
import numpy as np

class Protocol:
    def __init__(self, use_more_bits=False, encrypt=False, use_different_encoding=False, encoding=None):
        self.use_more_bits = use_more_bits # use the 2 lsb instead of just 1 lsb
        self.encrypt = encrypt # encrypt with AES 256
        self.use_different_encoding = use_different_encoding # use an encoding different from the default(ASCII)
        self.encoding = None
        self.encodings = ["base64", "png", "jpg", "mp4", "pdf" "exe", "zip", "custom"]
        if self.use_different_encoding:
            self.encoding = encoding

    # def read_protocol(self, image):
    #     pixels = image[0][0], image[0][1]
    #
    #     self.use_more_bits = np.binary_repr(pixels[0][2])[-1]
    #     self.encrypt = np.binary_repr(pixels[0][1])[-1]
    #     self.use_different_encoding = np.binary_repr(pixels[0][0])[-1]
    #
    #     if self.use_different_encoding:
    #         r = np.binary_repr(pixels[1][2])[-1]
    #         g = np.binary_repr(pixels[1][1])[-1]
    #         b = np.binary_repr(pixels[1][0])[-1]
    #
    #         self.encoding = self.encodings[int(r+g+b, 2)]
    #
    # def write_protocol(self, image):
    #     pixels = image[0][0], image[0][1]
    #     r = np.binary_repr(pixels[0][2])
    #     g = np.binary_repr(pixels[0][1])
    #     b = np.binary_repr(pixels[0][0])