from random import randint
import requests 

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer, level=1, exp=0, race = "❔Не определён", wins=0, upgrade=3):

        self.pokemon_trainer = pokemon_trainer   
        self.race = race
        self.upgrade = upgrade
        self.wins = wins

        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.abilities = self.get_abilities()
        self.exp = exp
        self.level = level
        self.hp = randint(150, 250)
        self.max_hp = self.hp
        self.power = randint(25,40)

        Pokemon.pokemons[pokemon_trainer] = self



    # Метод для получения способности покемона через API
    def get_abilities(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['abilities'][0]['ability']['name'])
        else:
            return "Pikachu"
        

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']['front_default'])
        else:
            return "Pikachu"


    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"
        



   # def attack(self, enemy):
    #    chacne = randint(1,5)
     #   
       # super_power = randint(5, 10)
      #  self.power += super_power
        #result = super().attack(enemy)
        #self
        #return result + f'\n\n🔥 Покемон-воин активировал супер способность и усилил свою атаку на {super_power} урона!'
    
    # Метод для атаки
    def attack(self, enemy):
        if isinstance(enemy, Wizard):
            if randint(1,5) == 4:
                return f'🛡️Покемон-волшебник @{self.pokemon_trainer} применил супер щит и отразил атаку питомца @{enemy.pokemon_trainer}!'

            if isinstance(self, Fighter):
                if randint(1,5) == 4:
                    super_power = randint(5, 10)
                    super_attack = self.power + super_power
                    enemy.hp -= super_attack
                    return (f'⚔️Покемон-воин @{self.pokemon_trainer} активировал супер способность и усилил свою атаку ДО {super_attack} урона!\n\n'
                            f'⚔️ @{self.pokemon_trainer} атаковал @{enemy.pokemon_trainer} и нанёс {self.power} урона!\n'
                            f'❤️ У @{enemy.pokemon_trainer} осталось {enemy.hp}❤️')
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return (f'⚔️ @{self.pokemon_trainer} атаковал @{enemy.pokemon_trainer} и нанёс {self.power} урона!\n\n'
                    f'❤️ У @{enemy.pokemon_trainer} осталось {enemy.hp}❤️')
        else:
            enemy.hp = 0
            self.wins += 1
            self.exp += 10
            if self.exp >= 30 * self.level:
                self.level += 1
                self.exp = 0
                if self.level == self.upgrade:
                    pow = randint(4, 10)
                    self.power += pow
                    self.upgrade += 2 
                
                return (f'💀 @{self.pokemon_trainer} поразил @{enemy.pokemon_trainer} насмерть, атакуя на {self.power} урона! @{enemy.pokemon_trainer} повержен!\n\n'
                        f'🏆 @{self.pokemon_trainer} одержал победу в схватке! \n'
                        f'🎉 @{self.pokemon_trainer}, Твой покемон вырос и теперь у него {self.level} уровень!')
                
                
            else:

                return (f'💀 @{self.pokemon_trainer} поразил @{enemy.pokemon_trainer} насмерть, атакуя на {self.power} урона! @{enemy.pokemon_trainer} повержен!\n\n'
                        f'🏆 @{self.pokemon_trainer} одержал победу в схватке! \n'
                        f'🎉 @{self.pokemon_trainer}, Твой покемон получил 10 опыта!')



# Раса покемона 
    # Метод класса для получения информации
    def info(self):
        return (f'📄 Профиль твоего покемона \n\n'
                f"🦊 Имя твоего покемона: {self.name} \n"
                f"🧬 Раса: {self.race} \n"
                f"⚡ Способности: {self.abilities} \n"
                f"🗡️ Сила: {self.power} \n"
                f"🏆 Победы: {self.wins}\n"
                f"❤️ Здоровье: {self.hp} \n"
                f"🔥 Уровень: {self.level}, Опыт: {self.exp} \n"
                f"🫅 Тренер: {self.pokemon_trainer} \n")


    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img


class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.race = "🧙 Волшебник"


class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.race = "⚔️ Воин"