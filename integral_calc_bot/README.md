# Integral Calculator Bot
This Telegram bot computes the indefinite integral of a given function using SymPy and displays it as a LaTeX image.

## How it Works
1. Start with `/start` for instructions.
2. Use `/calc` and enter a function (e.g., `x^2`, `sin(x)`).
3. Get the integral as an image with the formula.

## Supported Syntax
- Powers: `x^2` (use `^`)
- Multiplication: `2*x` (use `*`)
- Functions: `sin(x)`, `cos(x)`, `log(x)` (ln), `exp(x)`, `sqrt(x)`
- Constants: `pi`

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set your Telegram bot token:
   - `export TELEGRAM_TOKEN='your-token-here'` (Linux/Mac)
   - `set TELEGRAM_TOKEN='your-token-here'` (Windows)
3. Run: `python bot.py`