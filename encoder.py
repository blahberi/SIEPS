import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

image = input("image: ")
mode = input("do you want to encode a (f)ile or (t)ext? ")
mode2 = input("do you want to encrypt (y or n)? ")
if mode == "f":
    if mode2 == "n":
        file = input("file to encode: ")
        f = open(file, "rb")
        t = file.split(".")[-1]
        text = t + " split " + f.read().decode("latin-1") + "<!EOF!>"
        f.close()
    elif mode2 == "y":
        file = input("file to encode: ")
        f = open(file, "rb")
        t = file.split(".")[-1]
        key = get_random_bytes(16)
        plaintext = (t + " split " + f.read().decode("latin-1")).encode("utf-8")
        print("key: ", base64.b64encode(key).decode())
        cipher = AES.new(key, AES.MODE_EAX)
        ciphered_data, tag = cipher.encrypt_and_digest(plaintext)
        text = " encrypted " + cipher.nonce.decode("latin-1") + " split2 " + tag.decode("latin-1") + " split2 " + ciphered_data.decode("latin-1") + "<!EOF!>"
if mode == "t":
    if mode2 == "n":
        text = input("text: ") + "<!EOF!>"
    elif mode2 == "y":
        plain_text = input("text: ").encode("utf-8")
        key = get_random_bytes(16)
        print("key: ", base64.b64encode(key).decode())
        cipher = AES.new(key, AES.MODE_EAX)
        ciphered_data, tag = cipher.encrypt_and_digest(plain_text)
        text = " encrypted " + cipher.nonce.decode("latin-1") + " split2 " + tag.decode("latin-1") + " split2 " + ciphered_data.decode("latin-1") + "<!EOF!>"
if (mode != "f" and mode != "t") or (mode2 != "y" and mode2 != "n"):
    print("Error: no mode specified")

binary_text = list(format(ord(x), 'b')for x in text)
for byte in range(len(binary_text)):
    for i in range(8 - len(binary_text[byte])):
        byte_list = list(binary_text[byte])
        byte_list.insert(0, "0")
        binary_text[byte] = "".join(byte_list)

binary_text = "".join(binary_text)
image_matrix = cv2.imread(image)

k = int(np.ceil(len(binary_text)/(image_matrix.shape[0]*image_matrix.shape[1]*image_matrix.shape[2])))
if k > 8:
    print("Error: encoded file too big")
    exit()

binary_text = [binary_text[start:start+3*k] for start in range(0, len(binary_text), 3*k)]

for i in range(len(binary_text)):
    binary_text[i] = [binary_text[i][start:start + k] for start in range(0, len(binary_text[i]), k)]

bin_k = np.binary_repr(k)

while len(bin_k) < 3:
    bin_k = "0" + bin_k
image_matrix[0][0][2] = str(image_matrix[0][0][2])[:-1] + str(bin_k[0])
image_matrix[0][0][1] = str(image_matrix[0][0][1])[:-1] + str(bin_k[1])
image_matrix[0][0][0] = str(image_matrix[0][0][0])[:-1] + str(bin_k[2])

for i in range(1, len(binary_text) + 1):
    r = list(np.binary_repr(image_matrix[i // len(image_matrix[0])][i % len(image_matrix[0])][2]))
    g = list(np.binary_repr(image_matrix[i // len(image_matrix[0])][i % len(image_matrix[0])][1]))
    b = list(np.binary_repr(image_matrix[i // len(image_matrix[0])][i % len(image_matrix[0])][0]))

    rgb = r, g, b
    for j in range(len(binary_text[i-1])):
        rgb[j][-k:] = binary_text[i-1][j]

    r = "".join(r)
    g = "".join(g)
    b = "".join(b)

    r = int(r, 2)
    g = int(g, 2)
    b = int(b, 2)

    image_matrix[i // len(image_matrix[0])][i % len(image_matrix[0])][2] = r
    image_matrix[i // len(image_matrix[0])][i % len(image_matrix[0])][1] = g
    image_matrix[i // len(image_matrix[0])][i % len(image_matrix[0])][0] = b

cv2.imwrite("output.png", image_matrix)