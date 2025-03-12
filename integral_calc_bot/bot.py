import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import sympy as sp
import matplotlib.pyplot as plt
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
INPUT_FUNCTION = 1  # State for function input

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "Hi! Compute integrals with /calc.\n\n"
        "*Quick Guide:*\n"
        "- Powers: `x^2` (use `^`)\n"
        "- Multiplication: `2*x` (use `*`)\n"
        "- Functions: `sin(x)`, `cos(x)`, `log(x)` (natural log, ln), `exp(x)`, `sqrt(x)`\n"
        "- Logarithms: `log(x)` = ln(x), use `log10(x)` for base-10\n"
        "- Constants: `pi` (avoid `e`, use `exp(x)`)\n"
        "- Examples: `x^2 + 3*x`, `log(x) + exp(x)`\n"
        "*Tips*: Parentheses required (e.g., `sin(x)`), no spaces, lowercase only.\n"
        "Try it now with /calc!"
    )
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter a function (e.g., `x^2` or `sin(x)`):")
    return INPUT_FUNCTION

async def get_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    if not user_input:
        await update.message.reply_text("Error: Please enter a function (e.g., `x^2`).")
        return INPUT_FUNCTION

    await update.message.reply_text(f"You entered: {user_input}")

    try:
        # Define symbolic variable and parse the input
        x = sp.symbols('x')
        expression = sp.sympify(user_input.replace('^', '**'))
        integral = sp.integrate(expression, x).simplify()

        # Generate LaTeX for rendering
        integral_latex = sp.latex(integral)
        expr_latex = sp.latex(expression)

        plt.figure(figsize=(4, 2))
        plt.text(0.5, 0.6, f'$\\int {expr_latex} \, dx = {integral_latex} + C$', 
                 fontsize=14, ha='center', va='center')
        plt.axis('off')

        # Save and send image using a context manager
        with BytesIO() as buf:
            plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
            buf.seek(0)
            await update.message.reply_photo(photo=buf, caption=f"Integral of {user_input} computed!")
        plt.close()

    except sp.SympifyError:
        await update.message.reply_text("Error: Invalid input. Use examples like `x^2` or `sin(x)`. See `/start` for help.")
    except Exception as e:
        await update.message.reply_text(f"Unexpected error: {str(e)}. Please try again or contact support.")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operation canceled.")
    context.user_data.clear()
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('calc', calc)],
        states={INPUT_FUNCTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_func)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(start_handler)
    app.add_handler(conversation_handler)

    app.run_polling()

if __name__ == '__main__':
    main()