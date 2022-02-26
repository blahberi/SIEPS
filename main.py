import os

from SIEPS.lsb import LSB
from SIEPS.protocol import Protocol
from SIEPS.AES.aes import AESCipher

protocol = Protocol(use_more_bits=True, encrypt=True)
key = os.urandom(32)
LSB.encode("Hi there!", "unknown.png", protocol, AESkey=key)
print(LSB.decode("encoded.png", AESkey=key))