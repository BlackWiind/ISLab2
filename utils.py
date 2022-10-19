from codecs import getdecoder
from codecs import getencoder
from sys import version_info


xrange = range if version_info[0] == 3 else xrange


def strxor(a, b):
    mlen = min(len(a), len(b))
    a, b, xor = bytearray(a), bytearray(b), bytearray(mlen)
    for i in xrange(mlen):
        xor[i] = a[i] ^ b[i]
    return bytes(xor)


_hexdecoder = getdecoder("hex")
_hexencoder = getencoder("hex")


def hexdec(data):
    return _hexdecoder(data)[0]


# def hexenc(data):
#     return _hexencoder(data)[0].decode("ascii")


# def bytes2long(raw):
#     return int(hexenc(raw), 16)


# def long2bytes(n, size=32):
#     res = hex(int(n))[2:].rstrip("L")
#     if len(res) % 2 != 0:
#         res = "0" + res
#     s = hexdec(res)
#     if len(s) != size:
#         s = (size - len(s)) * b"\x00" + s
#     return s


# def modinvert(a, n):
#     if a < 0:
#         # k^-1 = p - (-k)^-1 mod p
#         return n - modinvert(-a, n)
#     t, newt = 0, 1
#     r, newr = n, a
#     while newr != 0:
#         quotinent = r // newr
#         t, newt = newt, t - quotinent * newt
#         r, newr = newr, r - quotinent * newr
#     if r > 1:
#         return -1
#     if t < 0:
#         t = t + n
#     return t


def pad_size(data_size, blocksize):
    if data_size < blocksize:
        return blocksize - data_size
    if data_size % blocksize == 0:
        return 0
    return blocksize - data_size % blocksize


def pad2(data, blocksize):
    return data + b"\x80" + b"\x00" * pad_size(len(data) + 1, blocksize)


def unpad2(data, blocksize):
    last_block = bytearray(data[-blocksize:])
    pad_index = last_block.rfind(b"\x80")
    if pad_index == -1:
        raise ValueError("Invalid padding")
    for c in last_block[pad_index + 1:]:
        if c != 0:
            raise ValueError("Invalid padding")
    return data[:-(blocksize - pad_index)]