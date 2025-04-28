# Defined functions to facilitate program operations

from functools import reduce

# Get a string of text from the user
def get_message():
    return input("Enter your message: ")

# Convert an ASCII-character message into binary
def ascii_to_binary(message):
    binary_string = ''.join(format(ord(char), '08b') for char in message)
    return binary_string

# Convert a binary-character message into ASCII
def binary_to_ascii(binary_string):
    chars = []
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i + 8]
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def hamming_syndrome(bits):
    return reduce(
        # Reduce by xor
        lambda x, y: x ^ y,
        # All indices of active bits
        [i for (i, b) in enumerate(bits) if b]
    )

