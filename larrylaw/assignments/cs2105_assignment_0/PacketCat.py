import sys

hasByte = True

while hasByte:
    data = sys.stdin.buffer.read1(1)
    if len(data) == 0:
        hasByte = False
    elif data == b" ":

        size = b""
        hasSizeByte = True
        while hasSizeByte:
            sizeByte = sys.stdin.buffer.read1(1)

            if sizeByte == b"B":
                hasSizeByte = False
            else:
                size += sizeByte

        payload = sys.stdin.buffer.read(int(size))
        sys.stdout.buffer.write(payload)
        sys.stdout.buffer.flush()

