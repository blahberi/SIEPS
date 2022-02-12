import cv2
import numpy as np

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
split = res.split(" split ")
if len(split) == 1:
    if done:
        print(res[:-len(EOF)])
    if not done:
        print(res)
if len(split) == 2:
    f = open("decoded" + "." + split[0], "wb")
    if done:
        f.write(split[1][:-len(EOF)].encode("latin-1"))
    if not done:
        f.write(split[1].encode("latin-1"))
    f.close()