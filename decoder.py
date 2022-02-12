import cv2
import numpy as np
from Crypto.Cipher import AES
import struct
import base64
def convert_string_to_bytes(string):
    bytes = b''
    for i in string:
        bytes += struct.pack("B", ord(i))
    return bytes
image = input("image: ")
image_matrix = cv2.imread(image)
EOF = "<!EOF!>"
EOF_binary = "00111100001000010100010101001111010001100010000100111110" # <!EOF!> in binary
res = ""
binary = ""
done = False
mode = input("is it encoded using the (b)ad method or the (g)ood method? ")
if mode == "g":
    for i, row in enumerate(image_matrix):
        for j, pixel in enumerate(row):
            rgb = pixel[2], pixel[1], pixel[0]
            if [i, j] == [0, 0]:
                k = str(pixel[2])[-1] + str(pixel[1])[-1] + str(pixel[0])[-1]
                k = int(k, 2)
            else:
                for color in rgb:
                    binary += np.binary_repr(color)[-k:]
                    if binary[-len(EOF_binary):] == EOF_binary:
                        done = True
                        break
            if done:
                break
        if done:
            break
if mode == "b":
    for row in image_matrix:
        for pixel in row:
            rgb = pixel[2], pixel[1], pixel[0]
            for color in rgb:
                binary += np.binary_repr(color)[-1:]
                if binary[-len(EOF_binary):] == EOF_binary:
                    done = True
                    break
            if done:
                break
        if done:
            break
if not done:
    print("Warning: no EOF found")

binary = [binary[i:i + 8] for i in range(0, len(binary), 8)]
res = ""
for byte in binary:
    res += chr((int(byte, 2)))
if done:
    res = res[:-len(EOF)]
if res[:11] == " encrypted ":
    res = res[11:]
    key = base64.b64decode(input("key: "))
    nonce = res.split(" split2 ")[0]
    tag = res.split(" split2 ")[1]
    ciphered_data = res.split(" split2 ")[2]
    cipher = AES.new(key, AES.MODE_EAX, nonce.encode("latin-1"))
    res = cipher.decrypt_and_verify(ciphered_data.encode("latin-1"), tag.encode("latin-1")).decode("utf-8")
split = res.split(" split ")
if len(split) == 1:
    print(res)
if len(split) == 2:
    f = open("decoded" + "." + split[0], "wb")
    f.write(split[1].encode("latin-1"))
    f.close()