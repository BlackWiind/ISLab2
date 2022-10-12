from tools import read
from bitarray import bitarray



def foo():
    a = bitarray()
    path = "/hello"
    with open(path, 'rb') as fh:
        a.fromfile(fh)
    print(fh)