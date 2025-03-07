from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = 'YOUR TOKEN'
P, V, T, N = range(4)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Welcome! I can help you calculate the missing variable from the Ideal Gas Law (PV = nRT).\n'
        'To begin, type /calc.'
    )
    
# Initiate calculation by asking for Pressure
async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Enter the pressure in Pascals (Pa). If you want to calculate it, enter 0.')
    return P

# Handle Pressure input
async def get_P(upd4ate: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_P = float(update.message.text)
        if user_P < 0:
            await update.message.reply_text('Pressure must be zero (for calculation) or a positive number. Please enter again.')
            return P
        context.user_data['P'] = user_P
    except ValueError:
        await update.message.reply_text('Invalid input! Please enter a valid number.')
        return P
    
    await update.message.reply_text('Enter the volume in cubic meters (m³). If you want to calculate it, enter 0.')
    return V

# Handle Volume input
async def get_V(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_V = float(update.message.text)
        if user_V < 0:
            await update.message.reply_text('Volume must be zero (for calculation) or a positive number. Please enter again.')
            return V
        context.user_data['V'] = user_V
    except ValueError:
        await update.message.reply_text('Invalid input! Please enter a valid number.')
        return V

    await update.message.reply_text('Enter the temperature in Kelvin (K). If you want to calculate it, enter 0.')
    return T

# Handle Temperature input
async def get_T(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_T = float(update.message.text)
        if user_T < 0:
            await update.message.reply_text('Temperature must be zero (for calculation) or a positive number. Please enter again.')
            return T
        context.user_data['T'] = user_T
    except ValueError:
        await update.message.reply_text('Invalid input! Please enter a valid number.')
        return T
    
    await update.message.reply_text('Enter the number of moles (mol). If you want to calculate it, enter 0.')
    return N

# Handle Moles input
async def get_N(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_N = float(update.message.text)
        if user_N < 0:
            await update.message.reply_text('Moles must be zero (for calculation) or a positive number. Please enter again.')
            return N
        context.user_data['N'] = user_N
    except ValueError:
        await update.message.reply_text('Invalid input! Please enter a valid number.')
        return N

    # Check how many variables are missing
    missing_var = sum([1 for var in context.user_data.values() if var == 0])
    if missing_var > 1:
        await update.message.reply_text('Only one variable can be missing. Please restart and enter correct values.')
        context.user_data.clear()
        return ConversationHandler.END
    elif missing_var == 0:
        await update.message.reply_text('All variables are provided. No calculation needed!')
        context.user_data.clear()
        return ConversationHandler.END
    
    # Extract values
    p = context.user_data['P']
    v = context.user_data['V']
    T = context.user_data['T']
    n = context.user_data['N']
    R = 8.314  # Ideal gas constant in J/(mol·K)
    
    # Perform the necessary calculation based on the missing variable
    if p == 0:
        p = (n * R * T) / v
        result = f'Calculated Pressure (P) = {p:.2f} Pa'
    elif v == 0:
        v = (n * R * T) / p
        result = f'Calculated Volume (V) = {v:.2f} m³'
    elif T == 0:
        T = (p * v) / (n * R)
        result = f'Calculated Temperature (T) = {T:.2f} K'
    elif n == 0:
        n = (p * v) / (R * T)
        result = f'Calculated Moles (N) = {n:.2f} mol'

    # Send the result and all variables
    await update.message.reply_text(
        f'{result}\n\nFinal values:\n'
        f'Pressure (P) = {p:.2f} Pa\n'
        f'Volume (V) = {v:.2f} m³\n'
        f'Temperature (T) = {T:.2f} K\n'
        f'Moles (N) = {n:.2f} mol'
    )

    context.user_data.clear()
    return ConversationHandler.END
    
# Cancel command handler
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Operation has been canceled.')
    context.user_data.clear()
    return ConversationHandler.END

# Main function to run the bot
def main():
    app = Application.builder().token(TOKEN).build()
    start_handler = CommandHandler('start', start)
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('calc', calc)],
        states={
            P: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_P)],
            V: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_V)],
            T: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_T)],
            N: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_N)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    app.add_handler(start_handler)
    app.add_handler(conversation_handler)
    app.run_polling()

if __name__ == '__main__':
    main()