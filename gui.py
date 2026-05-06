import tkinter as tk
from calculator import Calculator

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.calculator = Calculator()
        self.create_widgets()
        self.layout_widgets()
        self.bind_keyboard()

    def create_widgets(self):
        self.display = tk.Entry(self.root, font=("Arial", 24), borderwidth=2, relief="solid", justify='right')
        self.display.config(state='readonly')
        self.display.bind("<Key>", lambda e: "break")

        button_texts = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C', '←', '+/-'
        ]
        self.buttons = {}
        for text in button_texts:
            cmd = lambda t=text: self.on_button_click(t)
            btn = tk.Button(self.root, text=text, font=("Arial", 18), width=4, height=2, command=cmd)
            self.buttons[text] = btn

    def layout_widgets(self):
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", ipady=10)

        positions = [
            (1,0), (1,1), (1,2), (1,3),
            (2,0), (2,1), (2,2), (2,3),
            (3,0), (3,1), (3,2), (3,3),
            (4,0), (4,1), (4,2), (4,3),
            (5,0), (5,1), (5,2)
        ]
        for i, (row, col) in enumerate(positions):
            txt = list(self.buttons.keys())[i]
            self.buttons[txt].grid(row=row, column=col, sticky="nsew")

        for i in range(1, 6):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def bind_keyboard(self):
        self.root.bind('<Key>', self.on_key_press)

    def on_key_press(self, event):
        key = event.char
        if key in '0123456789+-*/.':
            self.on_button_click(key)
        elif key == '\r' or key == '=':
            self.on_button_click('=')
        elif event.keysym == 'BackSpace':
            self.on_button_click('←')
        elif event.keysym == 'Escape':
            self.on_button_click('C')
        elif key == '_':
            self.on_button_click('+/-')

    def on_button_click(self, char):
        if char in '0123456789+-*/.':
            self.calculator.append_char(char)
            self.update_display()
        elif char == '=':
            result = self.calculator.append_char('=')
            self.update_display(result)
        elif char == 'C':
            self.calculator.clear()
            self.update_display()
        elif char == '←':
            self.calculator.backspace()
            self.update_display()
        elif char == '+/-':
            self.calculator.toggle_sign()
            self.update_display()

    def update_display(self, value=None):
        if value is None:
            self.display.config(state='normal')
            self.display.delete(0, tk.END)
            self.display.insert(0, self.calculator.expression)
            self.display.config(state='readonly')
        else:
            self.display.config(state='normal')
            self.display.delete(0, tk.END)
            self.display.insert(0, str(value))
            self.display.config(state='readonly')