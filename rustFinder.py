import requests
import config
import telebot

bot=telebot.TeleBot(config.token2)
steamkey=config.steam_key

list_options=["deaths", 'bullet fired', 'kill player', 'bullet hit player', 'headshot', 'harvested wood', 'harvested stones']
url="https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=252490&key="+steamkey+"&steamid="
url_profile="https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key="+steamkey+"&steamids="

@bot.message_handler(commands=['start'])
def send_statistics(message):
    bot.send_message(message.chat.id, "Enter your SteamID to check your stats: ")


@bot.message_handler(content_types=['text'])
def message(message):
    global list_options, url
    try:
        i = int(message.text)
        try:
            response = requests.get(url+message.text)
            username = requests.get(url_profile+message.text).json()['response']['players'][0]['personaname']
            array_all = response.json()
            stats = array_all['playerstats']['stats']
            dict_stats = {}
            dict_stats['K/D'] = 0
            dict_stats['H/F'] = 0
            dict_stats['Headshots on hit'] = 0
            for el in stats:
                el['name']=" ".join(el['name'].split("_"))
                if(el['name'] in list_options):
                    dict_stats[el['name']]=el['value']
            dict_stats['K/D'] = dict_stats['kill player'] / dict_stats['deaths']
            dict_stats['H/F'] = dict_stats['bullet hit player'] / dict_stats['bullet fired']
            dict_stats['Headshots on hit'] = dict_stats['headshot'] / dict_stats['bullet hit player']
            text="Username - " + username + "\n"
            for i, n in dict_stats.items():
                i=i[0].upper()+i[1:]
                text += "<b>" + i + "</b> - " + str(n) + "\n"
            bot.send_message(message.chat.id, text, parse_mode="html")
            bot.send_message(message.chat.id, "You can again enter SteamID")
        except:
            bot.send_message(message.chat.id, "Error: Enter correct SteamID.")
    except:
        bot.send_message(message.chat.id, "Error: Enter correct steamID.")
    

bot.infinity_polling()


