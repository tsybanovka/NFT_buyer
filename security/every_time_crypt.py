import time

from security.crypt_functions import aes_decrypt, aes_encrypt
from random import randint
from time import sleep
from os import urandom
from threading import Event

def start_crypt(key:bytes, event:Event): # key - ключ, event - переменная для проверки состояния главного потока
    """Считывание зашифрованных данных из файла"""
    data = b''
    with open("key.pk", "rb") as file:
        data += file.readline()

    # Расшифровка данных
    data = aes_decrypt(key, data)

    while not event.isSet():
        key = urandom(16)
        with open("key.pk", "wb") as file:
            file.write(aes_encrypt(key, data))
        was = randint(3600, 7200)
        i = 0
        while i < was and not event.isSet():
            time.sleep(1)
            i += 1
