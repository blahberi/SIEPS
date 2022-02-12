import cv2
import numpy as np

image = input("image: ")
mode = input("do you want to encode a (f)ile or (t)ext? ")
if mode == "f":
    file = input("file to encode: ")
    f = open(file, "rb")
    t = file.split(".")[-1]
    text = t + " split " + f.read().decode("latin1") + "<!EOF!>"
    f.close()
if mode == "t":
    text = input("text: ") + "<!EOF!>"
if mode != "f" and mode != "t":
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
image_matrix[0][0][2] = bin_k[0]
image_matrix[0][0][1] = bin_k[1]
image_matrix[0][0][0] = bin_k[2]

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