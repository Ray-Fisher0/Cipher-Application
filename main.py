import tkinter as tk
from tkinter import ttk
from random import randint

class CipherApp:
    def __init__(self):
        # Setup window and set name and dimensions
        self.root = tk.Tk()
        self.root.title("Cipher Encryption / Decryption Tool")
        self.root.geometry("700x600")
        self.root.configure(bg="#F5F5F5")

        self.shift = tk.IntVar(value=randint(0, 25))
        self.non_alpha = tk.IntVar()

        self.setup_gui()

    def validate_input(P):
        if P.isdigit() or P == "":
            return True
        return False


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

    # Button Handlers
    def encrypt(self):
        shift = self.shift.get()
        text = self.input_text.get("1.0", tk.END)
        result = self.shift_cipher(text, shift)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)

    def decrypt(self):
        shift = -self.shift.get()
        text = self.input_text.get("1.0", tk.END)
        result = self.shift_cipher(text, shift)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)

    def clear(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)

    # Input Validation
    def validate_int(self, val):
        return val.isdigit() or val == ""
    
    # File Operations
    def load_file(self):
        filename = tk.filedialog.askopenfilename(
            title="Load Text File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filename:
            return
        
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = file.read()
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert(tk.END, data)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Couldn't load file:\n{e}")

    def save_output(self):
        text = self.output_text.get("1.0", tk.END).strip()
        if not text:
            tk.messagebox.showwarning("Empty Output", "There is no text to save.")
            return

        filename = tk.filedialog.asksaveasfilename(
            title="Save Output As",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filename:
            return

        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(text)
            tk.messagebox.showinfo("Saved", "File saved successfully!")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Couldn't save file:\n{e}")

    # GUI Layout
    def setup_gui(self):
        title = tk.Label(
            self.root,
            text="Cipher Encryption / Decryption Tool",
            font=("Helvetica", 26, "bold"),
            bg="#F5F5F5"
        )
        title.pack(pady=15)

        # Frame for shift + options
        option_frame = tk.Frame(self.root, bg="#F5F5F5")
        option_frame.pack(pady=5)

        # Shift Input
        tk.Label(option_frame, text="Shift Amount:", font=("Helvetica", 14), bg="#F5F5F5").grid(row=0, column=0, padx=5)

        vcmd = (self.root.register(self.validate_int), "%P")
        shift_entry = tk.Entry(option_frame, width=5, font=("Helvetica", 14), textvariable=self.shift,
                               validate="key", validatecommand=vcmd)
        shift_entry.grid(row=0, column=1, padx=10)

        # Checkbox option
        ttk.Checkbutton(option_frame,
                        text="Preserve non-alphabetic characters",
                        variable=self.non_alpha).grid(row=0, column=2, padx=10)

        # Text Input Frame
        input_frame = tk.Frame(self.root, bg="#F5F5F5")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Input Text:", font=("Helvetica", 16), bg="#F5F5F5").pack()
        self.input_text = tk.Text(input_frame, width=70, height=7, font=("Helvetica", 12))
        self.input_text.pack(pady=5)

        # Buttons
        button_frame = tk.Frame(self.root, bg="#F5F5F5")
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Encrypt", command=self.encrypt).grid(row=0, column=0, padx=15)
        ttk.Button(button_frame, text="Decrypt", command=self.decrypt).grid(row=0, column=1, padx=15)
        ttk.Button(button_frame, text="Clear", command=self.clear).grid(row=0, column=2, padx=15)

        # Output Frame
        output_frame = tk.Frame(self.root, bg="#F5F5F5")
        output_frame.pack(pady=10)

        tk.Label(output_frame, text="Output Text:", font=("Helvetica", 16), bg="#F5F5F5").pack()
        self.output_text = tk.Text(output_frame, width=70, height=7, font=("Helvetica", 12))
        self.output_text.pack(pady=5)

        # Save / Load Buttons
        file_frame = tk.Frame(self.root, bg="#F5F5F5")
        file_frame.pack(pady=5)

        ttk.Button(file_frame, text="Load Text File", command=self.load_file).grid(row=0, column=0, padx=20)
        ttk.Button(file_frame, text="Save Output to File", command=self.save_output).grid(row=0, column=1, padx=20)

    # Run App
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CipherApp()

    app.run()
