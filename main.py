import tkinter as tk
from tkinter import ttk
from random import randint

class CipherApp:
    def __init__(self):
        # Setup window and set name and dimensions
        self.root = tk.Tk()
        self.root.title("Cipher Encryption Application")
        self.root.geometry("500x600")

        self.shift = randint(0, 25)
        self.non_alpha = tk.IntVar()

        self.setupGUI()

    def shift_cipher(self, text, shift):
        # Shift needs to be in range between 0-25
        shift = shift % 26

        res = []
        for char in text:
            if char.isalpha():
                is_upper = char.isupper()

                char_upper = char.upper()

                char_pos = ord(char_upper) - ord('A')
                shifted_pos = (char_pos + shift) % 26

                new_char = chr(shifted_pos + ord('A'))

                # Maintain original case
                if is_upper:
                    res.append(new_char)
                else:
                    res.append(new_char.lower())
            elif self.non_alpha.get() == 0:
                # Preserve non-alphabetic chars
                res.append(char)

        return ''.join(res)

    def encrypt(self):
        # Encryption function
        enc_text = self.base_text.get(1.0, tk.END)
        
        enc_text = self.shift_cipher(enc_text, self.shift)

        # Delete old text 
        self.res_text.delete(1.0, tk.END)
        self.res_text.insert(tk.END, enc_text)

    def decrypt(self):
        # Decryption function
        dec_text = self.res_text.get(1.0, tk.END)

        dec_text = self.shift_cipher(dec_text, -self.shift)

        # Delete old text and insert new
        self.base_text.delete(1.0, tk.END)
        self.base_text.insert(tk.END, dec_text)

    def clear(self):
        # Clear
        self.base_text.delete(1.0, tk.END)

        self.res_text.delete(1.0, tk.END)

    def setupGUI(self):
        tabControl = ttk.Notebook(self.root)

        # Set up frame
        self.my_frame = tk.Frame(self.root)
        self.my_frame.pack(pady=20)

        # Create Buttons
        self.enc_button = tk.Button(self.my_frame, text="Encrypt", font = ('Helvetica', 18), command=self.encrypt)
        self.enc_button.grid(row=0, column=0)

        self.dec_button = tk.Button(self.my_frame, text="Decrypt", font = ('Helvetica', 18), command=self.decrypt)
        self.dec_button.grid(row=0, column=1, padx=30)

        self.clear_button = tk.Button(self.my_frame, text="Clear", font = ('Helvetica', 18), command=self.clear)
        self.clear_button.grid(row=0, column=2, padx=10)

        # Setup Options
        self.checkbox = ttk.Checkbutton(
            self.root,
            text='Only alphanumeric symbols',
            variable=self.non_alpha,
            onvalue=1,
            offvalue=0
        )

        self.checkbox.pack()

        # Main text editor
        self.enc_label = tk.Label(self.root, text="Decrypted Text:", font = ('Helvetica', 18))
        self.enc_label.pack()

        self.base_text = tk.Text(self.root, width=50, height=10)
        self.base_text.pack(pady=10)

        self.dec_label = tk.Label(self.root, text="Encrypted Text:", font = ('Helvetica', 18))
        self.dec_label.pack()

        self.res_text = tk.Text(self.root, width=50, height=10)
        self.res_text.pack(pady=10)

    def setup_tabs(self):
        pass

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CipherApp()

    app.run()


    