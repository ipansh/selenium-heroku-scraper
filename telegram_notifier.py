import requests

def send_message(text, telegram_token):
### permissions for telegram bot token
    bot_url = "https://api.telegram.org/bot{}/".format(telegram_token)
    url = bot_url + "sendMessage?text={}&chat_id={}".format(text, 33651759)
    return requests.get(url)