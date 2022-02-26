import cv2
import numpy as np
import base64
from .protocol import Protocol

EOF = "<!EOF!>"
EOF_binary = "00111100001000010100010101001111010001100010000100111110"  # <!EOF!> in binary

class LSB:
    @staticmethod
    def encode(data, image, protocol):
        binary_text = ""
        if protocol.encoding == "ASCII":
            binary_text = list(format(ord(i), 'b') for i in data)
        elif protocol.encoding == "base64":
            bytes = base64.b64decode(data)
            binary_text = ["{:08b}".format(i) for i in bytes]
        elif protocol.encoding == "file":
            with open(data, "rb") as f:
                bytes = f.read()
                binary_text = ["{:08b}".format(i) for i in bytes]
        else:
            return

        for byte in range(len(binary_text)):
            for i in range(8 - len(binary_text[byte])):
                byte_list = list(binary_text[byte])
                byte_list.insert(0, "0")
                binary_text[byte] = "".join(byte_list)

        binary_text = "".join(binary_text)+EOF_binary
        if protocol.use_more_bits:
            binary_text = [binary_text[i:i + 2] for i in range(0, len(binary_text), 2)]
        binary_text = [binary_text[i:i + 3] for i in range(0, len(binary_text), 3)]
        print(binary_text)
        for i in range(2):
            binary_text.insert(0, None)

        image_matrix = cv2.imread(image)

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
    def decode(image):
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

        res = ""
        if protocol.use_more_bits:
            binary = binary[12:-len(EOF_binary)]
        else:
            binary = binary[6:-len(EOF_binary)]
        if protocol.encoding == "ASCII":
            binary = [binary[i:i + 8] for i in range(0, len(binary), 8)]
            for byte in binary:
                res += chr((int(byte, 2)))
        elif protocol.encoding == "base64":
            bytes = int(binary, 2).to_bytes(len(binary) // 8, byteorder='big')
            res = base64.b64encode(bytes).decode()
        # elif protocol.encoding == "file":
        #     with open("decoded", "wb") as f:
        #         bytes = int(binary, 2).to_bytes(len(binary) // 8, byteorder='big')
        #         f.write(bytes)
        else:
            return
        return res