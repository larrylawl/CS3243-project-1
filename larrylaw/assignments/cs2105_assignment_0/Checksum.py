import zlib
import sys

fileName = sys.argv[1]

with open(fileName, "rb") as f:
    bytes = f.read()
checksum = zlib.crc32(bytes)
print(checksum)
