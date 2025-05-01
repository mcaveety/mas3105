# Working with Reed-Solomon Codes in Python

import reedsolo
from oct2py import Oct2Py
import random

from reedsolo import ReedSolomonError

oc = Oct2Py()
rsc = reedsolo.RSCodec(10)

def generate_hamming(message):
    test = oc.run("test.m")

def encode_reedsolo(message):
    return rsc.encode(message.encode())

def decode_reedsolo(message):
    try:
        return rsc.decode(message)[0].decode()
    except ReedSolomonError as rserror:
        return rserror

def add_noise(message, noise):
    length = len(message)
    if noise == "single":
        random_index = random.randint(0, length)
        message[random_index] += 1
    elif noise == "burst":
        burst_size = random.randint(0, 5)
        random_index = random.randint(0, length-burst_size)
        for i in range(burst_size):
            message[random_index + i] += 1
    return message