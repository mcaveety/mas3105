# MAS 3105 - Section 004
# Spring 2025 Final Project - Error Correction Codes
# Michelle M. & Colden H.
"""
Functions defined to implement Hamming encoding/decoding, Reed-Solomon encoding/decoding,
and simulation of random noise added to messages.
"""

import reedsolo
import random

from reedsolo import ReedSolomonError

# Begin Hamming Codes ----

def encode_hamming(message):
    """
    Encodes a string using Hamming (7,4)
    :param message: string
    :return: array
    """
    # Result will contain the Hamming-encoded value for each character
    result = []

    for char in message:
        # Convert character to integer (ASCII value)
        char_val = ord(char)

        # Create a Hamming code for this character
        hamming_code = encode_single_value(char_val)
        result.append(hamming_code)

    return result


def encode_single_value(value):
    """
    Encodes a single value using Hamming (7,4) by splitting into upper & lower bits
    :param value: integer
    :return: integer
    """
    # Break the value into two 4-bit chunks
    lower_bits = value & 0x0F  # Lower 4 bits
    upper_bits = (value >> 4) & 0x0F  # Upper 4 bits

    # Encode each chunk with Hamming(7,4)
    encoded_lower = hamming74_encode(lower_bits)
    encoded_upper = hamming74_encode(upper_bits)

    # Combine the results (7 bits for each chunk)
    encoded_value = (encoded_upper << 7) | encoded_lower

    return encoded_value


def hamming74_encode(data):
    """
    Encodes each integer using Hamming (7,4)
    :param data: integer
    :return: integer
    """
    # Extract data bits (we only use 4 bits)
    d1 = (data >> 0) & 1  # Least significant bit
    d2 = (data >> 1) & 1
    d3 = (data >> 2) & 1
    d4 = (data >> 3) & 1  # Most significant bit

    # Calculate parity bits
    # Each parity bit covers specific data bits according to standard Hamming code positions
    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4

    # Construct the 7-bit Hamming code
    # Format is: p1, p2, d1, p3, d2, d3, d4
    hamming = (p1 << 0) | (p2 << 1) | (d1 << 2) | (p3 << 3) | (d2 << 4) | (d3 << 5) | (d4 << 6)

    return hamming


def decode_hamming(encoded_message):
    """
    Decodes a Hamming (7,4) encoded message back to a string
    :param encoded_message: array
    :return: string
    """
    # Result will contain the decoded string
    result = ""

    for encoded_value in encoded_message:
        try:
            # Decode this value
            char_val = decode_single_value(encoded_value)

            # Convert the integer back to a character
            char = chr(char_val)
            result += char
        except:
            # In case of unrecoverable error, add a placeholder
            result += "?"

    return result


def decode_single_value(encoded_value):
    """
    Splits & decodes values from Hamming (7,4) code
    :param encoded_value: integer
    :return: integer
    """
    # Split the encoded value into two 7-bit chunks
    encoded_lower = encoded_value & 0x7F  # Lower 7 bits
    encoded_upper = (encoded_value >> 7) & 0x7F  # Upper 7 bits

    # Decode each chunk with Hamming(7,4)
    lower_bits = hamming74_decode(encoded_lower)
    upper_bits = hamming74_decode(encoded_upper)

    # Combine the results to get the original byte
    original_value = (upper_bits << 4) | lower_bits

    return original_value


def hamming74_decode(hamming):
    """
    Decodes an integer from Hamming (7,4) encoding implementation
    :param hamming: integer
    :return: integer
    """
    # Make sure hamming is within valid range (0-127)
    hamming = hamming & 0x7F

    # Extract all bits from the Hamming code
    # Format is: p1, p2, d1, p3, d2, d3, d4
    p1 = (hamming >> 0) & 1
    p2 = (hamming >> 1) & 1
    d1 = (hamming >> 2) & 1
    p3 = (hamming >> 3) & 1
    d2 = (hamming >> 4) & 1
    d3 = (hamming >> 5) & 1
    d4 = (hamming >> 6) & 1

    # Check parity bits to detect errors
    check1 = (p1 ^ d1 ^ d2 ^ d4) & 1
    check2 = (p2 ^ d1 ^ d3 ^ d4) & 1
    check3 = (p3 ^ d2 ^ d3 ^ d4) & 1

    # Calculate error position (if any)
    error_pos = (check3 << 2) | (check2 << 1) | check1

    # If error detected, correct it
    if error_pos != 0:
        # Error position corresponds to bit positions:
        # 3 -> d1, 5 -> d2, 6 -> d3, 7 -> d4
        # 1 -> p1, 2 -> p2, 4 -> p3
        if error_pos == 1:  # Error in p1
            p1 = 1 - p1  # Flip the bit
        elif error_pos == 2:
            p2 = 1 - p2
        elif error_pos == 3:
            d1 = 1 - d1
        elif error_pos == 4:
            p3 = 1 - p3
        elif error_pos == 5:
            d2 = 1 - d2
        elif error_pos == 6:
            d3 = 1 - d3
        elif error_pos == 7:
            d4 = 1 - d4

    # Reconstruct the original 4-bit data
    data = (d4 << 3) | (d3 << 2) | (d2 << 1) | d1

    return data

# Reed-Solomon Codes ----

# Create RSCodec object with max 10 error protection
rsc = reedsolo.RSCodec(10)

def encode_reedsolo(message):
    """
    Encodes a message using Reed-Solomon method
    :param message: string
    :return: bytearray
    """
    return rsc.encode(message.encode())

def decode_reedsolo(message):
    """
    Decodes a message using Reed-Solomon method
    :param message: bytearray
    :return: string
    """
    try:
        return rsc.decode(message)[0].decode()
    except ReedSolomonError as rserror:
        return rserror

# Noise simulation ---

def add_noise(message, noise):
    """
    Simulates noise disrupting message transfer
    :param message: string, bytearray
    :param noise: string
    :return: string, bytearray
    """
    length = len(message)
    if noise == "single":
        random_index = random.randint(0, length-1)
        message[random_index] += 1
    elif noise == "burst":
        burst_size = random.randint(0, 5)
        random_index = random.randint(0, length-burst_size-1)
        for i in range(burst_size):
            message[random_index + i] += 1
    return message