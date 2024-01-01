import requests
import telebot
from telebot import types
import config

bot=telebot.TeleBot(config.token)

api=config.steam_api
steam_id={}
steam_id_bool={}


@bot.message_handler(commands=['statistics'])
def send_statistics(message):
	api_url = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key="+api+"&steamid="+steam_id[message.chat.id]+"&format=json"
	response = requests.get(api_url)
	array_all = response.json()
	array_stat = array_all['response']['games']
	for i in array_stat:
		last2week=i['playtime_2weeks']/60
		alltime=i['playtime_forever']/60 
		text=i['name']+"\n - Зіграно за останні 2 тижні: %.1f" %last2week +" годин\n - Зіграно загалом: %.1f" %alltime +" годин"
		bot.send_message(message.chat.id, text)
	



@bot.message_handler(commands=['start'])
def send_start(message):
	text="Steam analytics"
	bot.send_message(message.chat.id, text, reply_markup=keyboard_start())

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
	global steam_id, steam_id_bool
	if(call.data=='start'):
		steam_id_bool[call.message.chat.id]=False
		bot.send_message(call.message.chat.id, 'Enter your id steam(Publicly available ur acc): ')

@bot.message_handler(content_types=['text'])
def message(message):
	if(not steam_id_bool[message.chat.id]):
		steam_id[message.chat.id]=message.text
		steam_id_bool[message.chat.id]=True
		bot.send_message(message.chat.id, 'Good. Try /statistics')


def keyboard_start():
	markup = types.InlineKeyboardMarkup()
	itembtn1 = types.InlineKeyboardButton(text='Enter new id', callback_data='start')
	markup.add(itembtn1)
	return markup



bot.infinity_polling()
