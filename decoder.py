import cv2
import numpy as np

image = input("image: ")
image_matrix = cv2.imread(image)
EOF = "<!EOF!>"
EOF_binary = "00111100001000010100010101001111010001100010000100111110" # <!EOF!> in binary

res = ""
binary = ""
done = False
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

binary = [binary[i:i + 8] for i in range(0, len(binary), 8)]
print(binary)
res = ""
for byte in binary:
    res += chr((int(byte, 2)))
print(res[:-len(EOF)])