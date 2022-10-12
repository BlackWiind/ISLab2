from bitarray import bitarray
from tools import *
import sys


def main(msg, key, mode=False):
    bits = read(msg, 64);
    outbits = bitarray()
    print(f"file = {bits}")
    keys = read(key, 32)
    print(f"key = {keys}")
    for subbits in bits:
        outbits.extend(coding(subbits, keys, mode))
    print(outbits)
    writeBits(outbits)


def coding(bits, keys, mode):
    leftBits, rightBits = bits[:32], bits[32:]
    if mode == False:
        for i in range(3):
            for j in range(8):
                rightBits = rightBits ^ keys[j]
                rightBits = replaceS(rightBits)
                rightBits = cycleShift11(rightBits)
                result = leftBits ^ rightBits
                rightBits = leftBits
                leftBits = result
        for j in range(7, -1, -1):
            rightBits = rightBits ^ keys[j]
            rightBits = replaceS(rightBits)
            rightBits = cycleShift11(rightBits)
            result = leftBits ^ rightBits
            if (j != 0):
                rightBits = leftBits
                leftBits = result
            if (j == 0):  rightBits = result

    if mode == True:
        for j in range(7, -1, -1):
            rightBits = rightBits ^ keys[j]
            rightBits = replaceS(rightBits)
            rightBits = cycleShift11(rightBits)
            result = leftBits ^ rightBits
            rightBits = leftBits
            leftBits = result
        for i in range(3):
            for j in range(8):
                rightBits = rightBits ^ keys[j]
                rightBits = replaceS(rightBits)
                rightBits = cycleShift11(rightBits)
                result = leftBits ^ rightBits
                if ((i + 2) * (j + 1)) != 32:
                    rightBits = leftBits
                    leftBits = result
                if ((i + 2) * (j + 1)) == 32:
                    rightBits = result
    leftBits.extend(rightBits)
    return leftBits


#msg = sys.argv[1]
msg = 'hello'
mode = 0
# if sys.argv[2] == '0':
#     mode = False
# else:
#     mode = True
main("hello", "key", mode)