import os

from SIEPS.lsb import LSB
from SIEPS.protocol import Protocol
from SIEPS.AES.aes import AESCipher

protocol = Protocol(use_more_bits=True, use_different_encoding=True, encrypt=True, encoding="custom", custom_encoding="md")
key = os.urandom(32)
LSB.encode("README.md", "unknown.png", protocol, AESkey=key)
print(LSB.decode("encoded.png", AESkey=key))