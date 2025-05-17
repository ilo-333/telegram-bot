from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

import os
TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = 369934680  # замени на свой числовой Telegram ID
GROUP_INVITE_LINK = 'https://t.me/+1C7TGihz-q45NmFi'  # ссылка на группу

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Для вступления в группу, отправь нам, пожалуйста, фото своей машины, где видно номера.")

# Обработка фото
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    photo = update.message.photo[-1].file_id
    caption = f"Фото от пользователя @{user.username or user.first_name} (ID: {user.id})"

    # Отправка админу
    await context.bot.send_photo(chat_id=ADMIN_ID, photo=photo, caption=caption)

    # Ответ пользователю
    await update.message.reply_text("Фото отправлено на проверку. Ожидай ответа.")

# Команда /approve
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])
        await context.bot.send_message(chat_id=user_id, text=f"Доступ одобрен! Вот ссылка для входа: {GROUP_INVITE_LINK}")
        await update.message.reply_text("Ссылка отправлена пользователю.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

# Запуск бота
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(CommandHandler("approve", approve))

app.run_polling()
