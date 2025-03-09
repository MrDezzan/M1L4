import telebot, time, random
from config import token
from logic import Pokemon

bot = telebot.TeleBot(token) 
feedcooldown = 0
lastfeed ={}
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет! Я бот, который поможет тебе создать своего покемона.🐣 Для этого напиши /go 😉')
@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        pokemon = Pokemon(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, 'Ты уже создал себе покемона')

@bot.message_handler(commands=['feed'])
def feed(message):
    user_id = (message.from_user.id)
    current_time = time.time()

    if message.from_user.username in Pokemon.pokemons.keys():   

        if user_id in lastfeed and current_time - lastfeed[user_id] < feedcooldown:

            remain_time = int(feedcooldown - (current_time - lastfeed[user_id]))
            bot.reply_to(message, f'❌ Подожди {remain_time // 60} мин. {remain_time % 60} сек. перед следующим кормлением!') 
            return
        
        pokemon = Pokemon.pokemons[message.from_user.username]
        lastfeed[user_id] = current_time
        expgain = random.randint(5, 15)
        pokemon.exp += expgain
        
        if pokemon.exp >= 30 * pokemon.level:
            pokemon.level += 1
            bot.reply_to(message, f'''Ты покормил {pokemon.name}, и он вырос! Теперь у него {pokemon.level} уровень!😊''')
            pokemon.exp = 0

            if pokemon.level == 5:
                bot.reply_to(message, f"Твой покемон стал редким! Теперь у него {pokemon.level} уровень!😊")
        else:
            bot.reply_to(message, f'''Ты покормил {pokemon.name}😋
Он получил {expgain} опыта⬆️ Кол-во опыта до следующего уровня: {30 * pokemon.level - pokemon.exp}''')
    else:
        bot.reply_to(message, 'Сначала создай себе покемона')


@bot.message_handler(commands=['pokemon'])
def pokemon(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
        bot.send_message(message.chat.id, f"Кол-во опыта: {pokemon.exp}, До след. уровня: {30 * pokemon.level - pokemon.exp}. Уровень: {pokemon.level}")
    else:
        bot.reply_to(message, 'Сначала создай себе покемона')

@bot.message_handler(commands=['info'])
def info(message):
    bot.reply_to(message, '''- Этот бот создан для того, чтобы ты мог создать себе покемона и кормить его.🐥
🔶 Автор: @sirdezzan
💠 Версия бота: 0.2''')

bot.infinity_polling(none_stop=True)

