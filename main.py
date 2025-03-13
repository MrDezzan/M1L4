import telebot, time, random
from config import token
from logic import Pokemon, Fighter, Wizard

bot = telebot.TeleBot(token) 
feedcooldown = 150
lastfeed ={}



@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет! Я бот, который поможет тебе создать своего покемона.🐣 Для этого напиши /go 😉')
@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        race = random.randint(1,2)
        if race == 2:
            pokemon = Fighter(message.from_user.username)
        else:
            pokemon = Wizard(message.from_user.username)
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
        if pokemon.level == pokemon.upgrade:
            pow = random.randint(4, 10)
            pokemon.power += pow
            pokemon.upgrade += 2 
        
        if pokemon.exp >= 30 * pokemon.level:
            pokemon.level += 1
            bot.reply_to(message, f'''Ты покормил {pokemon.name}, и он вырос! Теперь у него {pokemon.level} уровень!😊''')
            pokemon.exp = 0
            pow=random.randint(4,10)
            if pokemon.level == pokemon.upgrade:
                pow = random.randint(4, 10)
                pokemon.power += pow
                pokemon.upgrade += 2 

        
        else:
            bot.reply_to(message, f'''Ты покормил {pokemon.name}😋
Он получил {expgain} опыта⬆️ Кол-во опыта до следующего уровня: {30 * pokemon.level - pokemon.exp}''')
            pow=random.randint(4,10)
            if pokemon.level == pokemon.upgrade:
                pow = random.randint(4, 10)
                pokemon.power += pow
                pokemon.upgrade += 2 
    else:
        bot.reply_to(message, 'Сначала создай себе покемона')

@bot.message_handler(commands=['attack'])
def attack(message):
    if not message.reply_to_message or not message.reply_to_message.from_user:
        bot.send_message(message.chat.id, "⚠️ Ответь этой командой на сообщение противника, чтобы напасть!")
        return
    
    attacker_username = message.from_user.username
    defender_username = message.reply_to_message.from_user.username

    attacker = Pokemon.pokemons[attacker_username]
    defender = Pokemon.pokemons[defender_username]
    
    if attacker_username not in Pokemon.pokemons or defender_username not in Pokemon.pokemons:
        bot.send_message(message.chat.id, "❌ Оба игрока должны иметь покемонов для боя!")
        return

    bot.send_message(message.chat.id, f"🔥 @{defender_username}, вы готовы сразиться с @{attacker_username}? Ответьте 'Да' или 'Нет")
    bot.register_next_step_handler(message.reply_to_message, attack_confirm, attacker, defender)


def attack_confirm(message, attacker, defender):  

    if message.text.strip().lower() == "да":
        bot.send_message(message.chat.id, "🔥 Битва началась! ⚔️")
        while attacker.hp > 0 and defender.hp > 0:
            if defender.hp <= 50:
                bot.send_message(message.chat.id, f'😰 Питомец @{defender.pokemon_trainer} зарычал от усталости: Кхкххх...!')
            if attacker.hp <= 50:
                bot.send_message(message.chat.id, f'😰 Питомец @{attacker.pokemon_trainer} зарычал от усталости: Кхкххх...!')


            result = attacker.attack(defender)
            bot.send_message(message.chat.id, result)
            time.sleep(2) 
            if defender.hp > 0:
                result = defender.attack(attacker)
                bot.send_message(message.chat.id, result)
            time.sleep(4) 
        defender.hp = defender.max_hp
        attacker.hp = attacker.max_hp
        bot.send_message(message.chat_id, "🎮 Битва завершена! Вы можете вызвать нового противника командой /attack")
    else:
        bot.send_message(message.chat.id, "⚔️ Битва отменена! Противник отказался от сражения.")



@bot.message_handler(commands=['pokemon'])
def pokemon(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, pokemon.info())
    else:
        bot.reply_to(message, 'Сначала создай себе покемона')

@bot.message_handler(commands=['info'])
def info(message):
    bot.reply_to(message, '''- Этот бот создан для того, чтобы ты мог создать себе покемона и кормить его.🐥
🔶 Автор: @sirdezzan
💠 Версия бота: 0.3!''')

bot.infinity_polling(none_stop=True)

