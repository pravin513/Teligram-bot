import requests
import time
import phonenumbers
from phonenumbers import timezone, geocoder, carrier
import os

# BotFather से मिला टोकन (Heroku Config Vars से लेंगे)
BOT_TOKEN = os.environ.get("8318133167:AAExGbPgHEtNFH_acr3qqsCkgfGKkX7ZPWM")
URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

offset = 0

def get_updates():
    global offset
    response = requests.get(URL + "/getUpdates", params={"offset": offset}).json()
    if "result" in response:
        for item in response["result"]:
            offset = item["update_id"] + 1
            yield item

def send_message(chat_id, text):
    requests.get(URL + "/sendMessage", params={"chat_id": chat_id, "text": text})

def phone_info(number):
    try:
        phoneNumber = phonenumbers.parse(number)
        if not phonenumbers.is_valid_number(phoneNumber):
            return "❌ Invalid phone number!"

        timeZone = timezone.time_zones_for_number(phoneNumber)
        geolocation = geocoder.description_for_number(phoneNumber, "en")
        service = carrier.name_for_number(phoneNumber, "en")

        return (
            f"📞 Phone Number: {number}\n"
            f"🕒 Timezone: {timeZone}\n"
            f"📍 Location: {geolocation}\n"
            f"📡 Service Provider: {service if service else 'Unknown'}"
        )
    except Exception as e:
        return f"⚠️ Error: {e}"

def main():
    print("🤖 Bot is running...")
    while True:
        for update in get_updates():
            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "")

            if text == "/start":
                send_message(chat_id, "👋 Send me a phone number with country code (e.g. +919876543210)")
            else:
                reply = phone_info(text)
                send_message(chat_id, reply)
        time.sleep(1)

if __name__ == "__main__":
    main()
