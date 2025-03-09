import telebot, random
from config import token

from logic import Pokemon

bot = telebot.TeleBot(token) 

exp = 0
lvl = 1
@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        pokemon = Pokemon(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['feed'])
def feed(message):
    global exp, lvl
    if message.from_user.username in Pokemon.pokemons.keys():
        exp += 10
        bot.reply_to(message, f'''Ты покормил своего покемона😋
Он получил 10 опыта⬆️ Кол-во опыта до следующего уровня: {30 * lvl - exp}''')
        if exp >= 30 * lvl:
            lvl += 1
            bot.reply_to(message, f'''Твой покемон вырос! Теперь у него {lvl} уровень!😊''')
            exp = 0
            if lvl == 5:
                bot.reply_to_to(message, f'Твой покемон стал редким! Теперь у него {lvl} уровень!😊')
    else:
        bot.reply_to(message, "Сначала создай себе покемона")

@bot.message_handler(commands=['pokemon'])
def pokemon(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
        bot.send_message(message.chat.id, f"Кол-во опыта: {exp}, До след. уровня: {30 * lvl - exp}. Уровень: {lvl}")
    else:
        bot.reply_to(message, "Сначала создай себе покемона")


bot.infinity_polling(none_stop=True)

