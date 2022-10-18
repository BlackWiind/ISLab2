import sys
import gost

# with open("hello", "rb") as rb:
#     data = rb.read()
#
# with open("key", "rb") as rb:
#     key = rb.read()
#
# cripted_file = gost.ecb(key, data, True)
# cripted_file = gost.ecb(key, cripted_file, False)
# print(cripted_file)
# cripted_file = gost.cbc_encrypt(key, data)
# cripted_file = gost.cbc_decrypt(key, cripted_file)
# print(cripted_file)
# cripted_file = gost.crt(key, data)
# cripted_file = gost.crt(key, cripted_file)
# print(cripted_file)
# cripted_file = gost.ofb_encrypt(key, data)
# cripted_file = gost.ofb_decrypt(key, cripted_file)
# print(cripted_file)


def main(message_path, key_path, mode):
    """

    :param message_path: путь к файлу с сообщением
    :param key_path: путь к файлу с ключем
    :param mode: режим(ecbc/ecbd - режим ecb шифрование/дешифровка,
                       cbce/cbcd - режим cbc шифрование/дешифровка,
                       crt - режим crt, для расшифровки используется этот же ключ,
                       ofbe/ofbd - режим ofb шифрование/дешифровка)
    :return: зашифрованное или расшифрованное сообщение в консоль и в файл "newfile"


    """
    print("print")
    if not sys.argv[1]:
        print("Не указан путь к файлу с сообщением")
        return
    with open(message_path, "rb") as rb:
        data = rb.read()

    if not sys.argv[2]:
        print("Не указан путь к файлу с ключем")
        return
    with open(key_path, "rb") as rb:
        key = rb.read()

    if not sys.argv[3]:
        print("Не указан режим")
        return
    #param = sys.argv[3]
    match mode:
        case "ecbc":
            cripted_file = gost.ecb(key, data, True)
        case "ecbd":
            cripted_file = gost.ecb(key, data, False)
        case "cbce":
            cripted_file = gost.cbc_encrypt(key, data)
        case "cbcd":
            cripted_file = gost.cbc_decrypt(key, data)
        case "crt":
            cripted_file = gost.crt(key, data)
        case "ofbe":
            cripted_file = gost.ofb_encrypt(key, data)
        case "ofbd":
            cripted_file = gost.ofb_decrypt(key, data)
        case _:
            print("Не правильно введён режим")
            return
    print(f"Результат = {cripted_file}")
    with open("newfile", "wb") as fh:
        fh.seek(0)
        fh.write(cripted_file)



if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
    main("newfile", "key", "ecbd")