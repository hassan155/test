import re
import operator
from functools import reduce

class Calculator:
    def __init__(self):
        self.expression = ""
        self.operators = {'+': operator.add, '-': operator.sub, '×': operator.mul, '÷': operator.truediv}
    
    def append_char(self, char):
        if char in '0123456789+-×÷.':
            self.expression += char
        elif char == '=':
            return self.evaluate()
        return None

    def clear(self):
        self.expression = ""
    
    def backspace(self):
        if self.expression:
            self.expression = self.expression[:-1]
    
    def toggle_sign(self):
        if not self.expression:
            self.expression = '-'
        elif self.expression[0] == '-':
            self.expression = self.expression[1:]
        else:
            self.expression = '-' + self.expression
    
    def evaluate(self):
        if not self.expression:
            return "Error"
        try:
            # Sanitize input to prevent code injection
            allowed_chars = re.compile(r'^[0-9+\-*/.() ]+$')
            if not allowed_chars.match(self.expression):
                return "Error"
            
            # Replace operators to valid Python syntax
            expr = self.expression.replace('×', '*').replace('÷', '/')
            result = eval(expr)
            self.expression = str(result)
            return result
        except ZeroDivisionError:
            self.expression = ""
            return "Error"
        except:
            return "Error"