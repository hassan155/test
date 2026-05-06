# Simple GUI Calculator

A lightweight desktop calculator with a graphical user interface built using Python's `tkinter` library. This application supports basic arithmetic operations and is designed to be cross-platform, requiring only the Python standard library.

## Features

- Basic arithmetic operations: addition (+), subtraction (-), multiplication (×), and division (÷)
- Clear entry and backspace functionality
- Toggle positive/negative values
- Keyboard input support
- Error handling for operations like division by zero
- Cross-platform compatibility (Windows, macOS, Linux)

## Files

- `main.py` - Entry point of the application.
- `calculator.py` - Core logic for calculator operations.
- `gui.py` - Graphical user interface implementation.

## Usage

1. Run the calculator:
   ```bash
   python main.py
   ```

2. Use the GUI to perform calculations via mouse or keyboard.

## Requirements

- Python 3.x
- Tkinter (usually included with Python)

## Installation

No installation required. Clone or download the repository and run `main.py` directly.

## Controls

- **Mouse**: Click buttons to input numbers and operations.
- **Keyboard**: Use number keys and operators directly on the keyboard.

## Supported Operations

| Operation        | Button    | Key        |
|------------------|------------|------------|
| Clear            | C          |            |
| Backspace        | ←          | Backspace  |
| Sign Toggle       | +/-        | _          |
| Decimal point      | .          | .          |
| Equals            | =          | Enter      |
| Numbers & Operators | 0-9, ., +, -, ×, ÷ | 0-9, ., +, -, *, / |

## Error Handling

- Division by zero and invalid expressions will display "Error".
- The application prevents the use of unsafe characters in expressions to avoid code injection.

## Notes

- Only standard Python libraries are used (i.e., `tkinter` and `re`).
- The application is designed to be simple and efficient for basic calculations.

## License

This project is open-source and available under the MIT License.