import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password():
    try:
        length = int(length_entry.get())
        use_upper = var_upper.get()
        use_lower = var_lower.get()
        use_digits = var_digits.get()
        use_symbols = var_symbols.get()

        characters = ''
        if use_upper:
            characters += string.ascii_uppercase
        if use_lower:
            characters += string.ascii_lowercase
        if use_digits:
            characters += string.digits
        if use_symbols:
            characters += string.punctuation

        if not characters:
            messagebox.showerror("Error", "Select at least one character type.")
            return

        password = ''.join(random.choice(characters) for _ in range(length))
        password_display.delete(0, tk.END)
        password_display.insert(0, password)
        update_strength(length, use_upper, use_lower, use_digits, use_symbols)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for length.")

def save_password():
    password = password_display.get()
    if password:
        with open("saved_passwords.txt", "a") as f:
            f.write(password + "\n")
        messagebox.showinfo("Saved", "Password saved to file.")
    else:
        messagebox.showwarning("Warning", "No password to save.")

def copy_to_clipboard():
    password = password_display.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard.")
    else:
        messagebox.showwarning("Warning", "No password to copy.")

def update_strength(length, upper, lower, digits, symbols):
    strength = 0
    if upper: strength += 1
    if lower: strength += 1
    if digits: strength += 1
    if symbols: strength += 1

    if length >= 12:
        strength += 1
    elif length < 6:
        strength -= 1

    levels = {
        0: ("Very Weak", "red"),
        1: ("Weak", "orange"),
        2: ("Moderate", "yellow"),
        3: ("Strong", "green"),
        4: ("Very Strong", "blue"),
        5: ("Excellent", "purple")
    }

    label, color = levels.get(strength, ("Unknown", "gray"))
    strength_label.config(text=f"Strength: {label}", fg=color)

# GUI setup
root = tk.Tk()
root.title("Advanced Password Generator")

tk.Label(root, text="Password Length:").grid(row=0, column=0, sticky="w")
length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1)

# Checkboxes for complexity
var_upper = tk.BooleanVar()
var_lower = tk.BooleanVar()
var_digits = tk.BooleanVar()
var_symbols = tk.BooleanVar()

tk.Checkbutton(root, text="Include Uppercase", variable=var_upper).grid(row=1, column=0, columnspan=2, sticky="w")
tk.Checkbutton(root, text="Include Lowercase", variable=var_lower).grid(row=2, column=0, columnspan=2, sticky="w")
tk.Checkbutton(root, text="Include Digits", variable=var_digits).grid(row=3, column=0, columnspan=2, sticky="w")
tk.Checkbutton(root, text="Include Symbols", variable=var_symbols).grid(row=4, column=0, columnspan=2, sticky="w")

# Buttons
tk.Button(root, text="Generate Password", command=generate_password).grid(row=5, column=0, pady=10)
tk.Button(root, text="Save Password", command=save_password).grid(row=5, column=1)
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).grid(row=6, column=0, columnspan=2)

# Display
tk.Label(root, text="Generated Password:").grid(row=7, column=0, sticky="w")
password_display = tk.Entry(root, width=30)
password_display.grid(row=7, column=1)

# Strength indicator
strength_label = tk.Label(root, text="Strength: ", font=('Arial', 10, 'bold'))
strength_label.grid(row=8, column=0, columnspan=2)

root.mainloop()