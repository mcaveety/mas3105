# Working with Reed-Solomon Codes in Python

import reedsolo
from oct2py import Oct2Py
import random

from reedsolo import ReedSolomonError

rsc = reedsolo.RSCodec(10)

def encode_hamming(message):

    # Result will contain the Hamming-encoded value (integer) for each character
    result = []
    for char in message:
        # Convert character to integer (ASCII value)
        char_val = ord(char)

        # Create a Hamming code for this character
        hamming_code = encode_single_value(char_val)
        result.append(hamming_code)

    return result


def encode_single_value(value):
    # Encodes a single integer value using Hamming(7,4) code.
    # encode 8 bits (1 byte) as two 4-bit chunks

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
    # Implements Hamming(7,4) encoding for a 4-bit value

    # Extract data bits (we only use 4 bits)
    d1 = (data >> 0) & 1
    d2 = (data >> 1) & 1
    d3 = (data >> 2) & 1
    d4 = (data >> 3) & 1

    # Calculate parity bits
    p1 = d1 ^ d2 ^ d4  # Parity bit 1 covers bits 1,3,5,7
    p2 = d1 ^ d3 ^ d4  # Parity bit 2 covers bits 2,3,6,7
    p3 = d2 ^ d3 ^ d4  # Parity bit 3 covers bits 4,5,6,7

    # Construct the 7-bit Hamming code
    # Format is: p1, p2, d1, p3, d2, d3, d4
    hamming = (p1 << 0) | (p2 << 1) | (d1 << 2) | (p3 << 3) | (d2 << 4) | (d3 << 5) | (d4 << 6)

    return hamming


def decode_hamming(encoded_message):
    # Decodes a Hamming-encoded message back to a string

    # Result will contain the decoded string
    result = ""

    for encoded_value in encoded_message:
        # Decode this value
        char_val = decode_single_value(encoded_value)

        # Convert the integer back to a character
        char = chr(char_val)
        result += char

    return result


def decode_single_value(encoded_value):
    # Decodes each segment of a Hamming-encoded value

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
    # Decodes a 7-bit Hamming code to retrieve the original 4-bit data.
    # Corrects single-bit errors.

    # Extract bits from the Hamming code
    # Format is: p1, p2, d1, p3, d2, d3, d4
    p1_received = (hamming >> 0) & 1
    p2_received = (hamming >> 1) & 1
    d1_received = (hamming >> 2) & 1
    p3_received = (hamming >> 3) & 1
    d2_received = (hamming >> 4) & 1
    d3_received = (hamming >> 5) & 1
    d4_received = (hamming >> 6) & 1

    # Calculate parity bits
    p1_calc = d1_received ^ d2_received ^ d4_received
    p2_calc = d1_received ^ d3_received ^ d4_received
    p3_calc = d2_received ^ d3_received ^ d4_received

    # Check for errors
    syndrome = 0
    if p1_received != p1_calc:
        syndrome |= 1
    if p2_received != p2_calc:
        syndrome |= 2
    if p3_received != p3_calc:
        syndrome |= 4

    # Correct single-bit error if detected
    if syndrome != 0:
        # The syndrome value tells us which bit is in error
        # Flip the bit at position syndrome
        hamming ^= (1 << (syndrome - 1))

        # Re-extract data bits after error correction
        d1_corrected = (hamming >> 2) & 1
        d2_corrected = (hamming >> 4) & 1
        d3_corrected = (hamming >> 5) & 1
        d4_corrected = (hamming >> 6) & 1
    else:
        # No error detected, use the received data bits
        d1_corrected = d1_received
        d2_corrected = d2_received
        d3_corrected = d3_received
        d4_corrected = d4_received

    # Reconstruct the original 4-bit data
    data = (d1_corrected << 0) | (d2_corrected << 1) | (d3_corrected << 2) | (d4_corrected << 3)

    return data

# Reed-Solomon Codes ----

def encode_reedsolo(message):
    return rsc.encode(message.encode())

def decode_reedsolo(message):
    try:
        return rsc.decode(message)[0].decode()
    except ReedSolomonError as rserror:
        return rserror

# Noise simulation ---

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