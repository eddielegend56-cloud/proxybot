import telebot
import requests
import time
import os
import random

# ====================================
# TELEGRAM BOT TOKEN
# ====================================

BOT_TOKEN = os.getenv("8821238721:AAGG1oosX4pQ6K9vflZRZ5tlLL79CxiWwSQ")

bot = telebot.TeleBot(BOT_TOKEN)

# ====================================
# FETCH PREMIUM QUALITY PROXIES
# ====================================

def fetch_proxies(protocol="http", limit=10):

    url = (
        "https://proxylist.geonode.com/api/proxy-list"
        f"?limit={limit}"
        "&page=1"
        "&sort_by=speed"
        "&sort_type=asc"
        f"&protocols={protocol}"
        "&anonymityLevel=elite"
        "&uptime=90"
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
            anonymity = proxy.get("anonymityLevel", "Unknown")

            protocols = proxy.get("protocols", [])

            protocol_name = protocols[0] if protocols else protocol

            # =========================
            # SPEED RATING
            # =========================

            if isinstance(latency, int):

                if latency <= 100:
                    quality = "🔥 VERY FAST"

                elif latency <= 300:
                    quality = "⚡ FAST"

                elif latency <= 700:
                    quality = "🟡 MEDIUM"

                else:
                    quality = "🐢 SLOW"

            else:
                quality = "Unknown"

            # =========================
            # FORMAT OUTPUT
            # =========================

            text = (
                f"🌍 Country: {country}\n"
                f"🏙 Region: {city}\n"
                f"📡 IP: {ip}\n"
                f"🚪 Port: {port}\n"
                f"🛡 Protocol: {protocol_name.upper()}\n"
                f"🟢 Level: {anonymity.upper()}\n"
                f"⚡ Ping: {latency} ms\n"
                f"🔥 Speed: {quality}\n"
                f"🔐 Authentication: NO\n"
                f"━━━━━━━━━━━━━━━"
            )

            results.append(text)

        return results

    except Exception as e:

        print("Error:", e)

        return []

# ====================================
# START COMMAND
# ====================================

@bot.message_handler(commands=['start'])
def start(message):

    text = (
        "🤖 ADVANCED PROXY BOT ONLINE\n\n"
        "Commands:\n"
        "/http - High quality HTTP proxies\n"
        "/socks5 - High quality SOCKS5 proxies\n"
        "/socks4 - High quality SOCKS4 proxies\n"
        "/mix - Mixed premium proxies\n"
        "/check ip:port - Check proxy status\n"
    )

    bot.reply_to(message, text)

# ====================================
# HTTP
# ====================================

@bot.message_handler(commands=['http'])
def http_command(message):

    bot.reply_to(message, "🔄 Fetching premium HTTP proxies...")

    proxies = fetch_proxies("http")

    if proxies:

        bot.reply_to(
            message,
            "✅ PREMIUM HTTP PROXIES\n\n" +
            "\n".join(proxies)
        )

    else:

        bot.reply_to(message, "❌ Failed to fetch proxies.")

# ====================================
# SOCKS5
# ====================================

@bot.message_handler(commands=['socks5'])
def socks5_command(message):

    bot.reply_to(message, "🔄 Fetching premium SOCKS5 proxies...")

    proxies = fetch_proxies("socks5")

    if proxies:

        bot.reply_to(
            message,
            "✅ PREMIUM SOCKS5 PROXIES\n\n" +
            "\n".join(proxies)
        )

    else:

        bot.reply_to(message, "❌ Failed.")

# ====================================
# SOCKS4
# ====================================

@bot.message_handler(commands=['socks4'])
def socks4_command(message):

    bot.reply_to(message, "🔄 Fetching premium SOCKS4 proxies...")

    proxies = fetch_proxies("socks4")

    if proxies:

        bot.reply_to(
            message,
            "✅ PREMIUM SOCKS4 PROXIES\n\n" +
            "\n".join(proxies)
        )

    else:

        bot.reply_to(message, "❌ Failed.")

# ====================================
# MIXED PROXIES
# ====================================

@bot.message_handler(commands=['mix'])
def mixed_command(message):

    bot.reply_to(message, "🔄 Fetching mixed premium proxies...")

    all_proxies = []

    all_proxies.extend(fetch_proxies("http", 4))
    all_proxies.extend(fetch_proxies("socks4", 3))
    all_proxies.extend(fetch_proxies("socks5", 3))

    if all_proxies:

        bot.reply_to(
            message,
            "🔥 PREMIUM MIXED PROXIES\n\n" +
            "\n".join(all_proxies)
        )

    else:

        bot.reply_to(message, "❌ Failed.")

# ====================================
# CHECK PROXY
# ====================================

@bot.message_handler(commands=['check'])
def check_proxy(message):

    try:

        proxy = message.text.split(" ")[1]

        bot.reply_to(message, f"🔍 Testing {proxy}")

        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }

        start = time.time()

        r = requests.get(
            "https://httpbin.org/ip",
            proxies=proxies,
            timeout=10
        )

        end = time.time()

        ping = round((end - start) * 1000)

        if r.status_code == 200:

            if ping <= 100:
                speed = "🔥 VERY FAST"

            elif ping <= 300:
                speed = "⚡ FAST"

            elif ping <= 700:
                speed = "🟡 MEDIUM"

            else:
                speed = "🐢 SLOW"

            bot.reply_to(
                message,
                f"✅ WORKING PROXY\n\n"
                f"📡 Proxy: {proxy}\n"
                f"⚡ Ping: {ping} ms\n"
                f"🔥 Speed: {speed}"
            )

        else:

            bot.reply_to(message, "❌ DEAD PROXY")

    except Exception as e:

        bot.reply_to(
            message,
            "Usage:\n/check ip:port"
        )

# ====================================
# ONLINE STATUS
# ====================================

print("✅ Advanced Proxy Bot Online")

while True:

    try:

        bot.infinity_polling(
            timeout=60,
            long_polling_timeout=60
        )

    except Exception as e:

        print("Error:", e)

        time.sleep(5)

