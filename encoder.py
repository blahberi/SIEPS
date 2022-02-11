import cv2
import numpy as np

image = input("image: ")
text = input("text: ")+"<!EOF!>"

binary_text = list(format(ord(x), 'b')for x in text)

for byte in range(len(binary_text)):
    for i in range(8 - len(binary_text[byte])):
        byte_list = list(binary_text[byte])
        byte_list.insert(0, "0")
        binary_text[byte] = "".join(byte_list)

binary_text = "".join(binary_text)
binary_text = [binary_text[start:start+3] for start in range(0, len(binary_text), 3)]

print(binary_text)

image_matrix = cv2.imread(image)
for i in range(len(binary_text)):
    r = list(np.binary_repr(image_matrix[i//len(image_matrix[0])][i%len(image_matrix[0])][2]))
    g = list(np.binary_repr(image_matrix[i//len(image_matrix[0])][i%len(image_matrix[0])][1]))
    b = list(np.binary_repr(image_matrix[i//len(image_matrix[0])][i%len(image_matrix[0])][0]))

    rgb = r, g, b
    for j in range(len(binary_text[i])):
        rgb[j][-1:] = binary_text[i][j]

    r = "".join(r)
    g = "".join(g)
    b = "".join(b)

    r = int(r, 2)
    g = int(g, 2)
    b = int(b,2)

    image_matrix[i//len(image_matrix[0])][i%len(image_matrix[0])][2] = r
    image_matrix[i//len(image_matrix[0])][i%len(image_matrix[0])][1] = g
    image_matrix[i//len(image_matrix[0])][i%len(image_matrix[0])][0] = b

cv2.imwrite("output.png", image_matrix)