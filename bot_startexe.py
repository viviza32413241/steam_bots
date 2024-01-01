import telebot
import requests
import os
import config

bot = telebot.TeleBot(config.token)

api = config.steam_api
steam_id = config.steam_id

api_url = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key="+api+"&steamid="+steam_id+"&format=json"

class game:
    def __init__(self, appid, name):
        self.appid = appid
        self.name = name
        
games = []
total_count = 0

@bot.message_handler(commands=['start'])
def send_statistics(message):
    global games
    global total_count
    response = requests.get(api_url)
    array_all = response.json()
    bot.send_message(message.chat.id, "Оберіть гру, яку бажаєте запустити: ")
    total_count = array_all['response']['total_count']
    array_stat = array_all['response']['games']
    text=""
    for i in array_stat:
        games.append(game(i['appid'], i['name']))
    for i in range(total_count):
        text += str(i+1) +". "+ games[i].name + "\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def message(message):
    global games, total_count
    try:
        i = int(message.text)
        if(i>0 and i<=total_count):
            os.system('start steam://rungameid/'+str(games[i-1].appid))
            bot.send_message(message.chat.id, str(games[i-1].name)+" успішно запускається!")
        else:
            bot.send_message(message.chat.id, "Число не вірне. Спробуйте знову")
    except:
        bot.send_message(message.chat.id, "Введіть число, даний текст не є числом")

bot.infinity_polling()