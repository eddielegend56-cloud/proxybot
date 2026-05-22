import os
import telebot
import requests
from flask import Flask, request

# ====================================
# BOT TOKEN
# ====================================

BOT_TOKEN = os.getenv("8821238721:AAGG1oosX4pQ6K9vflZRZ5tlLL79CxiWwSQ")

bot = telebot.TeleBot(BOT_TOKEN)

# ====================================
# WEBHOOK SETTINGS
# ====================================

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)

# ====================================
# FETCH PROXIES
# ====================================

def fetch_proxies(protocol="http", limit=5):

    url = (
        "https://proxylist.geonode.com/api/proxy-list"
        f"?limit={limit}"
        "&page=1"
        "&sort_by=lastChecked"
        "&sort_type=desc"
        f"&protocols={protocol}"
    )

    try:

        response = requests.get(url, timeout=15)
        data = response.json()

        results = []

        for proxy in data.get("data", []):

            ip = proxy.get("ip", "Unknown")
            port = proxy.get("port", "Unknown")
            country = proxy.get("country", "Unknown")
            city = proxy.get("city", "Unknown")
            latency = proxy.get("latency", "Unknown")

            if isinstance(latency, int):

                if latency <= 100:
                    quality = "🔥 VERY FAST"

                elif latency <= 300:
                    quality = "⚡ FAST"

                else:
                    quality = "🟡 NORMAL"

            else:
                quality = "Unknown"

            text = (
                f"🌍 Country: {country}\n"
                f"🏙 Region: {city}\n"
                f"📡 IP: {ip}\n"
                f"🚪 Port: {port}\n"
                f"⚡ Ping: {latency} ms\n"
                f"🔥 Speed: {quality}\n"
                f"━━━━━━━━━━━━━━━"
            )

            results.append(text)

        return results

    except Exception as e:

        print(e)
        return []

# ====================================
# START COMMAND
# ====================================

@bot.message_handler(commands=['start'])
def start(message):

    text = (
        "🤖 PROXY BOT ONLINE\n\n"
        "/http - HTTP proxies\n"
        "/socks4 - SOCKS4 proxies\n"
        "/socks5 - SOCKS5 proxies\n"
    )

    bot.reply_to(message, text)

# ====================================
# HTTP
# ====================================

@bot.message_handler(commands=['http'])
def http_proxy(message):

    bot.reply_to(message, "🔄 Fetching HTTP proxies...")

    proxies = fetch_proxies("http")

    if proxies:

        bot.reply_to(
            message,
            "\n\n".join(proxies)
        )

    else:

        bot.reply_to(message, "❌ Failed.")

# ====================================
# SOCKS4
# ====================================

@bot.message_handler(commands=['socks4'])
def socks4_proxy(message):

    bot.reply_to(message, "🔄 Fetching SOCKS4 proxies...")

    proxies = fetch_proxies("socks4")

    if proxies:

        bot.reply_to(
            message,
            "\n\n".join(proxies)
        )

    else:

        bot.reply_to(message, "❌ Failed.")

# ====================================
# SOCKS5
# ====================================

@bot.message_handler(commands=['socks5'])
def socks5_proxy(message):

    bot.reply_to(message, "🔄 Fetching SOCKS5 proxies...")

    proxies = fetch_proxies("socks5")

    if proxies:

        bot.reply_to(
            message,
            "\n\n".join(proxies)
        )

    else:

        bot.reply_to(message, "❌ Failed.")

# ====================================
# WEBHOOK ROUTES
# ====================================

@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def webhook():

    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)

    bot.process_new_updates([update])

    return "OK", 200

@app.route("/")
def home():

    return "Bot is running"

# ====================================
# START SERVER
# ====================================

if __name__ == "__main__":

    bot.remove_webhook()

    bot.set_webhook(
        url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
    )

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
