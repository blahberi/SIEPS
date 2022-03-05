import cv2
import numpy as np
import base64
from .protocol import Protocol
from .AES.aes import AESCipher

EOF = "<!EOF!>"
EOF_binary = "00111100001000010100010101001111010001100010000100111110"  # <!EOF!> in binary
ENCODING = "<!ENCODING!>"
ENCODING_binary = "001111000010000101000101010011100100001101001111010001000100100101001110010001110010000100111110"  #<!ENCODING!> in binary


def binary_to_bytes(binary_string):
    bytes_string = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
    bytes_array = []
    for byte_string in bytes_string:
        bytes_array.append(int(byte_string, 2))
        print(int(byte_string, 2))
    bytes_array = bytearray(bytes_array)
    res = bytes(bytes_array)
    return res


class LSB:
    @staticmethod
    def encode(data, image, protocol, AESkey=None):
        bytes = None
        if protocol.encoding == "ASCII":
            bytes = data.encode()
        elif protocol.encoding == "base64":
            bytes = base64.b64decode(data)
        elif protocol.encoding in ("png", "jpg", "mp4", "pdf" "exe", "zip"):
            with open(data, "rb") as f:
                bytes = f.read()
        elif protocol.encoding == "custom":
            with open(data, "rb") as f:
                bytes = f.read()
        if protocol.encrypt:
            bytes = AESCipher(AESkey).encrypt(bytes.decode())

        if protocol.encoding == "custom":
            bytes = protocol.custom_encoding.encode() + ENCODING.encode() + bytes

        binary_text = ["{:08b}".format(i) for i in bytes]

        for byte in range(len(binary_text)):
            for i in range(8 - len(binary_text[byte])):
                byte_list = list(binary_text[byte])
                byte_list.insert(0, "0")
                binary_text[byte] = "".join(byte_list)

        binary_text = "".join(binary_text)+EOF_binary
        if protocol.use_more_bits:
            binary_text = [binary_text[i:i + 2] for i in range(0, len(binary_text), 2)]
        binary_text = [binary_text[i:i + 3] for i in range(0, len(binary_text), 3)]
        for i in range(2):
            binary_text.insert(0, None)

        image_matrix = cv2.imread(image)
        if image_matrix is None:
            return False

        protocol.write_protocol(image_matrix)

        for i in range(2, len(binary_text)):
            r = list(np.binary_repr(image_matrix[i // len(image_matrix[0])][i % len(image_matrix[0])][2]))
            g = list(np.binary_repr(image_matrix[i // len(image_matrix[0])][i % len(image_matrix[0])][1]))
            b = list(np.binary_repr(image_matrix[i // len(image_matrix[0])][i % len(image_matrix[0])][0]))

            rgb = r, g, b
            for j in range(len(binary_text[i])):
                if protocol.use_more_bits:
                    rgb[j][-2:] = binary_text[i][j]
                else:
                    rgb[j][-1] = binary_text[i][j]

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
        for row in image_matrix:
            for pixel in row:
                rgb = pixel[2], pixel[1], pixel[0]
                for color in rgb:
                    if protocol.use_more_bits:
                        binary += np.binary_repr(color)[-2]
                    binary += np.binary_repr(color)[-1]
                    if binary[-len(EOF_binary):] == EOF_binary:
                        done = True
                        break
                if done:
                    break
            if done:
                break

        if protocol.use_more_bits:
            binary = binary[12:-len(EOF_binary)]
        else:
            binary = binary[6:-len(EOF_binary)]

        custom_encoding_bytes = None
        if protocol.use_different_encoding:
            if protocol.encoding == "custom":
                custom_encoding_binary = binary[:binary.find(ENCODING_binary)]
                print(custom_encoding_binary)
                custom_encoding_bytes = binary_to_bytes(custom_encoding_binary)
                print(custom_encoding_bytes)
                binary = binary[binary.find(ENCODING_binary) + len(ENCODING_binary):]

        _bytes = binary_to_bytes(binary)

        if protocol.encrypt:
            _bytes = AESCipher(AESkey).decrypt(_bytes)

        if protocol.use_different_encoding:
            if protocol.encoding == "custom":
                protocol.custom_encoding = custom_encoding_bytes.decode()


        if protocol.encoding == "ASCII":
            return _bytes.decode()
        elif protocol.encoding == "base64":
            return base64.b64encode(_bytes).decode()
        elif protocol.encoding in ("png", "jpg", "mp4", "pdf" "exe", "zip"):
            with open(f"output.{protocol.encoding}", "wb") as f:
                f.write(_bytes)
        elif protocol.encoding == "custom":
            with open(f"output.{protocol.custom_encoding}", "wb") as f:
                f.write(_bytes)
        if protocol.encrypt:
            _bytes = AESCipher(AESkey).encrypt(_bytes.decode())
        else:
            return