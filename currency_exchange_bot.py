from secret import BOT_KEY
import telebot
import requests
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

bot = telebot.TeleBot(BOT_KEY)


@bot.message_handler(commands=['list'])
def currency_exchange(message):
    bot.send_message(message.chat.id, get_latest())


@bot.message_handler(commands=['exchange'])
def exchange(message):
    bot.send_message(message.chat.id, get_exchange(message))


@bot.message_handler(commands=['history'])
def history(message):
    answer = get_history(message)
    if type(answer) == str:
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_photo(message.chat.id, photo=open("img.png", "rb"))


def get_history_json(start_at, end_at, base, symbols):
    response = requests.get("http://api.exchangeratesapi.io/history",
                            params={'start_at': start_at, 'end_at': end_at, 'base': base, 'symbols': symbols})
    json_data = response.json()
    return json_data


def get_latest_json(base):
    response = requests.get("http://api.exchangeratesapi.io/latest", params={'base': base})
    json_data = response.json()
    return json_data


def get_text_from_latest(json_data):
    answer = ""
    keys = list(json_data['rates'].keys())
    values = list(json_data['rates'].values())
    for item in range(len(keys)):
        answer += str(keys[item]) + ": " + str(float('{:.2f}'.format(float(values[item])))) + "\n"
    return answer


def get_latest():
    with open("db.json", 'r') as file:
        s = file.read()
    dictionary = json.loads(s)
    datetime_str = dictionary['date']
    then = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
    duration = datetime.now() - then
    if divmod(duration.total_seconds(), 60)[0] > 10:
        json_data = get_latest_json("USD")
        json_data['date'] = str(datetime.now())
        with open("db.json", 'w') as file:
            file.write(json.dumps(json_data))
        answer = get_text_from_latest(json_data)
    else:
        answer = get_text_from_latest(dictionary)
    return answer


def get_exchange(message):
    try:
        message_splited = message.text.split()
        json_data = get_latest_json(message_splited[2])
        temporary = get_latest_json(message_splited[4])
        amount = int(message_splited[1])
        answer = str(float('{:.2f}'.format(json_data['rates'][message_splited[4]] * amount)))
    except Exception:
        answer = "Parameters are incorrect"
    return answer


def get_history(message):
    try:
        message_splited = message.text.split()
        base_and_symbol = message_splited[1].split('/')
        now = datetime.now().date()
        then = now - timedelta(days=7)
        json_data = get_history_json(then, now, base_and_symbol[0], base_and_symbol[1])
        keys = list(json_data['rates'].keys())
        values = list(json_data['rates'].values())
        values_int = []
        for item in range(len(values)):
            values_int.append(float(values[item][base_and_symbol[1]]))
        plt.plot(keys, values_int)
        answer = plt.savefig("img.png")
    except Exception:
        answer = "Parameters are incorrect or No exchange rate data is available for the selected currency"
    return answer


bot.polling()
