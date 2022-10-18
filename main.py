import math
import sys
import numpy.random
import itertools
from bitarray import bitarray
import pygost

matrix = (
    (4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3),
    (14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9),
    (5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11),
    (7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3),
    (6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2),
    (4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14),
    (13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12),
    (1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12),
)


# def bits_len(text, encoding='utf-8', errors='surrogatepass'):
#     # Перевод текста в массив битов
#     bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
#     bits = bits.zfill(8 * ((len(bits) + 7) // 8))
#     return len(bits)


def get_out(inright, key):
    out = 0
    temp = (inright + key) % (1 << 32)
    # Сдвиг суммы ключа и правой позиции
    for i in range(8):
        phonetic = (temp >> (4 * i)) & 0b1111
        '''
        Определение ячейки
        Сдвиг на n бит и выбор пересечения
        '''
        out |= (matrix[i][phonetic] << (4 * i))
        '''
        Второй бит устанавливается в 0
        Сдвиг влево на n бит
        '''
    out = ((out >> 21) | (out << 11)) & 0xFFFFFFFF
    # Пересечение бита и объединения множеств со сдвигами
    return out


def crypt_operation(inleft, inright, key):
    outleft = inright
    # Присваиваем левому выходу правые входные данные
    outright = inleft ^ get_out(inright, key)
    # Исключаем пересечение
    return outleft, outright

def decrypt_operation(inleft, inright, key):
    outright = inright ^ get_out(inleft, key)
    # Присваиваем левому выходу правые входные данные
    outleft = inleft
    # Исключаем пересечение
    return outright, outleft


class Gost:
    def __init__(self):
        self.key = [None] * 8

    def set_key(self, key):
        for i in range(8):
            self.key[i] = (key >> (32 * i)) & 0xFFFFFFFF
        # Пересечние сдвига ключа вправо на 32 бита с десятизначным числом
        print("Key:", self.key)

    def crypt_ecb(self, text):
        #text = int(text.encode('utf-8').hex(), 16)
        #print(text)
        text_left = text >> 32
        text_right = text & 0xFFFFFFFF
        # print(text_left)
        # print(text_right)
        # Разбитие текста с помощью побитового сдвига
        for q in range(24):
            text_left, text_right = crypt_operation(text_left, text_right, self.key[q % 8])
        for q in range(8):
            text_left, text_right = crypt_operation(text_left, text_right, self.key[7 - q])
        # 32 цикла с различными ключами
        hash = (text_left << 32) | text_right
        return hash

    def decrypt_ecb(self, text):
        text_left = text >> 32
        text_right = text & 0xFFFFFFFF
        # Разбитие текста с помощью побитового сдвига
        for q in range(8):
            text_left, text_right = decrypt_operation(text_left, text_right, self.key[q])
        for q in range(24):
            text_left, text_right = decrypt_operation(text_left, text_right, self.key[(7 - q) % 8])
        # 32 цикла с различными ключами
        message = (text_left << 32) | text_right
        message = bytes.fromhex(hex(message)[2:]).decode()

        return message




# a = Gost()
# a.set_key(0x1111222233334444555566667777888899990000aaaabbbbccccddddeeeeffff)
# hash = a.crypt_ecb('abrakadabraadasdasdasdasdasadhashdahdhasldhah21412541515151235aqfasfasdaфыввввввввввфыasfna290e93u5023ttgjh2848ghsifgsgs')
# print(f"Зашифрованное сообщение = {hash}")
# hash = a.decrypt_ecb(hash)
#
# print(f"Расшифрованное сообщение = {hash}")


def round_of_feistel_cipher(left_part, right_part, key):
    temp = right_part
    result = right_part ^ key
    out = bitarray()
    for i in range(8):
        block_4_bit = result[:4]

        phonetic = result[:4]
        '''
        Определение ячейки
        Сдвиг на n бит и выбор пересечения
        '''
        out.append(matrix[i][phonetic])
        del result[:4]
        '''
        Второй бит устанавливается в 0
        Сдвиг влево на n бит
        '''
    out = ((out >> 21) | (out << 11)) & 0xFFFFFFFF
    # Пересечение бита и объединения множеств со сдвигами
    return temp, left_part ^ out



def read_file(path, n):
    # file_array = bitarray()
    # with open(path, 'rb') as fh:
    #     file_array.fromfile(fh)
    # print(len(file_array))
    # bits = []
    # if len(file_array) == n:
    #     bits = [file_array]
    # else:
    #     count = math.ceil(len(file_array) / n)
    #     for i in range(0, count):
    #         block_bits = bitarray(n)
    #         block_bits.setall(0)
    #         file_array.reverse()
    #         while len(file_array) < n:
    #             file_array.append(0)
    #         file_array.reverse()
    #         block_bits |= file_array[:n]
    #         del file_array[: n]
    #         bits.append(block_bits)
    text = 0
    with open(path, "r") as fh:
        text = fh.read()
        text = int(text.encode('utf-8').hex(), 16)
    return text


def crypt_ecb(message, key):
    crypto = bitarray()
    for msg in message:
        print(msg)
        msg_left = msg[32:]
        print(msg_left)
        msg_right = msg[:32]
        print(msg_right)

        for q in range(8):
            msg_left, msg_right = round_of_feistel_cipher(msg_left, msg_right, key[q])
            #msg_left, msg_right = decrypt_operation(msg_left, msg_right, key[q])
        for q in range(24):
            msg_left, msg_right = round_of_feistel_cipher(msg_left, msg_right, key[(7 - q) % 8])
            #msg_left, msg_right = decrypt_operation(msg_left, msg_right, key[(7 - q) % 8])
        # 32 цикла с различными ключами
        #message = (msg_left << 32) | msg_right
        #message = bytes.fromhex(hex(message)[2:]).decode()
        crypto.append((msg_left << 32) | msg_right)

    return crypto


def main():
    # message = read_file("hello", 64)
    # key = read_file("key", 32)
    # a = Gost()
    # a.set_key(read_file("key", 32))
    # crypted_message = 0
    # message = 12345678901234567456456456456
    # print(sys.getsizeof(message))
    # while message != 0:
    #     # msg = message << 64 & 0xFFFFFFFF
    #     # #print(f"msg = {msg}")
    #     # print(sys.getsizeof(msg))
    #     message >>= 64
    #     print(f"mesaage = {message}")
    #     # print(sys.getsizeof(message))
    #     # crypted_message = crypted_message >> a.crypt_ecb(msg)
    # #print(crypted_message)
    # #print(msg)
    # #print(key)
    print(pygost.__file__)


if __name__ == '__main__':
    main()