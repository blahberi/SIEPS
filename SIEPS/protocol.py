import numpy as np


class Protocol:
    def __init__(self, compress="auto", encrypt=False, use_different_encoding=False, encoding="ASCII",
                 custom_encoding=None, bits=1):
        self.compress = compress  # use the 2 lsb instead of just 1 lsb
        self.encrypt = encrypt  # encrypt with AES 256
        self.use_different_encoding = use_different_encoding  # use an encoding different from the default(ASCII)
        self.encodings = ["base64", "png", "jpg", "mp4", "pdf" "exe", "zip", "custom"]
        self.encoding = encoding
        self.custom_encoding = custom_encoding
        self.bits = bits

    def read_protocol(self, image):
        pixels = image[0][0], image[0][1], image[0][2]

        self.compress = bool(int(np.binary_repr(pixels[0][2])[-1]))
        self.encrypt = bool(int(np.binary_repr(pixels[0][1])[-1]))
        self.use_different_encoding = bool(int(np.binary_repr(pixels[0][0])[-1]))

        if self.use_different_encoding:
            r = np.binary_repr(pixels[1][2])[-1]
            g = np.binary_repr(pixels[1][1])[-1]
            b = np.binary_repr(pixels[1][0])[-1]

            self.encoding = self.encodings[int(r + g + b, 2)]

        r = np.binary_repr(pixels[2][2])[-1]
        g = np.binary_repr(pixels[2][1])[-1]
        b = np.binary_repr(pixels[2][0])[-1]

        self.bits = int(r + g + b, 2) + 1

    def write_protocol(self, image):
        pixels = image[0][0], image[0][1], image[0][2]

        r = list(np.binary_repr(pixels[0][2]))
        g = list(np.binary_repr(pixels[0][1]))
        b = list(np.binary_repr(pixels[0][0]))

        r[-1] = str(int(self.compress))
        g[-1] = str(int(self.encrypt))
        b[-1] = str(int(self.use_different_encoding))

        r = "".join(r)
        g = "".join(g)
        b = "".join(b)

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
            while len(rgb) < 3:
                rgb = f"0{rgb}"
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

        r = list(np.binary_repr(pixels[2][2]))
        g = list(np.binary_repr(pixels[2][1]))
        b = list(np.binary_repr(pixels[2][0]))

        rgb = np.binary_repr(self.bits - 1)
        while len(rgb) < 3:
            rgb = f"0{rgb}"
        r[-1] = rgb[0]
        g[-1] = rgb[1]
        b[-1] = rgb[2]

        r = "".join(r)
        g = "".join(g)
        b = "".join(b)

        r = int(r, 2)
        g = int(g, 2)
        b = int(b, 2)

        pixels[2][2] = r
        pixels[2][1] = g
        pixels[2][0] = b
