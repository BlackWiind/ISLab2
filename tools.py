from bitarray import bitarray
from math import pow
SBlocks = [[12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1],
       [6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15],
       [11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0],
       [12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11],
       [7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12],
       [5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0],
       [8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7],
       [1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2]]


def read(path, n):
    '''read for n bits from file'''
    filebits = bitarray()
    with open(path, 'rb') as fh:
        filebits.fromfile(fh)
    #print(filebits)
    # f = open(path)
    # filebits = bitarray()
    # filebits.fromfile(f)
    bits = []
    if len(filebits) == n:
        bits = [filebits]
    else:
        for i in range(0, len(filebits), n):
            begin = i;
            end = i + n
            bits.append(filebits[begin: end])
    #print(bits)
    return bits


def writeBits(bits):
    bytes = bits.tobytes()
    f = open("newfile", "wb")
    f.seek(0); f.write(bytes)
def cycleShift11(bits):
    l = bits[: 11]; r = bits[11: ]
    result = bitarray()
    result.extend(r); result.extend(l)
    return result
def toQuart(bits):
    pattern = '0000'[len(bits): ]
    result = bitarray(pattern)
    result.extend(bits)
    return result
def replaceS(bits):
    indexes = []
    for i in range(0, len(bits) + 4, 4):
        if i != 0: indexes.append(bit2int(bits[abs(4 - i): i]))
    result, s = bitarray(), bitarray(); k = 0
    for indx in indexes:
        value = SBlocks[k][indx]
        s = int2bit(value)
        if len(s) < 4: s = toQuart(s)
        result.extend(s)
        k += 1
    return result

def int2bit(n):
    sbits = bin(n)[2:]; bits = bitarray()
    for bit in sbits:
        if bit == '1': bits.append(True)
        else: bits.append(False)
    return bits
def bit2int(bits): return int(bits.to01(), 2)