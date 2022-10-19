import sys
import gost


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

    if not message_path:
        print("Не указан путь к файлу с сообщением")
        return
    with open(message_path, "rb") as rb:
        data = rb.read()

    if not key_path:
        print("Не указан путь к файлу с ключем")
        return
    with open(key_path, "rb") as rb:
        key = rb.read()

    if not mode:
        print("Не указан режим")
        return

    print(f"Данные взятые из файла {message_path}: {data}\n"
          f"Ключ {key}\n"
          f"Выбран режим {mode}")

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
    print(f"Результат = {cripted_file} будет записан в newfile\n")
    with open("newfile", "wb") as fh:
        fh.seek(0)
        fh.write(cripted_file)



if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
    # Превью всех режимов
    # main("hello", "key", "ecbc")
    # main("newfile", "key", "ecbd")
    # main("hello", "key", "cbce")
    # main("newfile", "key", "cbcd")
    # main("hello", "key", "crt")
    # main("newfile", "key", "crt")
    # main("hello", "key", "ofbe")
    # main("newfile", "key", "ofbd")

