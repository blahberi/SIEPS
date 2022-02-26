from SIEPS.lsb import LSB
from SIEPS.protocol import Protocol

protocol = Protocol(use_more_bits=True)
LSB.encode("Hello World!", "unknown.png", protocol)
print(LSB.decode("encoded.png"))