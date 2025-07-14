import discord
import json
import logging
import sys
import os
from Bot import handle_message, init_files
from Github_push import git_push

# 🚀 Push ke GitHub di awal boot
git_push()

# 🔇 Logging hanya WARNING ke atas
logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

# 🔐 Ambil token dari Token.json
def get_token():
    try:
        with open("Token.json", "r", encoding="utf-8") as f:
            return json.load(f).get("token", "").strip()
    except Exception as e:
        print(f"❌ Tidak bisa membaca Token.json: {e}")
        return ""

# 🎯 Intents minimum
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot masuk sebagai: {client.user}")
    print(f"🔗 Terhubung ke {len(client.guilds)} server")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="?help"))

@client.event
async def on_message(message):
    if not message.author.bot:
        try:
            await handle_message(message)
        except Exception as e:
            print(f"⚠️ Error handle_message: {e}")

@client.event
async def on_error(event, *args, **kwargs):
    print(f"⚠️ Error event {event}: {sys.exc_info()}")

# 🔑 Jalankan bot
if __name__ == "__main__":
    init_files()
    token = get_token()
    if not token or token == "DUMMY_ONLY":
        print("❌ Token tidak valid. Masukkan di environment.")
        sys.exit(1)

    try:
        print("🚀 Menyalakan bot...")
        client.run(token)
    except discord.LoginFailure:
        print("❌ Token Discord salah.")