import sys

# Slice string with every 8 bits
# Convert to decimal
# Add to result

fullBit = sys.argv[1]

firstByte = str(int(fullBit[0:8], 2))
secondByte = str(int(fullBit[8:16], 2))
thirdByte = str(int(fullBit[16:24], 2))
fourthByte = str(int(fullBit[24:32], 2))

result = firstByte + "." + secondByte + "." + thirdByte + "." + fourthByte
print(result)


