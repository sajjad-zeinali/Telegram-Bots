# Ideal Gas Law Calculator Bot
This Telegram bot calculates the missing variable in the Ideal Gas Law (PV = nRT) based on user input.

## How it Works
1. Start the bot with `/start`.
2. Use `/calc` to begin.
3. Enter values for Pressure (P), Volume (V), Temperature (T), and Moles (N). Enter `0` for the variable you want to calculate.
4. The bot computes the missing value and shows all final variables.

## Units
- Pressure (P): Pascals (Pa)
- Volume (V): Cubic meters (m³)
- Temperature (T): Kelvin (K)
- Moles (N): Moles (mol)
- Gas constant (R): 8.314 J/(mol·K)

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the bot: `python bot.py`