###### Fibonacci ######
def fibonacci(params):
    n = params["n"]

    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    fib_array = [0, 1]
    for _ in range(2, n):
        fib_array.append(fib_array[-1] + fib_array[-2])


###### AES Encryption ######
import random
import string

import pyaes


def generate(length):
    letters = string.ascii_lowercase + string.digits
    return "".join(random.choice(letters) for i in range(length))


def aes(params):
    message_len = params["message_len"]

    message = generate(message_len)
    KEY = b"\xa1\xf6%\x8c\x87}_\xcd\x89dHE8\xbf\xc9,"

    aes = pyaes.AESModeOfOperationCTR(KEY)
    ciphertext = aes.encrypt(message)
    aes = pyaes.AESModeOfOperationCTR(KEY)
    aes.decrypt(ciphertext)


###### Matrix Multiplication ######
import numpy as np


def matmul(params):
    size = params["size"]

    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    np.dot(A, B)


###### Linear  ######
import scipy.linalg


def linalg(params):
    size = params["size"]

    a = np.random.rand(size, size)
    b = np.random.rand(size)
    scipy.linalg.solve(a, b)
