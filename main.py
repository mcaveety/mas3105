# MAS 3105 - Section 004
# Spring 2025 Final Project - Error Correction Codes
# Michelle M. & Colden H.
"""
Simulation of message encoding using Hamming and Reed-Solomon encoding techniques,
allowing the user to enter messages, apply random noise, encode and decode the message.
"""

import tkinter
from interface import Interface


def __main__():

    # Launch User Interface
    root = tkinter.Tk()
    Interface(root)
    root.mainloop()

if __name__ == "__main__":
    __main__()
