from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os, random

def aes_encrypt(key:bytes, plaintext:str):
    """Шифрует данные с использованием AES-256 в режиме CBC."""
    # Генерация случайного IV
    iv = os.urandom(16)
    # Создание объекта шифрования
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    # Дополнение данных
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    # Шифрование
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext

def aes_decrypt(key:bytes, ciphertext:bytes):
    """Расшифровывает данные, зашифрованные с помощью AES-256 в режиме CBC."""
    # Извлечение IV
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    # Создание объекта расшифрования
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    # Расшифрование
    decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    # Удаление дополнения
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    return unpadded_data.decode()

def get_random_password():
    def get_random_char():
        return chr(random.randint(32, 126))
    ans = ""
    for i in range(16):
        ans += get_random_char()
    return ans

