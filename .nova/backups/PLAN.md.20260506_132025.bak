# Simple GUI Calculator – Project Plan

## Overview
Create a lightweight desktop calculator with a graphical user interface using Python's built‑in `tkinter` library. The app will support basic arithmetic (+, –, ×, ÷) and handle input via button clicks and keyboard.

## Scope
- **Operations:** addition, subtraction, multiplication, division, clear, backspace, decimal point, sign toggle.
- **UI:** single window with a display entry and a grid of buttons.
- **Platform:** cross‑platform (Windows/macOS/Linux) with only the Python standard library.

## Architecture
1. **main.py** – entry point; creates the Tk root and launches `CalculatorApp`.
2. **calculator.py** – `Calculator` class handling expression building, evaluation, and state.
3. **gui.py** – `CalculatorApp` class building the UI, wiring button/keyboard events to `Calculator`.

## UI Design
- **Display:** read‑only `Entry` widget showing current expression/result.
- **Buttons:** 4×5 grid  

  ```
  7 8 9 /
  4 5 6 *
  1 2 3 -
  0 . = +
  C ← +/- 
  ```

- Uniform style via `tk.Button`; callbacks delegate to `Calculator` methods.

## Core Functions (Calculator)
- `append_char(char)` – add digit/operator to expression.
- `clear()` – reset expression.
- `backspace()` – delete last character.
- `toggle_sign()` – invert sign of the current number.
- `evaluate()` – safely compute result (whitelisted characters or simple parser).

## Error Handling
- Catch `ZeroDivisionError` → display “Error”.
- Guard against malformed expressions (e.g., consecutive operators).

## Testing
- Unit tests for `Calculator` logic (operations, edge cases).
- UI sanity test: simulate button presses with `unittest.mock`.

## Milestones
| Milestone                | Duration |
|--------------------------|----------|
| Project scaffolding      | 1 day    |
| Calculator logic module  | 2 days   |
| GUI construction         | 2 days   |
| Integration & polish     | 1 day    |
| Testing & documentation  | 1 day    |
| Release                  | –        |

## Deliverables
- Source: `main.py`, `calculator.py`, `gui.py`
- `requirements.txt` (empty; stdlib only)
- `README.md` with usage instructions
- `PLAN.md` (this document)

## Risks & Mitigations
- **Risk:** Using `eval` may be unsafe.  
  **Mitigation:** Restrict allowed characters or implement a simple shunting‑yard parser.
- **Risk:** UI inconsistencies across platforms.  
  **Mitigation:** Stick to default Tkinter widgets and avoid custom theming.

--- 

*End of plan.*