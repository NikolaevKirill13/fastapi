import os
import hashlib


def pass_gen(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    password = (salt + key).hex()
    # Получение значений обратно
    # salt_from_storage = password[:32]
    # key_from_storage = password[32:]
    return password
