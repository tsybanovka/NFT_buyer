from security.crypt_functions import *

def get_data(): # Функция для получения ключа
    key = b''           # переменная, хранящая ключ, который вы вводите
    data = b''          # переменная, хранящая зашифрованные данные файла
    with open("key.pk", "rb") as file: #
        for v in file.readlines():     # чтение файла
            data += v                  #
    is_key_true = False # проверка правильный ли ключ введен
    while not is_key_true: # Получать новый ключ пока не подойдет
        key = bytes(input("Введите пожалуйста ключ (0 - чтобы выйти): ").encode("utf-8")) # вы вводите ключ и он переводится в байты
        if key == b'0': # если вы решили выйти, то все переменные обнуляются и заканчивается цикл
            return b'', b'', False # возвращаются пустые значения и решение пользователя не продолжать работу
        try:
            data = aes_decrypt(key, data) #   попытка дешифрации
            is_key_true = True
        except:
            print("\nНеправильный ключ\n")        # если не удалась, то сообщить о неправильном ключе и возврат в начало цикла

    return data, key, is_key_true

def end_work_with_data(data:str):
    key = get_random_password()
    print(f"Ваш новый ключ: >>{key}<<")
    with open("spare.txt", "w") as file:   #
        file.write(key)                    #   резевная запись ключа

    with open("key.pk", "wb") as file:
        file.write(aes_encrypt(bytes(key.encode("utf-8")), data))

def write_new_data(data:str):
    key = get_random_password()
    print(f"Ваш новый ключ: >>{key}<<")

    with open("key.pk", "wb") as file:
        file.write(aes_encrypt(bytes(key.encode("utf-8")), data))