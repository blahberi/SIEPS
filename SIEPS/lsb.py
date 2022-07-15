import cv2
import numpy as np
import base64
from .protocol import Protocol
from .AES.aes import AESCipher
import zlib

EOF = "<!EOF!>"
EOF_binary = "00111100001000010100010101001111010001100010000100111110"  # <!EOF!> in binary
ENCODING = "<!ENCODING!>"
ENCODING_binary = "001111000010000101000101010011100100001101001111010001000100100101001110010001110010000100111110"  # <!ENCODING!> in binary


def binary_to_bytes(binary_string):
    bytes_string = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
    bytes_array = []
    for byte_string in bytes_string:
        bytes_array.append(int(byte_string, 2))
    bytes_array = bytearray(bytes_array)
    res = bytes(bytes_array)
    return res


class LSB:
    @staticmethod
    def encode(data, image, protocol, AESkey=None):
        _bytes = None
        image_matrix = cv2.imread(image)
        if image_matrix is None:
            return False
        if protocol.encoding == "ASCII":
            _bytes = data.encode()
        elif protocol.encoding == "base64":
            _bytes = base64.b64decode(data)
        elif protocol.encoding == "binary":
            _bytes = data
        elif protocol.encoding in ("png", "mp4", "pdf" "exe", "zip"):
            with open(data, "rb") as f:
                _bytes = f.read()
        elif protocol.encoding == "custom":
            with open(data, "rb") as f:
                _bytes = f.read()
        if protocol.encrypt:
            _bytes = AESCipher(AESkey).encrypt(_bytes)
        sussy_bytes = zlib.compress(_bytes, 9)
        if protocol.compress == "auto":
            if len(sussy_bytes) < len(_bytes):
                protocol.compress = True
            else:
                protocol.compress = False
        if protocol.compress:
            _bytes = sussy_bytes

        if protocol.encoding == "custom":
            _bytes = protocol.custom_encoding.encode() + ENCODING.encode() + _bytes

        binary_text = ["{:08b}".format(i) for i in _bytes]

        for byte in range(len(binary_text)):
            for i in range(8 - len(binary_text[byte])):
                byte_list = list(binary_text[byte])
                byte_list.insert(0, "0")
                binary_text[byte] = "".join(byte_list)

        binary_text = "".join(binary_text) + EOF_binary
        if protocol.bits == "auto":
            protocol.bits = int(np.ceil(len(binary_text)/(image_matrix.shape[0]*image_matrix.shape[1]*image_matrix.shape[2])))
        binary_text = [binary_text[i:i + protocol.bits] for i in range(0, len(binary_text), protocol.bits)]
        binary_text = [binary_text[i:i + 3] for i in range(0, len(binary_text), 3)]
        for i in range(3):
            binary_text.insert(0, None)

        protocol.write_protocol(image_matrix)

        for i in range(3, len(binary_text)):
            r = list(np.binary_repr(image_matrix[i // len(image_matrix[0])][i % len(image_matrix[0])][2]))
            g = list(np.binary_repr(image_matrix[i // len(image_matrix[0])][i % len(image_matrix[0])][1]))
            b = list(np.binary_repr(image_matrix[i // len(image_matrix[0])][i % len(image_matrix[0])][0]))

            rgb = r, g, b
            for j in range(len(binary_text[i])):
                binary_text[i][j] = binary_text[i][j][::-1]
                if len(binary_text[i][j][::-1]) < protocol.bits:
                    rgb[j][-1 * len(binary_text):] = binary_text[i][j]
                else:
                    rgb[j][-1*protocol.bits:] = binary_text[i][j]

            r = "".join(r)
            g = "".join(g)
            b = "".join(b)

            r = int(r, 2)
            g = int(g, 2)
            b = int(b, 2)

            image_matrix[i // len(image_matrix[0])][i % len(image_matrix[0])][2] = r
            image_matrix[i // len(image_matrix[0])][i % len(image_matrix[0])][1] = g
            image_matrix[i // len(image_matrix[0])][i % len(image_matrix[0])][0] = b

        cv2.imwrite("encoded.png", image_matrix)

    @staticmethod
    def decode(image, AESkey=None):
        image_matrix = cv2.imread(image)

        protocol = Protocol()
        protocol.read_protocol(image_matrix)

        binary = ""
        done = False
        if image_matrix is None:
            return
        for row in image_matrix:
            for pixel in row:
                rgb = pixel[2], pixel[1], pixel[0]
                for color in rgb:
                    color = np.binary_repr(color, 8)
                    for i in range(protocol.bits):
                        binary += color[-1 * (i + 1)]
                        if binary[-len(EOF_binary):] == EOF_binary:
                            done = True
                            break
                    if done:
                        break
                if done:
                    break
            if done:
                break

        binary = binary[9*protocol.bits:-len(EOF_binary)]

        custom_encoding_bytes = None
        if protocol.use_different_encoding:
            if protocol.encoding == "custom":
                custom_encoding_binary = binary[:binary.find(ENCODING_binary)]
                custom_encoding_bytes = binary_to_bytes(custom_encoding_binary)
                binary = binary[binary.find(ENCODING_binary) + len(ENCODING_binary):]

        _bytes = binary_to_bytes(binary)
        if protocol.compress:
            _bytes = zlib.decompress(_bytes)
        if protocol.encrypt:
            _bytes = AESCipher(AESkey).decrypt(_bytes)

        if protocol.use_different_encoding:
            if protocol.encoding == "custom":
                protocol.custom_encoding = custom_encoding_bytes.decode()

        if protocol.encoding == "ASCII":
            return _bytes.decode()
        elif protocol.encoding == "base64":
            return base64.b64encode(_bytes).decode()
        elif protocol.encoding == "binary":
            return _bytes
        elif protocol.encoding in ("png", "mp4", "pdf" "exe", "zip"):
            with open(f"output.{protocol.encoding}", "wb") as f:
                f.write(_bytes)
        elif protocol.encoding == "custom":
            with open(f"output.{protocol.custom_encoding}", "wb") as f:
                f.write(_bytes)
        if protocol.encrypt:
            _bytes = AESCipher(AESkey).encrypt(_bytes)
        else:
            return
