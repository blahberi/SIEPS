from steganography.lsb import LSB

LSB.encode("uAtbK6WZV00yJ3lnXpeEZGr+u6YcRBgW9oYLwrXHXg4QNeapoOD3FdMB8rJK5+wz", "unknown.png", "base64")
print(LSB.decode("output.png", "base64"))