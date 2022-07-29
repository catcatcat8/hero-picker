import config
import telebot
import json
from pprint import pformat
import difflib

bot = telebot.TeleBot(config.token)

versus = {}

keyboard_base = telebot.types.ReplyKeyboardMarkup(True)
keyboard_base.row('Начать новый драфт', 'Добавить героя', 'Показать контрпики')

heroes = ['anti-mage', 'meepo', 'lone-druid', 'tiny', 'slardar', 'legion-commander', 'phantom-assassin', 'troll-warlord',
        'monkey-king', 'riki', 'templar-assassin', 'io', 'kunkka', 'huskar', 'axe', 'bloodseeker', 'earthshaker',
        'shadow-fiend', 'night-stalker', 'enchantress', 'drow-ranger', 'sven', 'terrorblade', 'hoodwink', 'puck',
        'dawnbreaker', 'elder-titan', 'lina', 'luna', 'spirit-breaker', 'ursa', 'naga-siren', 'disruptor', 'alchemist',
        'shadow-shaman', 'magnus', 'slark', 'earth-spirit', 'crystal-maiden', 'beastmaster', 'tusk', 'nyx-assassin',
        'snapfire', 'lycan', 'broodmother', 'ember-spirit', 'clinkz', 'viper', 'jakiro', 'chen', 'dazzle', 'natures-prophet',
        'outworld-destroyer', 'centaur-warrunner', 'grimstroke', 'silencer', 'lion', 'dragon-knight', 'invoker', 
        'keeper-of-the-light', 'mirana', 'weaver', 'bane', 'windranger', 'bounty-hunter', 'shadow-demon', 'warlock',
        'witch-doctor', 'doom', 'visage', 'pangolier', 'lifestealer', 'rubick', 'phoenix', 'vengeful-spirit', 'gyrocopter',
        'tidehunter', 'leshrac', 'chaos-knight', 'mars', 'faceless-void','timbersaw', 'dark-willow', 'treant-protector',
        'marci', 'pudge', 'dark-seer', 'queen-of-pain', 'sniper', 'venomancer', 'abaddon', 'enigma', 'omniknight',
        'void-spirit', 'phantom-lancer', 'batrider', 'lich', 'bristleback', 'arc-warden', 'undying', 'razor', 'oracle',
        'underlord', 'death-prophet', 'ogre-magi', 'juggernaut', 'techies', 'skywrath-mage', 'clockwerk', 'spectre',
        'wraith-king', 'winter-wyvern', 'brewmaster', 'tinker', 'sand-king', 'morphling', 'necrophos', 'ancient-apparition',
        'pugna', 'storm-spirit', 'zeus', 'medusa', 'primal-beast']

big_heroes = ['Anti-Mage', 'Meepo', 'Lone Druid', 'Tiny', 'Slardar', 'Phantom Assassin', 'Legion Commander', 'Troll Warlord', 
              'Monkey King', 'Riki', 'Templar Assassin', 'Io', 'Kunkka', 'Huskar', 'Axe', 'Bloodseeker', 'Earthshaker', 
              'Shadow Fiend', 'Night Stalker', 'Enchantress', 'Drow Ranger', 'Sven', 'Terrorblade', 'Hoodwink', 'Puck', 
              'Dawnbreaker', 'Elder Titan', 'Lina', 'Spirit Breaker', 'Luna', 'Ursa', 'Naga Siren', 'Disruptor', 'Alchemist', 
              'Shadow Shaman', 'Magnus', 'Slark', 'Earth Spirit', 'Crystal Maiden', 'Beastmaster', 'Nyx Assassin', 'Tusk', 
              'Snapfire', 'Lycan', 'Broodmother', 'Ember Spirit', 'Viper', 'Chen', 'Jakiro', 'Clinkz', 'Dazzle', "Nature's Prophet", 
              'Outworld Destroyer', 'Grimstroke', 'Centaur Warrunner', 'Silencer', 'Lion', 'Invoker', 'Dragon Knight', 
              'Keeper of the Light', 'Mirana', 'Weaver', 'Bane', 'Windranger', 'Shadow Demon', 'Bounty Hunter', 'Warlock', 
              'Witch Doctor', 'Visage', 'Doom', 'Pangolier', 'Lifestealer', 'Rubick', 'Phoenix', 'Vengeful Spirit', 'Gyrocopter', 
              'Tidehunter', 'Leshrac', 'Mars', 'Chaos Knight', 'Faceless Void', 'Timbersaw', 'Dark Willow', 'Treant Protector', 
              'Marci', 'Dark Seer', 'Pudge', 'Queen of Pain', 'Sniper', 'Venomancer', 'Abaddon', 'Enigma', 'Omniknight', 
              'Void Spirit', 'Phantom Lancer', 'Batrider', 'Lich', 'Bristleback', 'Arc Warden', 'Undying', 'Razor', 'Underlord', 
              'Oracle', 'Death Prophet', 'Ogre Magi', 'Juggernaut', 'Techies', 'Skywrath Mage', 'Clockwerk', 'Spectre', 
              'Wraith King', 'Winter Wyvern', 'Brewmaster', 'Tinker', 'Sand King', 'Morphling', 'Necrophos', 'Ancient Apparition', 
              'Pugna', 'Storm Spirit', 'Zeus', 'Medusa', 'Primal Beast']

all_heroes = pformat(sorted(heroes)).replace('[', '')
all_heroes = all_heroes.replace(']', '')
all_heroes = all_heroes.replace(' ', '')
all_heroes = all_heroes.replace("'", '')
all_heroes = all_heroes.replace(',', '')

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Начать новый драфт', 'Добавить героя', 'Показать контрпики')
    bot.send_message(message.chat.id, 'Привет, это контрпикер для Dota 2 от @lebedev666e.\nНажимай начать новый драфт.', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Рофлан здарова')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'bb челик..')
    elif message.text.lower() == 'начать новый драфт' or message.text.lower() == '/new':
        versus[message.chat.id] = []
        msg = bot.send_message(message.chat.id, 'Вводи пики соперников отдельными словами (полностью, первое слово или аббревиатура).\nНапример: "crystal-maiden", "cm", "crystal".\nЕсли не помнишь всех героев, пиши \'/help\').\nРегистр букв при вводе не учитывается.')
        bot.register_next_step_handler(msg, new_draft)

    elif message.text.lower() == 'показать контрпики' or message.text.lower() == '/show':
        opponents = versus.get(message.chat.id) 
        if not opponents is None and len(opponents) > 0:
            counterpicks = return_counters(opponents)
            counterpicks = sort_by_value(counterpicks)
            counterpicks_str = return_dict_as_table(counterpicks)
            msg = bot.send_message(message.chat.id, f'Список контрпиков против {opponents} снизу.\nЧем больше значение, тем лучше герой.')
            msg = bot.send_message(message.chat.id, f'{counterpicks_str}', parse_mode="Markdown")
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            return
        else:
            msg = bot.send_message(message.chat.id, 'Сначала введи хотя бы одного героя')
            bot.register_next_step_handler(msg, new_draft)

    elif message.text.lower() == 'добавить героя' or message.text.lower() == '/add':
        opponents = versus.get(message.chat.id)
        if opponents is None:
            versus[message.chat.id] = [] 
        if len(versus[message.chat.id]) < 5:
            msg = bot.send_message(message.chat.id, 'Вводи пики соперников отдельными словами (полностью, первое слово или аббревиатура).\nНапример: "crystal-maiden", "cm", "crystal".\nЕсли не помнишь всех героев, пиши \'/help\').\nРегистр букв при вводе не учитывается.')
            bot.register_next_step_handler(msg, new_draft)
        else:
            msg = bot.send_message(message.chat.id, 'Ты уже ввел 5 героев, больше добавить нельзя.\nМожешь начать новый драфт.')

    elif message.text.lower() == '/help':
        bot.send_message(message.chat.id, 'Вот список всех героев.\nЕсли название героя содержит более одного слова, можешь вводить первые буквы этих слов или первое слово.\nНапример: "crystal-maiden", "cm", "crystal"')
        bot.send_message(message.chat.id, all_heroes)
    
def new_draft(message):
    if message.text.lower() == 'показать контрпики' or message.text.lower() == '/show':
        opponents = versus.get(message.chat.id)
        if not opponents is None and len(opponents) > 0:
            counterpicks = return_counters(opponents)
            counterpicks = sort_by_value(counterpicks)
            counterpicks_str = return_dict_as_table(counterpicks)
            msg = bot.send_message(message.chat.id, f'Список контрпиков против {opponents} снизу.\nЧем больше значение, тем лучше герой.')
            msg = bot.send_message(message.chat.id, f'{counterpicks_str}', parse_mode="Markdown")
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            return
        else:
            msg = bot.send_message(message.chat.id, 'Сначала введи хотя бы одного героя')
            bot.register_next_step_handler(msg, new_draft)
    
    elif message.text.lower() == 'начать новый драфт' or message.text.lower() == '/new':
        versus[message.chat.id] = []
        msg = bot.send_message(message.chat.id, 'Вводи пики соперников отдельными словами (полностью, первое слово или аббревиатура).\nНапример: "crystal-maiden", "cm", "crystal".\nЕсли не помнишь всех героев, пиши \'/help\').\nРегистр букв при вводе не учитывается.')
        bot.register_next_step_handler(msg, new_draft)
        return

    elif message.text.lower() == 'добавить героя' or message.text.lower() == '/add':
        opponents = versus.get(message.chat.id)
        if opponents is None:
            versus[message.chat.id] = []
        if len(versus.get(message.chat.id)) < 5:
            msg = bot.send_message(message.chat.id, 'Вводи пики соперников отдельными словами (полностью, первое слово или аббревиатура).\nНапример: "crystal-maiden", "cm", "crystal".\nЕсли не помнишь всех героев, пиши \'/help\').\nРегистр букв при вводе не учитывается.')
            bot.register_next_step_handler(msg, new_draft)
        else:
            msg = bot.send_message(message.chat.id, 'Ты уже ввел 5 героев, больше добавить нельзя.\nМожешь начать новый драфт.')
            bot.register_next_step_handler(msg, new_draft)

    elif message.text.lower() == '/start':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Начать новый драфт', 'Добавить героя', 'Показать контрпики')
        bot.send_message(message.chat.id, 'Привет, это контрпикер для Dota 2 от @lebedev666e.\nНажимай начать новый драфт.', reply_markup=keyboard)
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    
    elif message.text.lower() == '/help':
        bot.send_message(message.chat.id, 'Вот список всех героев.\nЕсли название героя содержит более одного слова, можешь вводить первые буквы этих слов или первое слово.\nНапример: "crystal-maiden", "cm", "crystal"')
        msg = bot.send_message(message.chat.id, all_heroes)
        bot.register_next_step_handler(msg, new_draft)

    elif len(versus.get(message.chat.id)) < 5:
        predict_if_hero_not_found = ''
        possible_heroes = []

        for hero in heroes:
            str = ""
            if ('-') in hero:
                for word in hero.split('-'):
                    str += word[0] 
            if hero == message.text.lower() or hero.split('-')[0] == message.text.lower() or str == message.text.lower():
                possible_heroes.append(hero)
        if len(possible_heroes) == 1:
            if not ''.join(possible_heroes) in versus.get(message.chat.id):
                versus[message.chat.id].append(''.join(possible_heroes))
                msg = bot.send_message(message.chat.id, f'Добавлен герой: {"".join(possible_heroes)}\nЕще можно ввести героев: {5-len(versus.get(message.chat.id))}.\nЛибо нажми кнопку меню и посмотри контрпики.')
            else:
                msg = bot.send_message(message.chat.id, f"Ты уже добавлял этого героя.\nЕще можно ввести героев: {5-len(versus.get(message.chat.id))}.\nЛибо нажми кнопку меню и посмотри контрпики.")
        elif len(possible_heroes) == 0:
            predict_if_hero_not_found = difflib.get_close_matches(message.text.lower(), heroes)
            msg = bot.send_message(message.chat.id, "Ты неправильно ввел вражеского героя.\nВот примеры корректного ввода: 'crystal-maiden', 'luna'.\nМожешь посмотреть всех героев, написав '/help'")
            if len(predict_if_hero_not_found) > 0:
                msg = bot.send_message(message.chat.id, f'Может быть ты имел в виду: {predict_if_hero_not_found}?')
        elif len(possible_heroes) > 1:
            keyboard_choose_hero = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard_choose_hero.row(*possible_heroes)
            msg = bot.send_message(message.chat.id, text="Какого из этих героев вы имели в виду?",  reply_markup=keyboard_choose_hero)
            bot.register_next_step_handler(msg, choose, *possible_heroes)
            return
        bot.register_next_step_handler(msg, new_draft)
        return
    else:
        msg = bot.send_message(message.chat.id, 'Ты уже ввел 5 героев, нажимай "Показать контрпики"')

def choose(message, *args):
    hero_already_added = False
    hero_found = False
    added_hero = ''
    for hero in args:
        if message.text.lower() == hero:
            if not hero in versus.get(message.chat.id):
                versus[message.chat.id].append(hero)
                hero_found = True
                added_hero = hero
            else:
                hero_already_added = True
            break
    if not hero_already_added and hero_found:
        msg = bot.send_message(message.chat.id, text = f'Добавлен герой: {added_hero}\nЕще можно ввести героев: {5-len(versus.get(message.chat.id))}.\nЛибо нажми кнопку меню и посмотри контрпики.', reply_markup=keyboard_base)
    elif hero_already_added:
        msg = bot.send_message(message.chat.id, f"Ты уже добавлял этого героя.\nЕще можно ввести героев: {5-len(versus.get(message.chat.id))}.\nЛибо нажми кнопку меню и посмотри контрпики.", reply_markup=keyboard_base)
    else:
        msg = bot.send_message(message.chat.id, "Ошибка (нужно было выбрать героя из показанного меню).\nПопробуй добавить героя еще раз", reply_markup=keyboard_base)
    bot.register_next_step_handler(msg, new_draft)  

def return_counters(versus):

    with open('./heropicker/spiders/dump.json') as json_file:
        data = json.load(json_file)
        
        opponents = []
        for hero in versus:
            for hero_json in data:
                if hero_json["Hero"] == hero:
                    opponents.append(hero_json)

        counters = {}

        versus_tmp = [i.replace("-", "").lower() for i in versus] 
  
        for each_opponent in opponents:
            for a_h in big_heroes:
                if not each_opponent.get(a_h) is None and not a_h.replace(" ", "").lower() in versus_tmp:
                    if (counters.get(a_h) is None):
                        counters[a_h] = each_opponent.get(a_h)
                    else:
                        counters[a_h] = round(counters[a_h] + each_opponent.get(a_h), 2)

        return counters

def sort_by_value(versus):
    sorted_tuple = sorted(versus.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_tuple)
    
def return_dict_as_table(versus):
    tmpstring = "```\n"
    tmpstring += "Герой                Значение\n"

    for key, value in versus.items():
        tmpstring = tmpstring + "{0:<20} {1}".format(key, value) + "\n"
    tmpstring += '```'

    return tmpstring

def main():
    bot.infinity_polling(timeout=10, long_polling_timeout = 5)

if __name__ == "__main__":
    main()
