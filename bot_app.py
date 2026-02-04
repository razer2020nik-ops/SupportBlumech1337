import threading
import time
import tkinter as tk
from tkinter import messagebox
import telebot

# ================= НАСТРОЙКИ =================
BOT_TOKEN = "8322137959:AAE3c3iOkIUO-ZMcFhc2J27mGXysvbRJBNM"
ANTISPAM_SECONDS = 3

# ================= ГЛОБАЛЬНЫЕ =================
bot = None
bot_thread = None
running = False
last_message_time = {}

# ================= ЛОГИКА БОТА =================
def is_spam(chat_id, user_id):
    now = time.time()
    key = (chat_id, user_id)
    last = last_message_time.get(key, 0)

    if now - last < ANTISPAM_SECONDS:
        return True

    last_message_time[key] = now
    return False

def run_bot():
    global bot, running

    bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

    @bot.message_handler(commands=["start"])
    def start_cmd(m):
        bot.reply_to(
            m,
            "👋 Привет!\n\n"
            "🤖 <b>Support Blumech1337</b>\n"
            "🚫 Антиспам: 3 секунды\n\n"
            "Бот работает, пока приложение включено ✅"
        )

    @bot.message_handler(func=lambda m: True)
    def handle_all(m):
        if not m.from_user:
            return

        if is_spam(m.chat.id, m.from_user.id):
            try:
                bot.delete_message(m.chat.id, m.message_id)
            except:
                pass

    while running:
        try:
            bot.polling(none_stop=False, interval=1, timeout=20)
        except Exception:
            time.sleep(2)

# ================= GUI =================
def start_bot_gui():
    global running, bot_thread

    if running:
        return

    if not BOT_TOKEN or "ВСТАВЬ" in BOT_TOKEN:
        messagebox.showerror("Ошибка", "Вставь BOT TOKEN!")
        return

    running = True
    status_label.config(text="Status: ON ✅", fg="green")

    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

def stop_bot_gui():
    global running
    running = False
    status_label.config(text="Status: OFF ⛔", fg="red")

# ================= ОКНО =================
root = tk.Tk()
root.title("Support Blumech1337")
root.geometry("320x220")
root.resizable(False, False)

title = tk.Label(root, text="Support Blumech1337", font=("Arial", 16, "bold"))
title.pack(pady=10)

status_label = tk.Label(root, text="Status: OFF ⛔", font=("Arial", 14), fg="red")
status_label.pack(pady=10)

btn_start = tk.Button(root, text="▶ Play Bot", font=("Arial", 12), width=18, command=start_bot_gui)
btn_start.pack(pady=5)

btn_stop = tk.Button(root, text="⏹ Stop Bot", font=("Arial", 12), width=18, command=stop_bot_gui)
btn_stop.pack(pady=5)

root.mainloop()
