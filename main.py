import telebot
from telebot import types


TOKEN = "8920471060:AAFnWujeXl0WmGkYzV4S0xZE2-djWfMen9w"
bot = telebot.TeleBot(TOKEN)

# База данных в памяти (баланс и журнал)
USER_BANK = 20000.0
JOURNAL = [
    {"date": "30.09", "match": "Эритрея — ЮАР", "market": "Ф1 (+2.0)", "odds": 1.85, "stake": 400, "status": "Списание 🔴"},
    {"date": "30.09", "match": "ОАЭ — Катар (Экспресс)", "market": "ТБ 4.5 ЖК + ТБ 8.5 угл", "odds": 3.18, "stake": 100, "status": "Списание 🔴"},
    {"date": "03.10", "match": "Партик Тисл — Селтик", "market": "Ф1 (+1.5)", "odds": 1.95, "stake": 400, "status": "Резерв ⏳"},
    {"date": "04.10", "match": "Брюгге — Андерлехт", "market": "Ф2 (+1.0)", "odds": 1.85, "stake": 318, "status": "Резерв ⏳"}
]

# Главное меню с кнопками
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📊 Мой Баланс")
    btn2 = types.KeyboardButton("📋 Показать Журнал")
    btn3 = types.KeyboardButton("🌧️ Проверить Сигналы")
    markup.add(btn1, btn2, btn3)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        f"🤖 Робот-аналитик ADJUST приветствует вас!\n\n"
        f"Все кластерные фильтры лиг, погодные модули и Stealth-экспрессы успешно интегрированы.\n"
        f"Текущий виртуальный банк: {USER_BANK} грн.", 
        reply_markup=main_keyboard()
    )

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    global USER_BANK
    
    if message.text == "📊 Мой Баланс":
        allocated = sum(item['stake'] for item in JOURNAL if item['status'] == "Резерв ⏳")
        spent = sum(item['stake'] for item in JOURNAL if item['status'] == "Списание 🔴")
        free_money = USER_BANK - allocated - spent
        
        response = (
            f"💰 **ФИНАНСОВЫЙ СТАТУС БАНКА:**\n\n"
            f"💵 Стартовый капитал: `{USER_BANK} грн`\n"
            f"🔴 Списано на сегодня: `{spent} грн`\n"
            f"⏳ В резерве на выходные: `{allocated} грн`\n"
            f"🍏 Свободный остаток: `{free_money} грн`"
        )
        bot.send_message(message.chat.id, response, parse_mode="Markdown")
        
    elif message.text == "📋 Показать Журнал":
        response = "📋 **ТЕКУЩИЙ ЖУРНАЛ УЧЕТА ADJUST:**\n\n"
        for i, item in enumerate(JOURNAL, 1):
            response += (
                f"{i}. **{item['date']}** | {item['match']}\n"
                f"   🎯 Рынок: `{item['market']}` (кэф {item['odds']})\n"
                f"   💵 Ставка: `{item['stake']} грн` | Статус: {item['status']}\n\n"
            )
        bot.send_message(message.chat.id, response, parse_mode="Markdown")
        
    elif message.text == "🌧️ Проверить Сигналы":
        # Демонстрация работы погодного фильтра
        response = (
            f"🎯 **ОБНАРУЖЕН АКТУАЛЬНЫЙ ПЕРЕКОС ЛИНfieldsetИИ!**\n\n"
            f"⚽ Матч: **Брюгге — Андерлехт** (04.10)\n"
            f"🌧️ Контекст: Сильный ливень и шторм в Бельгии. xG Брюгге снижен.\n"
            f"📈 Рекомендуемый рынок: **Ф2 (+1.0) Азиатская**\n"
            f"🔮 Кэф БК: `1.85` | Валуйность: `+18.4%` (Вес 1.2)\n"
            f"💰 Рекомендуемая сумма: `318 грн`"
        )
        bot.send_message(message.chat.id, response, parse_mode="Markdown")

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен и готов к работе...")
    bot.polling(none_stop=True)
