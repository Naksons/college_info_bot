import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes


# Загрузка данных
def load_data(filename):
    with open(f"data/{filename}", "r", encoding="utf-8") as f:
        return json.load(f)


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    🎓 <b>Добро пожаловать в информационный бот колледжа!</b>

    Доступные команды:
    /start - Начать работу
    /help - Список команд
    /schedule - Расписание звонков
    /contacts - Контакты отделов
    /news - Последние новости
    /faq - Частые вопросы
    """
    await update.message.reply_text(help_text, parse_mode="HTML")


# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)  # Используем ту же логику, что и в /start


# Команда /contacts
async def send_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contacts = """
    📞 <b>Контакты отделов:</b>

    <b>Приёмная комиссия:</b>
    Телефон: +7(863)210-79-94

    <b>Зам. директора:</b>
  Заместитель директора по учебной работе. Телефон: +7(863)267-34-33
  Заместитель директора по воспитательной работе. Телефон: +7(863)267-53-44
    <b>Канцелярия:</b>
    Телефон: +7(863)267-51-77
    """
    await update.message.reply_text(contacts, parse_mode="HTML")


# Команда /schedule
async def send_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    schedule = """
    📅 <b>Расписание звонков:</b>
    1 пара: 8:00 - 9:35
    2 пара: 9:45 - 11:20
    3 пара: 11:50 - 13:25
    4 пара: 13:35 - 15:10
    5 пара: 15:20 - 16:55
    6 пара: 17:05 - 18:40
    7 пара: 18:50 - 20:35
    """
    await update.message.reply_text(schedule, parse_mode="HTML")


# Команда /news
async def send_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news = load_data("news.json")[:3]  # Последние 3 новости
    response = "📢 <b>Последние новости:</b>\n" + "\n".join([f"{n['date']}: {n['text']}" for n in news])
    await update.message.reply_text(response, parse_mode="HTML")


# Команда /faq с кнопками
async def send_faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    faq = load_data("faq.json")
    keyboard = [[InlineKeyboardButton(q, callback_data=q)] for q in faq.keys()]
    await update.message.reply_text("❓ <b>Выберите вопрос:</b>",
                                    reply_markup=InlineKeyboardMarkup(keyboard),
                                    parse_mode="HTML")


# Обработка нажатий на кнопки FAQ
async def faq_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    faq = load_data("faq.json")
    await query.answer()
    await query.edit_message_text(text=f"❓ <b>{query.data}</b>\n\n{faq[query.data]}",
                                  parse_mode="HTML")


def main():
    app = Application.builder().token("7572317798:AAFLOyja0VXANOW_ad-NexUxNYMt5Lk5AUY").build()

    # Регистрация обработчиков команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("contacts", send_contacts))
    app.add_handler(CommandHandler("schedule", send_schedule))
    app.add_handler(CommandHandler("news", send_news))
    app.add_handler(CommandHandler("faq", send_faq))
    app.add_handler(CallbackQueryHandler(faq_button))

    app.run_polling()


if __name__ == "__main__":
    main()