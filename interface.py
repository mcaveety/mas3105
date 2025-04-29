# User Interface
# Based on Tkinter functionality

from tkinter import *
from tkinter.ttk import *


class Interface:

    def __init__(self, root):

        # Set up basic application window
        self.root = root
        self.root.title("MAS 3105 - Error Correction Codes")

        # Organize basic window layout
        self.root.minsize(400, 400) # Default to 400px * 400px window
        self.frame = Frame(root, padding="3 3 12 12") # Default padding (px)
        self.frame.grid(column=0, row=0) # Establish grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Application window elements
        self.title = Label(self.frame, text="Error Correction Codes Demo", font=("TkDefaultFont", 20, "bold"))
        self.subtitle = Label(self.frame, text="MAS 3105 - Final Project", font=("TkDefaultFont", 16, "bold"))

        # Encoding label, entry box, and submission button
        self.encoding_type = IntVar() # 0 = Hamming code, 1 = Reed-Solomon code
        self.encode_label = Label(self.frame, text="Enter message to encode:")
        self.encode_message_entry = Entry(self.frame, width=80)

        # Select the encoding type (Hamming or Reed-Solomon codes)
        self.encode_hamming = Radiobutton(self.frame, text="Hamming", value=0, variable=self.encoding_type)
        self.encode_reedsolomon = Radiobutton(self.frame,text="Reed-Solomon", value=1, variable=self.encoding_type)
        self.encode_button = Button(self.frame, text="Encode", command=self._get_encoding)

        # Error selection button
        self.error_type = IntVar() # 0 = Single-Bit error, 1 = Burst error
        self.error_label = Label(self.frame, text="Introduce Error")
        self.error_single = Radiobutton(self.frame, text="Single-bit error", value=0, variable=self.error_type)
        self.error_burst = Radiobutton(self.frame, text="Burst error", value=1, variable=self.error_type)
        self.error_button = Button(self.frame, text="Apply Noise", command=self._get_error)

        # Output feed for interactions
        self.activity_feed = Text(self.frame)
        self.activity_feed_label = Label(self.frame, text="Activity Feed")
        self.activity_feed.insert(END, "-- Begin Program --\n")
        self.activity_feed.config(state=DISABLED)

        self.feed_button = Button(self.frame, text="Clear Activity Feed", command=self._clear_activity)
        self.quit = Button(self.frame, text="Quit Program", command=root.destroy)

        # Application Layout (Grid)
        # Title and subtitle
        self.title.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.subtitle.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Encoding section
        self.encode_label.grid(row=2, column=0, sticky="w")
        self.encode_message_entry.grid(row=3, column=0, columnspan=2, sticky="ew")
        self.encode_hamming.grid(row=4, column=0, sticky="w")  # Remove sticky="ew"
        self.encode_reedsolomon.grid(row=4, column=1, sticky="w")  # Remove sticky="ew"
        self.encode_button.grid(row=5, column=0, columnspan=2, sticky="ew")

        # Error selection
        self.error_label.grid(row=6, column=0, sticky="w")
        self.error_single.grid(row=7, column=0, sticky="w")  # Remove sticky="ew"
        self.error_burst.grid(row=7, column=1, sticky="w")  # Remove sticky="ew"
        self.error_button.grid(row=8, column=0, columnspan=2, sticky="ew")

        # Activity feed
        self.activity_feed_label.grid(row=9, column=0, columnspan=2, sticky="w")
        self.activity_feed.grid(row=10, column=0, columnspan=2, sticky="ew")
        self.feed_button.grid(row=11, column=0, sticky="ew")
        self.quit.grid(row=11, column=1, sticky="ew")

        # Configure column and row padding
        for i in range(12):  # Adjust range as needed for total rows
            self.frame.rowconfigure(i, pad=5)
        self.frame.columnconfigure(0, weight=1, pad=5)
        self.frame.columnconfigure(1, weight=1, pad=5)

    def _update_activity(self, message):
        self.activity_feed.config(state=NORMAL)
        self.activity_feed.insert(END, message)
        self.activity_feed.config(state=DISABLED)

    def _clear_activity(self):
        self.activity_feed.config(state=NORMAL)
        self.activity_feed.delete(1, END)
        self.activity_feed.config(state=DISABLED)

    def _get_encoding(self):
        encoding_type = self.encoding_type.get()
        message = self.encode_message_entry.get()
        if encoding_type:
            encoding_name = "Reed-Solomon"
        else:
            encoding_name = "Hamming"
        self._update_activity(f"Encoding selected: {encoding_name} Code applied to \"{message}\"\n")
        self.encode_message_entry.delete(0, END)

    def _get_error(self):
        error_type = self.error_type.get()
        if error_type:
            error_name = "Burst Error"
        else:
            error_name = "Single-bit Error"

        self._update_activity(f"Error introduced: {error_name}\n")

