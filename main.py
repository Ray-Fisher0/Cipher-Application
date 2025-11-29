import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from random import randint

ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # 'J' is typically omitted in Playfair cipher

class CipherApp:
    def __init__(self):
        # Setup window and set name and dimensions
        self.root = tk.Tk()
        self.root.title("Cipher Encryption / Decryption Tool")
        self.root.geometry("700x600")
        self.root.configure(bg="#F5F5F5")

        # Variables
        self.shift = tk.IntVar(value=randint(0, 25))
        self.non_alpha = tk.IntVar()
        self.playfair_key = tk.StringVar(value="KEYWORD")
        self.algorithm = tk.StringVar(value="Caesar")

        # Create tabbed layout
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Tabs
        self.tab_caesar = tk.Frame(self.notebook, bg="#F5F5F5")
        self.tab_reverse = tk.Frame(self.notebook, bg="#F5F5F5")
        self.tab_playfair = tk.Frame(self.notebook, bg="#F5F5F5")

        self.notebook.add(self.tab_caesar, text="Caesar Cipher")
        self.notebook.add(self.tab_reverse, text="Reverse Cipher")
        self.notebook.add(self.tab_playfair, text="Playfair Cipher")

        # Build GUI for each tab
        self.build_caesar_tab()
        self.build_reverse_tab()
        self.build_playfair_tab()

    # Ceaser Cipher functions
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
            elif self.non_alpha.get() == 1:
                # Preserve non-alphabetic chars
                res.append(char)
        return ''.join(res)
    
    # Reverse Cipher functions
    def reverse_cipher(self, text):
        return text[::-1]
    
    # Playfair Cipher functions
    def playfair_generate_table(self, key):
        key = key.upper().replace("J", "I")
        used = set()
        table = []

        for ch in key:
            if ch.isalpha() and ch not in used:
                used.add(ch)
                table.append(ch)

        for ch in ALPHABET:
            if ch not in used:
                table.append(ch)

        return [table[i:i+5] for i in range(0, 25, 5)]

    def playfair_prepare(self, text):
        text = "".join([c for c in text.upper().replace("J","I") if c.isalpha()])
        pairs = []
        i = 0
        while i < len(text):
            a = text[i]
            b = text[i+1] if i+1 < len(text) else "X"
            if a == b:
                pairs.append(a + "X")
                i += 1
            else:
                pairs.append(a + b)
                i += 2
        return pairs

    def playfair_encrypt(self, text, key):
        table = self.playfair_generate_table(key)
        pairs = self.playfair_prepare(text)
        out = []

        for a, b in pairs:
            posA = [(r,c) for r in range(5) for c in range(5) if table[r][c]==a][0]
            posB = [(r,c) for r in range(5) for c in range(5) if table[r][c]==b][0]
            r1,c1 = posA
            r2,c2 = posB

            if r1 == r2:
                out.append(table[r1][(c1+1)%5])
                out.append(table[r2][(c2+1)%5])
            elif c1 == c2:
                out.append(table[(r1+1)%5][c1])
                out.append(table[(r2+1)%5][c2])
            else:
                out.append(table[r1][c2])
                out.append(table[r2][c1])

        return "".join(out)

    def playfair_decrypt(self, text, key):
        table = self.playfair_generate_table(key)
        pairs = self.playfair_prepare(text)
        out = []

        for a, b in pairs:
            posA = [(r,c) for r in range(5) for c in range(5) if table[r][c]==a][0]
            posB = [(r,c) for r in range(5) for c in range(5) if table[r][c]==b][0]
            r1,c1 = posA
            r2,c2 = posB

            if r1 == r2:
                out.append(table[r1][(c1-1)%5])
                out.append(table[r2][(c2-1)%5])
            elif c1 == c2:
                out.append(table[(r1-1)%5][c1])
                out.append(table[(r2-1)%5][c2])
            else:
                out.append(table[r1][c2])
                out.append(table[r2][c1])

        return "".join(out)
    
    # Clear Input and Output
    def clear(self):
        if self.notebook.index(self.notebook.select()) == 0:
            self.caesar_input.delete("1.0", tk.END)
        elif self.notebook.index(self.notebook.select()) == 1:
            self.rev_input.delete("1.0", tk.END)
        else:
            self.play_input.delete("1.0", tk.END)

    # Input Validation
    def validate_int(self, val):
        return val.isdigit() or val == ""
    
    # File Operations
    def load_file(self):
        filename = filedialog.askopenfilename(
            title="Load Text File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filename:
            return
        
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = file.read()
            if self.notebook.index(self.notebook.select()) == 0:
                self.caesar_input.delete("1.0", tk.END)
                self.caesar_input.insert(tk.END, data)
            elif self.notebook.index(self.notebook.select()) == 1:
                self.rev_input.delete("1.0", tk.END)
                self.rev_input.insert(tk.END, data)
            else:
                self.play_input.delete("1.0", tk.END)
                self.play_input.insert(tk.END, data)
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't load file:\n{e}")

    def save_output(self):
        if self.notebook.index(self.notebook.select()) == 0:
            text = self.output_text.get("1.0", tk.END).strip()
        elif self.notebook.index(self.notebook.select()) == 1:
            text = self.rev_output.get("1.0", tk.END).strip()
        else:
            text = self.play_output.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Empty Output", "There is no text to save.")
            return

        filename = filedialog.asksaveasfilename(
            title="Save Output As",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filename:
            return

        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(text)
            messagebox.showinfo("Saved", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't save file:\n{e}")

    # GUI Layout
    def build_caesar_tab(self):
        frame = self.tab_caesar

        title = tk.Label(
            frame,
            text="Caesar Cipher Encryption / Decryption",
            font=("Helvetica", 24, "bold"),
            bg="#F5F5F5"
        )
        title.pack(pady=15)

        # Frame for shift + options
        option_frame = tk.Frame(frame, bg="#F5F5F5")
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
        input_frame = tk.Frame(frame, bg="#F5F5F5")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Input Text:", font=("Helvetica", 16), bg="#F5F5F5").pack()
        self.caesar_input = tk.Text(input_frame, width=70, height=7, font=("Helvetica", 12))
        self.caesar_input.pack(pady=5)

        # Buttons
        button_frame = tk.Frame(frame, bg="#F5F5F5")
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Encrypt", command=self.caesar_encrypt).grid(row=0, column=0, padx=15)
        ttk.Button(button_frame, text="Decrypt", command=self.caesar_decrypt).grid(row=0, column=1, padx=15)
        ttk.Button(button_frame, text="Clear", command=self.clear).grid(row=0, column=2, padx=15)

        # Output Frame
        output_frame = tk.Frame(frame, bg="#F5F5F5")
        output_frame.pack(pady=10)

        tk.Label(output_frame, text="Output Text:", font=("Helvetica", 16), bg="#F5F5F5").pack()
        self.caesar_output = tk.Text(output_frame, width=70, height=7, font=("Helvetica", 12))
        self.caesar_output.pack(pady=5)

        # Save / Load Buttons
        file_frame = tk.Frame(frame, bg="#F5F5F5")
        file_frame.pack(pady=5)

        ttk.Button(file_frame, text="Load Text File", command=self.load_file).grid(row=0, column=0, padx=20)
        ttk.Button(file_frame, text="Save Output to File", command=self.save_output).grid(row=0, column=1, padx=20)

    def caesar_encrypt(self):
        text = self.caesar_input.get("1.0", tk.END)
        out = self.shift_cipher(text, self.shift.get())
        self.caesar_output.delete("1.0", tk.END)
        self.caesar_output.insert(tk.END, out)

    def caesar_decrypt(self):
        text = self.caesar_input.get("1.0", tk.END)
        out = self.shift_cipher(text, -self.shift.get())
        self.caesar_output.delete("1.0", tk.END)
        self.caesar_output.insert(tk.END, out)

    # Reverse Cipher Tab
    def build_reverse_tab(self):
        frame = self.tab_reverse

        title = tk.Label(
            frame,
            text="Reverse Cipher Encryption / Decryption",
            font=("Helvetica", 24, "bold"),
            bg="#F5F5F5"
        )
        title.pack(pady=15)

        self.rev_input = tk.Text(frame, width=70, height=7, font=("Helvetica", 12))
        tk.Label(frame, text="Input Text:", bg="#F5F5F5").pack()
        self.rev_input.pack(pady=5)

        button_frame = tk.Frame(frame, bg="#F5F5F5")
        button_frame.pack()
        ttk.Button(button_frame, text="Encrypt",
                   command=self.reverse_encrypt).grid(row=0, column=0, padx=15)
        ttk.Button(button_frame, text="Decrypt",
                   command=self.reverse_encrypt).grid(row=0, column=1, padx=15)
        ttk.Button(button_frame, text="Clear", command=self.clear).grid(row=0, column=2, padx=15)

        self.rev_output = tk.Text(frame, width=70, height=7, font=("Helvetica", 12))
        tk.Label(frame, text="Output Text:", bg="#F5F5F5").pack()
        self.rev_output.pack(pady=5)

         # Save / Load Buttons
        file_frame = tk.Frame(frame, bg="#F5F5F5")
        file_frame.pack(pady=5)

        ttk.Button(file_frame, text="Load Text File", command=self.load_file).grid(row=0, column=0, padx=20)
        ttk.Button(file_frame, text="Save Output to File", command=self.save_output).grid(row=0, column=1, padx=20)

    def reverse_encrypt(self):
        text = self.rev_input.get("1.0", tk.END)
        out = self.reverse_cipher(text)
        self.rev_output.delete("1.0", tk.END)
        self.rev_output.insert(tk.END, out)

    # Playfair Cipher Tab
    def build_playfair_tab(self):
        frame = self.tab_playfair

        title = tk.Label(
            frame,
            text="Playfair Cipher Encryption / Decryption",
            font=("Helvetica", 24, "bold"),
            bg="#F5F5F5"
        )
        title.pack(pady=15)

        tk.Label(frame, text="Playfair Key:", font=("Helvetica", 14),
                 bg="#F5F5F5").pack(pady=5)
        tk.Entry(frame, textvariable=self.playfair_key,
                 width=15, font=("Helvetica", 14)).pack()

        self.play_input = tk.Text(frame, width=70, height=7, font=("Helvetica", 12))
        tk.Label(frame, text="Input Text:", bg="#F5F5F5").pack()
        self.play_input.pack(pady=5)

        button_frame = tk.Frame(frame, bg="#F5F5F5")
        button_frame.pack()
        ttk.Button(button_frame, text="Encrypt",
                   command=self.playfair_encrypt_text).grid(row=0, column=0, padx=15)
        ttk.Button(button_frame, text="Decrypt",
                   command=self.playfair_decrypt_text).grid(row=0, column=1, padx=15)
        ttk.Button(button_frame, text="Clear", command=self.clear).grid(row=0, column=2, padx=15)

        self.play_output = tk.Text(frame, width=70, height=7, font=("Helvetica", 12))
        tk.Label(frame, text="Output Text:", bg="#F5F5F5").pack()
        self.play_output.pack(pady=5)

         # Save / Load Buttons
        file_frame = tk.Frame(frame, bg="#F5F5F5")
        file_frame.pack(pady=5)

        ttk.Button(file_frame, text="Load Text File", command=self.load_file).grid(row=0, column=0, padx=20)
        ttk.Button(file_frame, text="Save Output to File", command=self.save_output).grid(row=0, column=1, padx=20)

    def playfair_encrypt_text(self):
        text = self.play_input.get("1.0", tk.END)
        out = self.playfair_encrypt(text, self.playfair_key.get())
        self.play_output.delete("1.0", tk.END)
        self.play_output.insert(tk.END, out)

    def playfair_decrypt_text(self):
        text = self.play_input.get("1.0", tk.END)
        out = self.playfair_decrypt(text, self.playfair_key.get())
        self.play_output.delete("1.0", tk.END)
        self.play_output.insert(tk.END, out)

    # Run App
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CipherApp()
    app.run()
